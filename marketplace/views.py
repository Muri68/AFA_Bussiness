from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import NewsLetterUsers
from vendor .models import *

# Create your views here.
def index(request):
    return render(request, 'marketplace/index.html')


def index2(request):
    states = State.objects.all()
    c_type = CompanyType.objects.all()
    context = {
        'states': states,
        'c_type': c_type,
    }
    return render(request, 'marketplace/hi-fi.html' , context)


def is_valid_queryparam(param):
    return param != '' and param is not None


def search(request):
    qs = Company.objects.all().order_by('-is_sponsored')
    states = State.objects.all()
    c_type = CompanyType.objects.all()
    state = request.GET.get('state')
    companytype = request.GET.get('companytype')

    if is_valid_queryparam(state) and state != 'Select Location...':
        qs = qs.filter(state__name=state)
    
    if is_valid_queryparam(companytype) and companytype != 'Select Category...':
        qs = qs.filter(company_type__type=companytype)

    context = {
        'qs': qs,
        'states': states,
        'companytype': companytype,
        'state': state,
    }
    return render(request, 'marketplace/search_result.html', context)




def company_detail(request, company_slug):
    company = get_object_or_404(Company, company_slug=company_slug)
    # room_type = RoomType.objects.filter(company=company)
    # rooms = Room.objects.filter(company=company)[:3]
    reviews = ReviewAndRatingsR.objects.filter(company=company).order_by('-created_at')
    categories = Category.objects.filter(company=company)
    fooditems = FoodItem.objects.filter(company=company)
    vendorQ_A = VendorQ_A.objects.filter(company=company).order_by('-created_at')
    context = {
        'company': company,
        # 'room_type': room_type,
        # 'rooms': rooms,
        'categories': categories,
        'fooditems': fooditems,
        'reviews': reviews,
        'vendorQ_A': vendorQ_A,
    }
    return render(request, 'marketplace/company_detail.html', context)


def company_products(request, company_slug):
    company = get_object_or_404(Company, company_slug=company_slug)
    categories = Category.objects.filter(company=company)
    fooditems = FoodItem.objects.filter(company=company)
    context = {
        'company': company,
        'categories': categories,
        'fooditems': fooditems,
    }
    return render(request, 'marketplace/company_products.html', context)



def write_a_review(request, company_slug):
    company = get_object_or_404(Company, company_slug=company_slug)
    context = {
        'company': company,
        'values': request.POST
    }
    if request.method == 'POST':
        company = company
        full_name = request.POST.get('full_name')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        
        if not full_name:
            messages.error(request, 'Your Name is required')
            return render(request, 'marketplace/write_a_review.html', context)
        if not rating:
            messages.error(request, 'To rate this Vendor you must At least give a Star')
            return render(request, 'marketplace/write_a_review.html', context)

        newReview = ReviewAndRatingsR(company=company, full_name=full_name, review=review, rating=rating)
        newReview.save()
        messages.success(request, 'Review Save successful!')
        return redirect('company_detail', company.company_slug)
    return render(request, 'marketplace/write_a_review.html', context)


def contact_vendor(request, company_slug):
    company = get_object_or_404(Company, company_slug=company_slug)
    context = {
        'company': company,
        'values': request.POST
    }
    
    if request.method == 'POST':
        company = company
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if not full_name:
            messages.error(request, 'Your Name is required')
            return render(request, 'marketplace/contact_vendor.html', context)
        if not email:
            messages.error(request, 'Email is required')
            return render(request, 'marketplace/contact_vendor.html', context)
        if not subject:
            messages.error(request, 'Message Body is required')
            return render(request, 'marketplace/contact_vendor.html', context)

        newMessage = ContactVendor(company=company, full_name=full_name, email=email, 
                                   phone_number=phone_number, subject=subject, message=message)
        newMessage.save()
        messages.success(request, 'Message Send successful!')
        return redirect('company_detail', company.company_slug)
    
    return render(request, 'marketplace/contact_vendor.html', context)



def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect('index') 

        subscribe_user = NewsLetterUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect('index')  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('index') 

        subscribe_model_instance = NewsLetterUsers()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect('index') 