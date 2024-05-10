from django import forms
from .models import ShippingAddress




class ShippingForms(forms.ModelForm):

    full_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'نام و نام خانوادگی'}), required=True)
    phone= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'تلفن'}), required=True)
    city= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'شهر'}), required=False)
    address= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'آدرس'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'phone', 'city', 'address']

        exclude = ['user',]



