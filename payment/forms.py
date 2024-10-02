from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    
    shipping_full_name = forms.CharField(label="Shipping Full Name :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping Full Name'}), required=True)
    shipping_address1 = forms.CharField(label="Shipping Address1 :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping Address 1'}), required=True)
    shipping_address2 = forms.CharField(label="Shipping Address2 :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping Address 2'}), required=False)
    shipping_city = forms.CharField(label="Shipping City :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping City'}), required=True)
    shipping_state = forms.CharField(label="Shipping State :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping State'}), required=False)
    shipping_zipcode = forms.CharField(label="Shipping Zipcode :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping Zipcode'}), required=False)
    shipping_country = forms.CharField(label="Shipping Country :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ('shipping_full_name', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country', )

        exclude = ['user']

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="Name On Card", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name On Card'}), required=True)
    card_number = forms.CharField(label="Card Number", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}), required=True)
    card_exp_date = forms.CharField(label="Expiration Date", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}), required=True)
    card_cvv_number = forms.CharField(label="CVV Code", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV Code'}), required=True)
    card_address1 = forms.CharField(label="Billing Address 1", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address 1'}), required=True)
    card_address2 = forms.CharField(label="Billing Address 2", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address 2'}), required=False)
    card_city = forms.CharField(label="Billing City", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing City'}), required=True)
    card_state = forms.CharField(label="Billing State", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing State'}), required=True)
    card_zipcode = forms.CharField(label="Billing Zipcode", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Zipcode'}), required=True)
    card_country = forms.CharField(label="Billing Country", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Country'}), required=True)