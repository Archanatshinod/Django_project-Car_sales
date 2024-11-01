from django.contrib import admin

from .models import *


# Register your models here.
admin.site.register(Login)
admin.site.register(User)
admin.site.register(OilType)
admin.site.register(Brand)
admin.site.register(CarForSale)
admin.site.register(CarForRent)
