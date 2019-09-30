from django.conf import settings

from requests.exceptions import HTTPError

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from social_django.utils import psa

from account.models import Account
from account.serializers import SocialSerializer, AccountSerializer


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def token_authentication(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.

    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.

    ## Request format

    Requests must include the following field
    - 'access_token': The OAuth2 access token provided by the provider
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # Initializing user variable to None
        user = None

        # If not declared in settings, configuring a default value
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            # Getting the token from the request after validated
            token = serializer.validated_data['access_token']
            if token:
                # Authenticating in provider side (in our case only Google right now)
                user = request.backend.do_auth(token)
        except HTTPError as e:
            # Error authenticating in provider side (in our case only Google right now)
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            # If the user is allowed
            if user.email in settings.ADMIN_LIST or settings.ADMIN_LIST:
                user.is_active = True
                user.is_staff = True
            else:
                user.is_active = False
                user.is_staff = False
            # Save the information preventing the changes in ADMIN_LIST
            user.save()

            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                # If the account registered has not admin rights, will be inactive
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider generated as to why specifically
            # the authentication failed; this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(http_method_names=['POST'])
def logout(request):
    """
        Execute the logout functionality, which remove the current token for the user
    """
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def accounts(request):
    """
        Function to get all the accounts data from database and show them in the accounts.html
    """
    # Creating the default values
    accounts_data = []
    editable = False

    # Checking that the user doing the request is already logged in
    if request.user:
        # Retrieving all the account list
        for account in Account.objects.all():
            # If the user doing the request is the same who created it, enabling the modification/deletion rights
            if account.creator == request.user:
                editable = True
            else:
                editable = False
            accounts_data.append({
                'id': account.id,
                'first_name': account.first_name,
                'last_name': account.last_name,
                'iban': account.iban,
                'is_editable': editable,
            })

    return Response(accounts_data)


@api_view(http_method_names=['POST'])
def accounts_add(request):
    """
        Function to manage the addition of new accounts
    """
    # Creating the default value
    response = {}

    # If not declared in settings, configuring a default value
    # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
    try:
        nfe = settings.NON_FIELD_ERRORS_KEY
    except AttributeError:
        nfe = 'non_field_errors'

    # Parsing data from the request and changing the creator field for the user who did the request
    data = JSONParser().parse(request)
    data['creator'] = request.user.pk

    # Check if all the data is valid to be used
    serializer = AccountSerializer(data=data)
    if serializer.is_valid():
        # If valid, create it and notify
        try:
            Account.objects.get(iban=serializer.validated_data['iban'])
            response = {
                'errors': {
                    nfe: 'iban already exists',
                }
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            serializer.create(serializer.validated_data)
            response = {
                'status': 'ok',
                'message': 'created'
            }
    else:
        # If not valid, raise an error for data_validation
        response = {
            {'errors': {'data_validation_error': 'Error validating data'}}
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    return Response(response)


@api_view(http_method_names=['PUT'])
def accounts_modify(request):
    """
        Function to manage the accounts modification
    """
    # Creating the default value
    account = None

    # If not declared in settings, configuring a default value
    # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
    try:
        nfe = settings.NON_FIELD_ERRORS_KEY
    except AttributeError:
        nfe = 'non_field_errors'

    # Parsing data from the request and changing the creator field for the user who did the request
    data = JSONParser().parse(request)
    data['creator'] = request.user.pk

    # Check if all the data is valid to be used
    serializer = AccountSerializer(data=data)
    if serializer.is_valid():
        # If valid, try to get the model instance to check if already exists
        try:
            account = Account.objects.get(id=serializer.validated_data['id'])
            # Check if the creator is who did the request
            if request.user.pk == account.creator.pk:
                # If yes, allow to modify it
                serializer.update(account, serializer.validated_data)
            else:
                return Response(
                    {
                        'errors': {
                            nfe: 'No permissions',
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Account.DoesNotExist:
            return Response(
                {
                    'errors': {
                        nfe: 'Not exists',
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response({'status': 'ok', 'message': 'updated'})


@api_view(http_method_names=['DELETE'])
def accounts_delete(request):
    """
        Function to manage the deletion of the accounts
    """
    # Creating the default value
    account = None

    # If not declared in settings, configuring a default value
    # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
    try:
        nfe = settings.NON_FIELD_ERRORS_KEY
    except AttributeError:
        nfe = 'non_field_errors'

    # Parsing data from the request and changing the creator field for the user who did the request
    data = JSONParser().parse(request)
    data['creator'] = request.user.pk

    # Check if all the data is valid to be used
    serializer = AccountSerializer(data=data)
    if serializer.is_valid():
        # If valid, try to get the model instance to check if already exists
        try:
            account = Account.objects.get(id=serializer.validated_data['id'])

            # Check if the creator is who did the request
            if request.user.pk == account.creator.pk:
                account.delete()
                return Response({
                    'status': 'ok',
                    'message': 'deleted'
                })
            else:
                return Response(
                    {
                        'errors': {
                            nfe: 'No permissions',
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Account.DoesNotExist:
            return Response(
                {
                    'errors': {
                        nfe: 'Not exists',
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {
                'errors': {
                    'data_validation_error': 'Error validating data',
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
