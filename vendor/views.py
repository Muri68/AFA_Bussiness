from unicodedata import category
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError


# from .forms import CompanyForm
# from accounts.forms import UserProfileForm


from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from authentications.views import check_role_company
from .models import *
from django.template.defaultfilters import slugify

from authentications.forms import UserInfoForm
from .forms import CompanyForm, CategoryForm, FoodItemForm


def get_vendor(request):
    vendor = Company.objects.get(user=request.user)
    return vendor



####### Vendor Dashboard Function ######.
@login_required(login_url='login')
@user_passes_test(check_role_company)
def vendorDashboard(request):
    vendor = get_vendor(request)
    
    if not vendor.user.company_name:
        messages.error(request, 'Profile must be Updated before you can Proceed.')
        return redirect('vprofile')
    
    else:
        categories = Category.objects.filter(company=vendor).order_by('created_at')
        fooditems = FoodItem.objects.filter(company=vendor).order_by('created_at')
        reviews = ReviewAndRatingsR.objects.filter(company=vendor)
        v_messages = ContactVendor.objects.filter(company=vendor).order_by('created_at')
        context = {
            'vendor': vendor,
            'categories': categories,
            'fooditems': fooditems,
            'reviews': reviews,
            'v_messages': v_messages,
        }

    return render(request, 'vendor/vendorDashboard.html', context)




@login_required(login_url='login')
@user_passes_test(check_role_company)
def vprofile(request):
    user=request.user
    vendor = get_object_or_404(Company, user=request.user)
    states = State.objects.all()
    c_types = CompanyType.objects.all()
    vendor_Q_A = VendorQ_A.objects.filter(company=vendor).order_by('-created_at')
    if request.method == 'POST' and 'SaveProfile' in request.POST:
        user_form = UserInfoForm(request.POST, instance=user)
        vendor_form = CompanyForm(request.POST, request.FILES, instance=vendor)
        if user_form.is_valid() and vendor_form.is_valid():
            user_form.save()
            vendor_form.save()
            messages.success(request, 'Profile Updated Successfully.')
            return redirect('vprofile')
        else:
            messages.error(request, vendor_form.errors)
            print(user_form.errors)
            print(vendor_form.errors)
    else:
        user_form = UserInfoForm(instance=user)
        vendor_form = CompanyForm(instance=vendor)
    
    if request.method == 'POST'  and 'addQ&A' in request.POST:
        title = request.POST.get('title')
        body = request.POST.get('body')

        newReview = VendorQ_A(company=vendor, title=title, body=body)
        newReview.save()
        messages.success(request, 'Q&A Save successful!')
        return redirect('vprofile')

    context = {
        'user_form': user_form,
        'vendor_form': vendor_form,
        'vendor': vendor,
        'states': states,
        'c_types': c_types,
        'vendor_Q_A': vendor_Q_A,
    }
    return render(request, 'vendor/vprofile.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_company)
def all_products(request):
    vendor = get_vendor(request)
    if not vendor.user.company_name:
        messages.error(request, 'Profile must be Updated before you can Proceed.')
        return redirect('vprofile')
    
    else:
        items = FoodItem.objects.filter(company=vendor).order_by('-created_at')
        categories = Category.objects.filter(company=vendor).order_by('-created_at')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(items, 8)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        
        
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                category_name = form.cleaned_data['category_name']
                category = form.save(commit=False)
                category.company = get_vendor(request)
                category.category_name = category_name
                category.save()
                messages.success(request, 'added successfully!')
                    
                return redirect('v-products')
                # return redirect('products_by_category', product.category.id)
            else:
                messages.error(request, form.errors)
                print(form.errors)
        else:
            form = CategoryForm()
                

        context = {
            'vendor': vendor,
            'page_obj': page_obj,
            'categories': categories,
            'form':form,
        }
    return render(request, 'vendor/Vendorproducts.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_company)
def add_product(request):
    vendor = get_vendor(request)
    if not vendor.user.company_name:
        messages.error(request, 'Profile must be Updated before you can Proceed.')
        return redirect('vprofile')
    
    else:
        categories = Category.objects.filter(company=vendor)
        if request.method == 'POST':
            form = FoodItemForm(request.POST, request.FILES)
            if form.is_valid():
                food_title = form.cleaned_data['food_title']
                description = form.cleaned_data['description']
                food_title = form.cleaned_data['food_title']
                price = form.cleaned_data['price']
                image = form.cleaned_data['image']
                is_available = form.cleaned_data['is_available']
                fooditem = form.save(commit=False)
                fooditem.company = get_vendor(request)
                fooditem.slug = slugify(food_title)
                fooditem.description = description
                fooditem.price = price
                fooditem.image = image
                fooditem.is_available = is_available
                form.save()
                messages.success(request, 'Food added successfully!')
                return redirect('v-products')
                # return redirect('products_by_category', product.category.id)
            else:
                messages.error(request, form.errors)
                print(form.errors)
        else:
            form = FoodItemForm()
            # modify this form
            form.fields['category_name'].queryset = Category.objects.filter(company=vendor)
        
        context = {
            'categories': categories,
            'form': form,
        }
    return render(request, 'vendor/add_product.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_company)
def reviews_and_rating(request):
    vendor = get_vendor(request)
    if not vendor.user.company_name:
        messages.error(request, 'Profile must be Updated before you can Proceed.')
        return redirect('vprofile')
    
    else:
        reviews = ReviewAndRatingsR.objects.filter(company=vendor).order_by('-created_at')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(reviews, 6)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        context = {
            'page_obj': page_obj,
        }
    return render(request, 'vendor/Vendor-reviews.html', context)





def replyReview(request,id):
    review = ReviewAndRatingsR.objects.get(id=id)
    replies = ReplyComment.objects.filter(replyReview=review)
    vendor = get_vendor(request)

    if request.method == 'POST':
        company = vendor
        reply_content = request.POST.get('reply_content')

        newReply = ReplyComment(company=company, reply_content=reply_content)
        newReply.replyReview = review
        newReply.save()
        messages.success(request, 'Review replied!')
        return redirect('reviews')
    context = {
        'review': review,
        'replies': replies,
    }
    return render(request, 'vendor/Vendor-Replied-reviews.html', context)