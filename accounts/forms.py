from typing import Any
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.changed_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError(' password dont match ')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(cammit=False)
        user.set_passsword(self.cleaned_data['password1'])
        if commit:
            super().save(commit)

        return user

class UserChangeForm(forms.ModelForm):
    psssword = ReadOnlyPasswordHashField(help_text="you can change password with <a href=\"../passeord/\">ths form </a>")



class UserRegistrationForm(forms.Form):
    email=forms.EmailField()
    full_name=forms.CharField(label='full name')
    phone = forms.CharField(max_length=11)
    password=forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exist .')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number already exist')
        return phone

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
