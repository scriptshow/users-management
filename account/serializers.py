from django.contrib.auth.models import User

from rest_framework import serializers

from account.models import Account
from account.utils import verify_iban


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class AccountSerializer(serializers.Serializer):
    """
    Serializer which manage and validate all the interactions with Account model
    """
    # Needed when updating an already created instance
    id = serializers.IntegerField(required=False)

    # Using the most common standard length, 35 for each one and a total of 70
    first_name = serializers.CharField(max_length=35)
    last_name = serializers.CharField(max_length=35)

    # Getting the max length from: https://en.wikipedia.org/wiki/International_Bank_Account_Number#Structure
    # 2 Country code + 2 Check digits + 30 BBAN (Basic Bank Account Number)
    iban = serializers.CharField(validators=[verify_iban, ])

    # Validating against User table
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects)

    def create(self, validated_data):
        """
        Create and return a new `Account` instance, given the validated data.
        """
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Account` instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.iban = validated_data.get('iban', instance.iban)
        instance.creator = validated_data.get('creator', instance.creator)
        instance.save()
        return instance

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'iban', 'creator')
