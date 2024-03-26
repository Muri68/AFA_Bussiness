from django.contrib import admin
from .models import *


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'user', 'company_type', 'company_logo', 'company_license', 'country', 'state', 'is_approved', 'created_at')
    list_display_links = ('user',)
    list_editable = ('is_approved',)
    # prepopulated_fields = {"company_slug": ("id",)+("company_type",)}


admin.site.register(Company, CompanyAdmin)

admin.site.register(State)
admin.site.register(CompanyType)
admin.site.register(FoodItem)
admin.site.register(Category)
admin.site.register(ReviewAndRatingsR)
admin.site.register(ReplyComment)
admin.site.register(ContactVendor)
admin.site.register(VendorQ_A)