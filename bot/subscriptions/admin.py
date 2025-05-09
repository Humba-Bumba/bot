from django.contrib import admin

from .models import UserSubscription, Tariff

# Register your models here.
admin.site.register(Tariff)
admin.site.register(UserSubscription)