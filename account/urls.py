from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='home:main'), name='logout'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    path("activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
         views.activate, name='activate'),

    # password reset urls
    path('reset-password/',
         auth_views.PasswordResetView.as_view(template_name="account/forgot_password.html",
                                              email_template_name="account/password_reset_email.html",
                                              success_url=reverse_lazy('account:password_reset_done')),
         name="reset_password"),

    path('reset-password/sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset-password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html",
                                                     success_url=reverse_lazy('account:password_reset_complete')),
         name="password_reset_confirm"),

    path('reset_password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"),
         name="password_reset_complete"),
]
