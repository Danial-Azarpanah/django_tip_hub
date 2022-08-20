from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate

from .forms import UserCreationForm, UserLoginForm


class LoginUserView(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    fields = '__all__'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('home:main')


class RegisterUserView(CreateView):
    template_name = 'account/register.html'
    success_url = reverse_lazy('home:main')
    form_class = UserCreationForm

    # Login to user right after registering
    def form_valid(self, form):
        form.save()  # Save the user first
        email = self.request.POST['email']
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
        return redirect('home:main')

    # Redirect the user to home page if already authenticated
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home:main')
        return super(RegisterUserView, self).get(*args, **kwargs)
