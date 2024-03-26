from django.contrib import admin
from .models import NewsLetterUsers

class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')

admin.site.register(NewsLetterUsers, SubscribedUsersAdmin)

# Register your models here.
