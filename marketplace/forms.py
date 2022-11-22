from django import forms
from .models import *

    # class EditMessageForm(forms.ModelForm):
    #     # specify the name of model to use
    #     class Meta:
    #         model = ChatMessage
    #         fields = ('msg_content',)
            


# "Buyer" Request For a Quote Form
class BuyerRequestForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, help_text='Required')
    description = forms.CharField(max_length=3000, required=True, help_text='Required')
    need_by_date = forms.DateField()
    maximum_quotes_desired = forms.IntegerField(required=True, help_text='Required')
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = BuyerRequest
        fields = [
            'title',
            'description',
            'need_by_date',
            'maximum_quotes_desired',
            'attachment',
            ]



# "Seller" Quote Form
class SellerQuoteForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, help_text='Required')
    description = forms.CharField(max_length=3000, required=True, help_text='Required')
    price = forms.IntegerField(required=True, help_text='Required')
    # expiry_date = forms.DateField()
    attachment = forms.FileField()
    

    class Meta:
        model = SellerQuote
        fields = [
            'title',
            'description',
            'price',
            # 'expiry_date',
            'attachment',
            ]
