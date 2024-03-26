from enum import unique
from django.db import models
from django.utils.text import slugify 
from authentications.models import User, user_directory_path
from authentications.utils import send_notification
from datetime import time, date, datetime
from django.utils.safestring import mark_safe


class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class CompanyType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Company(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    company_type = models.ForeignKey(CompanyType, default=1, on_delete=models.CASCADE, related_name='company_type', blank=True, null=True)
    company_slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    company_license = models.ImageField(upload_to=user_directory_path, default='license.png', null=True, blank=True)
    company_logo = models.ImageField(upload_to=user_directory_path, default='logo2.png', null=True, blank=True)
    cover_photo = models.ImageField(upload_to=user_directory_path, default='banner.png', blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.ForeignKey(State, default=1, on_delete=models.CASCADE, related_name='company_state', blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)

    facebook = models.CharField(max_length=150, blank=True, null=True)
    instagram = models.CharField(max_length=150, blank=True, null=True)
    twitter = models.CharField(max_length=150, blank=True, null=True)
    youtube = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # def save(self, *args, **kwargs):
    #     self.company_slug = slugify(self.user.email)
    #     super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.company_name
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = "Companies"
    
    def thumbnail(self):
        return mark_safe("<img src='%s' width='50' height='50' style='object-fit: cover; border-radius: 6px' />" % (self.company_logo.url))
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Company.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # Send notification email
                    mail_subject = f"Congratulations! Your {self.company_type.type} has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template, context)
                    
        self.company_slug = slugify(self.user.email) 
        return super(Company, self).save(*args, **kwargs)



########### MODELS FOR RESTAURANT  ###########
class Category(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def clean(self):
        self.category_name = self.category_name.capitalize()
    
    def __str__(self):
        return self.category_name
    
    def categories_count(self):
        FoodItem.objects.filter(category_name=self).count()


class FoodItem(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='restaurantimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title
    

# class ReviewAndRatingsH(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=100)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     review = models.CharField(max_length=500)
#     rating = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.room.room_number}: {self.rating}"


class ReviewAndRatingsR(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    review = models.CharField(max_length=500)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.user.company_name}: {self.rating}"


class ReplyComment(models.Model):
    replyReview = models.ForeignKey(ReviewAndRatingsR, on_delete=models.CASCADE, related_name='replies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reply_content = models.TextField()
    replied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "'{}' replied with '{}' to '{}'".format(self.company,self.reply_content, self.replyReview)
    
    

class ContactVendor(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message for  {self.company.user.company_name}: {self.message}"
    

class VendorQ_A(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Q&A for  {self.company.user.company_name}"