from django.contrib import auth
from django.shortcuts import render, redirect

from account.utils import verify_iban
from usersmanagement.settings import ADMIN_LIST
from account.models import Account

"""
    Just load the login.html where the Google Auth is configured
"""


def login(request):
    return render(request, 'account/login.html')


"""
    Execute the logout functionality    
"""


def logout(request):
    if request.user:
        auth.logout(request)
    return redirect('home')


"""
    Function to manage the login, just check that the user logged by Google Auth is inside the ADMIN_LIST, if yes,
    keep it there and give the Administrator rights, if not, just remove the user, because is not allowed.
"""


def after_login(request):
    # Getting the user from the request
    user = request.user

    # Checking if the user is allow to be Administrator
    if user.email in ADMIN_LIST or '*' in ADMIN_LIST:
        if not user.is_staff:
            # Enabling the staff permissions
            user.is_staff = True
            user.save()
    # If it's not allowed, delete it
    else:
        user.delete()

    return redirect('home')


"""
    Function to get all the accounts data from database and show them in the accounts.html
"""


def accounts(request):
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

    return render(request, 'account/accounts.html', {'accounts_data': accounts_data})


"""
    Function to manage the addition of new accounts
"""


def accounts_add(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        iban = request.POST['iban']
        if verify_iban(iban):
            creator = request.user
            account = Account.objects.filter(first_name=first_name, last_name=last_name)

            if not account.exists():
                account = Account(first_name=first_name, last_name=last_name, iban=iban, creator=creator)
                account.save()

        return redirect('accounts')
    elif request.method == 'GET':
        return render(request, 'account/add_account.html')


"""
    Function to manage the accounts modification
"""


def accounts_modify(request, id=None):
    if id is None:
        return redirect('accounts')

    account = None

    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return redirect('accounts')

    if account and request.user == account.creator:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            iban = request.POST['iban']

            if verify_iban(iban):
                account.first_name = first_name
                account.last_name = last_name
                account.iban = iban
                account.save()

            return redirect('accounts')

        if request.method == 'GET':
            account_data = None

            if account.creator == request.user:
                account_data = account

            return render(request, 'account/edit_account.html', {'account_data': account_data})


"""
    Function to manage the deletion of the accounts
"""


def accounts_delete(request, id=None):
    if request.method in ["DELETE", "POST"]:
        if id is None:
            return redirect('accounts')

        account = None

        try:
            account = Account.objects.get(id=id)
        except Account.DoesNotExist:
            return redirect('accounts')

        if account and request.user == account.creator:
            account.delete()

        return redirect('accounts')
