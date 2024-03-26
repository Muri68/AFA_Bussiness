"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from authentications import views
from vendor import views as vendor_views
from marketplace import views as market_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    
    path('', market_views.index, name='index'),
    path('hi-fi/', market_views.index2, name='index2'),
    path('search-result/', market_views.search, name='search-result'),
    path('<slug:company_slug>/', market_views.company_detail, name='company_detail'),
    path('<slug:company_slug>/products/', market_views.company_products, name='company_products'),
    path('<slug:company_slug>/write-a-review/', market_views.write_a_review, name='write-a-review'),
    path('<slug:company_slug>/contact/', market_views.contact_vendor, name='contact-vendor'),
    
    path('subscribe/', market_views.subscribe, name='subscribe'),
    
    
    path('vendor/', include('vendor.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
