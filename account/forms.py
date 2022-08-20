from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'placeholder': 'آدرس ایمیل'}))
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه'}))

    class Meta:
        model = User
        fields = ('email', 'username')

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
    error_messages = {
        "invalid_login":
            "کاربری با این مشخصات موجود نیست",
    }


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active')
