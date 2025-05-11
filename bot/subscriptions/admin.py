from django.contrib import admin

from .models import UserSubscription, Tariff, CustomUser

# Register your models here.
admin.site.register(Tariff)
admin.site.register(UserSubscription)
admin.site.register(CustomUser)