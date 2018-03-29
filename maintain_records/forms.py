from django import forms
from .models import *


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class ItemDetailsForm(forms.ModelForm):
    class Meta:
        model = ItemDetails
        fields = ['item_name', 'default_cost_price', 'default_selling_price']


class DealersDetailsForm(forms.ModelForm):
    class Meta:
        model = DealersDetails
        fields = ['dealer_name', 'dealer_phone_number', 'dealer_email', 'dealer_address']


class PurchaseDetailsForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetails
        fields = ['invoice_date_and_time', 'invoice_number', 'dealer', 'item_name', 'quantity']


class SalesDetailsForm(forms.ModelForm):
    class Meta:
        model = SalesDetails
        fields = ['invoice_date_and_time', 'invoice_number', 'dealer', 'item_name', 'quantity']
