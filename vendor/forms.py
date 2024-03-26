from django import forms
from .models import Company, Category, FoodItem
from authentications.validators import allow_only_images_validator


class CompanyForm(forms.ModelForm):
    # company_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    # company_logo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    facebook = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    twitter = forms.CharField(required=False)
    youtube = forms.CharField(required=False)
    


    class Meta:
        model = Company
        fields = ['company_logo', 'company_license', 'company_description', 'address', 'country', 'state', 'company_type', 'city',
                  'facebook', 'instagram','twitter','youtube']
    

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-floating'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name',]


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = FoodItem
        fields = ['category_name', 'food_title', 'description', 'price', 'image', 'is_available']