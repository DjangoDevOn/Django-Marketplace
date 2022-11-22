from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Selling
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm


# Sign Up Buyer Form
class SignUpBuyerForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Business email address')
    useralias = forms.CharField(max_length=100, help_text='Username')

    class Meta:
        model = User
        fields = [
            'email',
            'useralias',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'company_name',
            'business_street_address',
            'business_street_address2',
            'city',
            'state',
            'zip_code',
            'company_phone_number',
            ]

class CustomMMCF(forms.ModelMultipleChoiceField):    
    def label_from_instance(self, selling):
        return selling.selling

# Sign Up Seller Form 
class SignUpSellerForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Business email address')
    useralias = forms.CharField(max_length=100, help_text='Username')

    class Meta:
        model = User
        fields = [
            'email',
            'useralias',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'company_name',
            'business_street_address',
            'business_street_address2',
            'city',
            'state',
            'zip_code',
            'company_phone_number',
            'selling'
            ]

        selling = CustomMMCF(
        queryset=Selling.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
 