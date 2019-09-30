from django.db import models
from django.contrib.auth.models import User


"""
    Account class is who will manage all the interactions with the database where we will save all the specific user
    information like IBAN number
    
    I'm not using a Custom User model (AbstractUser), because this information is not needed for the login management
    and in my opinion, is better to have it separated
"""


class Account(models.Model):
    # Using the most common standard length, 35 for each one and a total of 70
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)

    # Getting the max length from: https://en.wikipedia.org/wiki/International_Bank_Account_Number#Structure
    # 2 Country code + 2 Check digits + 30 BBAN (Basic Bank Account Number)
    iban = models.CharField(max_length=34, null=False, blank=False, unique=True)

    # Field to manage who created the user to restrict the permissions
    creator = models.ForeignKey(User, related_name="creator", null=False, blank=False, on_delete=models.CASCADE)

    # Returning first name + last name to have a nice view in Administration page
    def __str__(self):
        return '{0} {1} - {2}'.format(self.first_name, self.last_name, self.iban)
