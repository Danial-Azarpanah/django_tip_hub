from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='home:main'), name='logout'),
    path('register', views.RegisterUserView.as_view(), name='register'),
]