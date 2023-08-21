from django import forms
from django.core import validators

def start_with_09(value):
  if value[0]!='0' and value[1]!="0":
    raise forms.ValidationError("phone number should start with 09")

def is_phone_number(value):
    for i in value:
        try:
            int(i)
        except:
            raise forms.ValidationError("you only can enter numbers")
class LoginForm(forms.Form):
    username = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Enter phone number or email',"class":"form-control"}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password',"class":"form-control"}))



class RegisterForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number', "class": "form-control"}),
        validators=[start_with_09,is_phone_number])
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if len(phone) !=11:
            raise forms.ValidationError(message=f"your phone number should have 11 character not{len(phone)}",code="Invalid phone number")
        return phone
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
    