from django.contrib import admin
from django.urls import path, include
from vendor import views as vendor_views

urlpatterns = [    
    path('dashboard/', vendor_views.vendorDashboard, name='vendor-dashboard'),
    path('profile/', vendor_views.vprofile, name='vprofile'),
    path('products-builder/products/all/', vendor_views.all_products, name='v-products'),
    path('products-builder/product/add/', vendor_views.add_product, name='add_product'),
    path('reviews/', vendor_views.reviews_and_rating, name='reviews'),
    path('reviews/<int:id>/', vendor_views.replyReview, name='reply-review'),
    
]
