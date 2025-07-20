from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

import requests

def get_usd_to_uzs_rate():
    try:
        response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/USD/")
        response.raise_for_status()
        data = response.json()
        return Decimal(data[0]["Rate"])
    except Exception as e:
        print(f"Kurs olishda xatolik: {e}")
        return Decimal("12500")  # fallback qiymat



class Taminotchi(models.Model):
    taminotchi_ismi = models.CharField(max_length=200)
    taminotchi_telefon_raqami = models.CharField(max_length=14,null=True,blank=True)
    taminotchi_turar_joyi = models.CharField(max_length=500,null=True,blank=True)

    def umumiy_qarz(self):
        today = timezone.localdate()
        usd_rate = get_usd_to_uzs_rate()

        purchases = self.purchases.filter(sana__lte=today)
        total_purchase_uzs = 0
        for p in purchases:
            amount = p.umumiy_miqdor
            if p.currency == 'USD':
                amount *= p.dollar_amount
            total_purchase_uzs += amount

        payments = self.payments.filter(sana__lte=today)
        total_payment_uzs = 0
        for p in payments:
            amount = p.summa
            if p.currency == 'USD':
                amount *= p.dollar_amount2
            total_payment_uzs += amount

        return total_purchase_uzs - total_payment_uzs
    class Meta:
        verbose_name = "Yetqazib beruvchi"            
        verbose_name_plural = "Yetqazib beruvchilar" 

    def __str__(self):
        return f"{self.id} - Yetqazib beruvchi - {self.taminotchi_ismi} - {self.taminotchi_telefon_raqami}"
class Pul_olish(models.Model):
    status_choice2 = [
        ("tolangan","To'langan"),
        ("tolanmagan","To'lanmagan"),
        
    ]
    taminotchi = models.ForeignKey(Taminotchi,on_delete=models.CASCADE,null=True,blank=True,related_name='purchases')
    sabab = models.CharField(max_length=200,null=True,blank=True)
    sana = models.DateField()
    umumiy_miqdor = models.DecimalField(max_digits=30,decimal_places=2)
    tolangan = models.DecimalField(max_digits=30,default=0,decimal_places=2)
    status = models.CharField(max_length=25,choices=status_choice2,default="tolanmagan")
    currency = models.CharField(max_length=3, choices=[("UZS", "UZS"), ("USD", "USD")], default="UZS")
    dollar_amount = models.FloatField(default=0)

    class Meta:
        verbose_name = "Qarz olish"            
        verbose_name_plural = "Qarz olish"  

    def __str__(self):
        return f"{self.taminotchi} - {self.umumiy_miqdor}"
    
class Pul_berish(models.Model):
    
    taminotchi = models.ForeignKey(Taminotchi,on_delete=models.CASCADE,null=True,blank=True,related_name='payments')
    pul_olingan = models.ForeignKey(Pul_olish,on_delete=models.CASCADE,null=True,blank=True,related_name='payments')
    sana = models.DateField()
    
    summa = models.DecimalField(max_digits=30,decimal_places=2)
    notification_sent = models.BooleanField(default=False)
    berildi = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, choices=[("UZS", "UZS"), ("USD", "USD")], default="UZS")
    dollar_amount2 = models.FloatField(default=0)
    def __str__(self):
        return f"{self.taminotchi} - olingan:{self.pul_olingan} -  berildi:{self.summa} sana: {self.sana}"
    class Meta:
        verbose_name = "Qarz to'lash"            
        verbose_name_plural = "Qarz to'lash" 
    
class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    telefon_number = models.CharField(max_length=14,null=True,blank=True)
    telegram_bot_login = models.CharField(max_length=200)
    can_add_expanse = models.BooleanField(default=False)
    can_add_expanse_to_others = models.BooleanField(default=False)
    can_add_new_users = models.BooleanField(default=False)
    can_change_expanse = models.BooleanField(default=False)
    can_show_harajatlar = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Foydalanuvchi"            
        verbose_name_plural = "Foydalanuvchilar" 

    def calculating_users_expanse(self):
        total_expanse = self.expanses.aggregate(models.Sum("summa"))["summa__sum"] or 0
        return total_expanse
    
    def __str__(self):
        return f"{self.id} - Foydalanuvchi- {self.telegram_bot_login}"

class Harajatlar(models.Model):
    ishchi = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name = "expanses")
    sabab = models.CharField(max_length=300,null=True,blank=True)
    summa = models.DecimalField(decimal_places=2,max_digits=30)
    sana = models.DateField()

    class Meta:
        verbose_name = "Harajat"            
        verbose_name_plural = "Harajatlar" 

    def __str__(self):
        return f"{self.id} - Ishchi: {self.ishchi} - summa: {self.summa} - sabab: {self.sabab}"

