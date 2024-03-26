from allauth.account.forms import SignupForm 
from django import forms 
from .models import User

class CustomSignupForm(SignupForm): 
    email = forms.CharField(label='email')
    website = forms.CharField(label='Website')
    company_name = forms.CharField(label='Company Name')
    mobile_number = forms.CharField(label='Mobile Number')
    job_title = forms.CharField(label='Job Title')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
		
        email = self.cleaned_data['email']
        website = self.cleaned_data['website']
        company_name = self.cleaned_data['company_name']
        mobile_number = self.cleaned_data['mobile_number']
        job_title = self.cleaned_data['job_title']
        
        user.email = email
        user.website = website
        user.company_name = company_name
        user.mobile_number = mobile_number
        user.job_title = job_title

        user.save()
        return user
    
    
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['company_name', 'mobile_number', 'website']
        
    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-floating'
