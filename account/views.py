from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.views import PasswordResetView
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View

from .forms import UserCreationForm, UserLoginForm, UserEditForm
from .tokens import account_activation_token
from .models import User
from video.models import Video


class LoginUserView(LoginView):
    """
    View for logging users in
    """

    template_name = 'account/login.html'
    redirect_authenticated_user = True
    fields = '__all__'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('home:main')


class RegisterUserView(CreateView):
    """
    View to register new users
    """
    template_name = 'account/register.html'
    success_url = reverse_lazy('home:main')
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Send account activation email
        current_site = get_current_site(self.request)  # to get the domain of the current site
        mail_subject = 'لینک فعالسازی به ایمیل شما ارسال گردید'
        message = render_to_string('account/account_active_email.html', {
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


class ProfileView(TemplateView):
    """
    View to users profile if logged in. Otherwise, return to login page
    """
    template_name = 'account/user-panel.html'

    # Redirect to login page if not authenticated
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account:login')
        return super().get(*args, **kwargs)


class ProfileEditView(UpdateView):
    """
    View to edit user info
    """
    model = User
    template_name = 'account/edit-user-panel.html'
    form_class = UserEditForm

    def form_valid(self, form):
        form.save()
        return redirect('account:profile')

    # Redirect to login page if not authenticated
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account:login')
        return super().get(*args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view
    for managing errors
    """
    template_name = "account/forgot_password.html"
    email_template_name = "account/password_reset_email.html"
    success_url = reverse_lazy('account:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            form.add_error('email', 'کاربری با این ایمیل موجود نیست')
            return super(CustomPasswordResetView, self).form_invalid(form)  # if user is not found
        else:
            return super(CustomPasswordResetView, self).form_valid(form)  # if user is available

    # Redirect to login page if not authenticated
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account:login')
        return super().get(*args, **kwargs)


class ActivateView(View):
    """
    View for activating new accounts
    after clicking on the link in
    activation email
    """

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home:main')
        else:
            return HttpResponse('Activation link is invalid!')


class LikeView(View):
    """
    View to like videos with ajax
    """

    def post(self, request):
        result = ""
        id = int(request.POST.get("videoid"))
        video = get_object_or_404(Video, id=id)

        # If user has already liked the video, so unlike it.
        if video.likes.filter(id=request.user.id).exists():
            video.likes.remove(request.user)
            video.like_count -= 1
            result = video.like_count,
            liked = False
            video.save()
        # If user hasn't liked the video yet, like it.
        else:
            video.likes.add(request.user)
            video.like_count += 1
            result = video.like_count
            liked = True
            video.save()

        return JsonResponse({"result": result, "liked": liked})


class AddFavoriteView(View):
    """
    Add or remove a video from favorites
    """

    def get(self, request, pk):
        video = get_object_or_404(Video, id=pk)

        if video.favorites.filter(id=request.user.id).exists():
            video.favorites.remove(request.user)
            return JsonResponse({"response": "deleted"})
        else:
            video.favorites.add(request.user)
            return JsonResponse({"response": "added"})


class FavoriteListView(ListView):
    """
    View to display user's favorite videos
    """

    def get(self, request):
        videos = Video.objects.filter(favorites=request.user)
        # pagination
        page_number = request.GET.get("page")
        paginator = Paginator(videos, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, "account/favorites.html", {"videos": objects_list})
