from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model
    """
    email = models.EmailField(
        verbose_name='آدرس ایمیل',
        max_length=255,
        unique=True,)
    username = models.CharField(
        max_length=50, unique=True, verbose_name='نام کاربری')
    phone_number = models.CharField(
        max_length=11, unique=True, blank=True,
        null=True, verbose_name='شماره موبایل')
    first_name = models.CharField(
        max_length=50, verbose_name='نام',
        blank=True, null=True)
    last_name = models.CharField(
        max_length=50, verbose_name='نام خانوادگی',
        blank=True, null=True)
    image = models.ImageField(
        upload_to='images/users', null=True,
        blank=True, verbose_name='تصویر')
    bio = models.TextField(
        null=True, blank=True)
    instagram = models.URLField(
        blank=True, null=True, unique=True,
        verbose_name='آیدی اینستاگرام')
    github = models.URLField(
        blank=True, null=True, unique=True,
        verbose_name='آدرس گیتهاب')
    linkedin = models.URLField(
        blank=True, null=True, unique=True,
        verbose_name='آدرس لینکدین')
    twitter = models.URLField(
        blank=True, null=True, unique=True,
        verbose_name='آدرس توییتر')
    is_active = models.BooleanField(
        default=True, verbose_name='فعال')
    is_staff = models.BooleanField(
        default=False, verbose_name='کارمند')
    is_superuser = models.BooleanField(
        default=False, verbose_name='ادمین')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'

    def __str__(self):
        return self.email
