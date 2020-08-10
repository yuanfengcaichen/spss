from django.contrib import admin

#Register your models here.
from analysis.models import Red


@admin.register(Red)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('nicotine_mean','nicotine_sd')
    fields = ('nicotine_mean','nicotine_sd')