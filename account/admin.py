from django.contrib import admin
from account.models import Account

# Adding Account class to administration page
admin.site.register(Account)
