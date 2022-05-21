from django.contrib import admin

from .models import User, Account
from django.contrib.sessions.models import Session

admin.site.register(User)
admin.site.register(Session)
admin.site.register(Account)