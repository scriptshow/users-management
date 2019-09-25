from django.db import models
from django.contrib.auth.models import User


"""
    Account class is who will manage all the interactions with the database where we will save all the specific user
    information like IBAN number.
    
    I'm not using a Custom User model (AbstractUser), because this information is not needed for the login management
    and in my opinion, is better to have it separated.
"""


class Account(models.Model):
    # Linking each account number to a Django user
    user = models.OneToOneField(User, unique=True, null=False, blank=False, on_delete=models.CASCADE)

    # Getting the max length from: https://en.wikipedia.org/wiki/International_Bank_Account_Number#Structure
    # 2 Country code + 2 Check digits + 30 BBAN (Basic Bank Account Number)
    iban = models.CharField(max_length=34, null=False, blank=False)

    # Returning first name + last name to have a nice view in Administration page
    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)
