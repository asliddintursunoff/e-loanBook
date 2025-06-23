from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Taminotchi,Pul_olish,Pul_berish,Harajatlar

admin.site.register(CustomUser)
admin.site.register(Taminotchi)
admin.site.register(Pul_olish)
admin.site.register(Pul_berish)
admin.site.register(Harajatlar)