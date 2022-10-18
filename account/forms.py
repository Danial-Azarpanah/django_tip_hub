from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={'placeholder': 'آدرس ایمیل'}))
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'phone_number', 'username', 'bio', 'image',
                  'instagram', 'github', 'linkedin', 'twitter')

    def clean_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError('گذرواژه باید بیشتر از ۸ کاراکتر داشته باشد.', 'short_password')
        return password

    def clean_username(self):
        # Check that the username for registration is not already taken
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('کاربر با این نام کاربری از قبل موجود است.'), 'username_taken')
        return username

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom form for user login
    """
    username = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={'placeholder': 'آدرس ایمیل'}))
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه'}))

    error_messages = {
        "invalid_login":
            "کاربری با این مشخصات موجود نیست",
    }


class UserEditForm(forms.ModelForm):
    """
    A form for editing users
    with a little modification to fields
    """
    first_name = forms.CharField(
        label='نام',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'نام'}))
    last_name = forms.CharField(
        label='نام خانوادگی',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}))
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
    phone_number = forms.CharField(
        label='شماره موبایل',
        required=False,
        max_length=11,
        min_length=11,
        widget=forms.TextInput(
            attrs={'placeholder': 'شماره موبایل                                   مثال:۰۹۱۲۱۲۳۴۵۶۷'}))
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    bio = forms.CharField(
        label='بیوگرافی',
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'بیوگرافی',
                   'class': 'comment-area w-100',
                   'style': 'background-color: rgba(0, 0, 0, 0.05);'}))
    instagram = forms.CharField(
        label='آدرس اینستاگرام',
        required=False, widget=forms.URLInput(
            attrs={'placeholder': 'آدرس اینستاگرام'}
        ))
    github = forms.CharField(
        label='آدرس گیتهاب',
        required=False,
        widget=forms.URLInput(
            attrs={'placeholder': 'آدرس گیتهاب'}
        ))
    linkedin = forms.CharField(
        label='آدرس لینکدین',
        required=False,
        widget=forms.URLInput(
            attrs={'placeholder': 'آدرس لینکدین'}
        ))
    twitter = forms.CharField(
        label='آدرس گیتهاب',
        required=False,
        widget=forms.URLInput(
            attrs={'placeholder': 'آدرس توییتر'}
        ))
    image = forms.ImageField(required=False, label='تصویر')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'phone_number', 'username', 'bio', 'image',
                  'instagram', 'github', 'linkedin', 'twitter')


class PasswordEditForm(forms.ModelForm):
    """
    Form for changing the password of an authenticated user
    """
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه جدید'}))
    password2 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput(attrs={'placeholder': 'تکرار گذرواژه جدید'}))

    class Meta:
        model = User
        fields = ["password1", "password2"]

    def clean(self):
        cd = self.cleaned_data
        if cd.get("password1") != cd.get("password2"):
            raise ValidationError("گذرواژه ها یکسان نیستند، لطفا دوباره امتحان نمائید", "different_passwords")
        if len(cd.get("password1")) < 8:
            raise ValidationError("طول گذرواژه باید بیشتر از ۸ کاراکتر باشد", "short_password")


