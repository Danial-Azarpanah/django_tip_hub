from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import UserCreationForm, UserLoginForm
from .tokens import account_activation_token


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
        # save form in the memory not in database
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Send account activation email
        # to get the domain of the current site
        current_site = get_current_site(self.request)
        mail_subject = 'لینک فعالسازی به ایمیل شما ارسال گردید'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'account/email_confirmation.html')

    # Redirect the user to home page if already authenticated
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home:main')
        return super(RegisterUserView, self).get(*args, **kwargs)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home:main')
    else:
        return HttpResponse('Activation link is invalid!')
