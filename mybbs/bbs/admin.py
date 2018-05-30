from django.contrib import admin
from bbs import models


# Register your models here.

class Mynews(admin.ModelAdmin):
    list_display = ("title", "url", "avatar", "summary", "new_type")


admin.site.register(models.News, Mynews)
