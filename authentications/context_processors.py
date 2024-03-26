from urllib.parse import uses_relative
from authentications.models import User
from vendor.models import Company
from django.conf import settings

def get_vendor(request):
    try:
        vendor = Company.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)
