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
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', views.ProfileEditView.as_view(), name='edit-profile'),

    # video liking url
    path("like", views.like, name="like"),

    # favorites add and favorites' list
    path("add-favorite/<int:pk>", views.favorite_add, name="favorite_add"),
    path("favorite-list", views.FavoriteListView.as_view(), name="favorite_list"),

    # password reset urls
    path('reset-password/', views.CustomPasswordResetView.as_view(), name='reset_password'),

    path('reset-password/sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset-password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html",
                                                     success_url=reverse_lazy('account:password_reset_complete')),
         name="password_reset_confirm"),

    path('reset-password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"),
         name="password_reset_complete"),
]
