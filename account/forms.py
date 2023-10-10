from django import forms
from django.core import validators
from django.views.generic import FormView

from account.models import Address, User


def start_with_09(value):
  if value[0]!='0' and value[1]!="0":
    raise forms.ValidationError("phone number should start with 09")

def is_phone_number(value):
        try:
            int(value)
        except:
            raise forms.ValidationError("you only can enter numbers")
class LoginForm(forms.Form):
    username = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Enter phone number or email',"class":"form-control"}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password',"class":"form-control"}))



class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username',"class":"form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', "class": "form-control"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Enter your email","class":"form-control"}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number', "class": "form-control"}),
        validators=[start_with_09,is_phone_number])
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        user =None

        if len(phone) !=11:
            raise forms.ValidationError(message=f"your phone number should have 11 character not{len(phone)}",code="Invalid phone number")
        try:
            user = User.objects.get(phone_number=phone)
        except:
            pass
        if user is not None:
            raise forms.ValidationError(message="your phone number have to be unique", code="existed phone number")
        return phone
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = None
        try:
            user = User.objects.get(email=email)
        except :
            pass
        if user is not None:
            raise forms.ValidationError(message="your email have to be unique",code="existed email")

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            pass
        if  user is not None:
            raise forms.ValidationError(message="your username have to be unique", code="existed username")
        return username


class CheckOptForm(forms.Form):
    expire_code = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter expire code', "class": "form-control"}),
        )

    def clean_expire_code(self):
        xcode = self.cleaned_data.get('expire_code')
        if xcode >9999:
            raise forms.ValidationError(message="your code must be Four-digit",
                                        code="Invalid expire code")

        return xcode
class AddAdressForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Enter your email", "class": "form-control"}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your city", "class": "form-control"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your name", "class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your address", "class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number', "class": "form-control"}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter postal code', "class": "form-control"}))
    user = forms.IntegerField(widget=forms.TextInput(attrs={'class':'d-none'}),required=False)



