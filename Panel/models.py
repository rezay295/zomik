from django.db import models
from django.utils import timezone
from jalali_date import datetime2jalali, date2jalali


# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=100, default="ادمین", help_text="اسم ادمین")
    email = models.CharField(max_length=100, default="", help_text="ایمیل ادمین")
    phone = models.CharField(max_length=20, default="0", help_text="شماره موبایل ادمین")
    profile = models.ImageField(upload_to="adminProfile//%Y/%m/%d/%H/%m/%s", default="adminProfile/default.jpg",
                                help_text="عکس ادمین")
    password = models.TextField(default="", help_text="پسورد ادمین")


class Category(models.Model):
    title = models.CharField(max_length=100, default="")
    news_count = models.IntegerField(default=0)


class News(models.Model):
    admin = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=100, default="")
    date = models.DateTimeField(default=timezone.now)
    seenCount = models.IntegerField(default=0)
    text = models.TextField(default="")

    def per_date(self):
        return datetime2jalali(self.date).strftime('%y/%m/%d _ %H:%M:%S')