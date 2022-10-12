from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.views import View

from .models import Video, Comment, Category, \
    UserNotification, AdminNotification
from account.models import User


class VideoListView(ListView):
    """
    View for all views page
    with pagination capability
    """
    model = Video
    template_name = 'video/all_videos.html'
    paginate_by = 1


class VideoDetailView(View):
    """
    View for video detail view
    with comment and reply capability
    """

    def get(self, request, pk):
        video = get_object_or_404(Video, id=pk)

        # Comments pagination (infinite scroll)
        page_number = request.GET.get("page")
        paginator = Paginator(video.comments.all(), 10)
        objects_list = paginator.get_page(page_number)

        context = {"video": video, "comments": objects_list}

        # View counter algorithm with IP address
        ip_address = request.user.ip_address
        if ip_address not in video.hits.all():
            video.hits.add(ip_address)

        # Check if the video is liked by the user
        if request.user.is_authenticated:
            if video.likes.filter(email=request.user.email).exists():
                context["is_liked"] = True
            else:
                context["is_liked"] = False

        # Check if video is added to favorites by user
        if video.favorites.filter(id=request.user.id).exists():
            context["is_fav"] = True
        else:
            context["is_fav"] = False

        return render(request, "video/video_detail.html", context)

    def post(self, request, pk):
        video = get_object_or_404(Video, id=pk)
        parent_id = request.POST.get("parent_id")
        body = request.POST.get("body")
        Comment.objects.create(body=body, video=video, user=request.user, parent_id=parent_id)

        # if true, create a object for notification to display to replied user
        if parent_id:
            sender = request.POST.get("sender")
            sender = User.objects.get(email=sender)
            receiver = request.POST.get("receiver")
            receiver = User.objects.get(email=receiver)
            # if users hasn't replied his own comment, create notification
            if sender != receiver:
                UserNotification.objects.create(sender=sender,
                                                receiver=receiver,
                                                comment_id=parent_id)
        return redirect(reverse("video:video_detail", kwargs={"pk": pk}))


class CategoryDetailView(View):
    """
    View for returning videos
    of the selected category
    """

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        videos = Video.objects.filter(category__title=category)

        # pagination
        page_number = request.GET.get('page')
        paginator = Paginator(videos, 1)
        objects_list = paginator.get_page(page_number)

        context = {"videos": objects_list, "category": category}
        return render(request, 'video/category_list.html', context)


class SearchView(View):
    """
    A view to search all
    video titles with pagination
    """

    def get(self, request):
        q = request.GET.get("q")

        # Search algorythm to search video tags, title and description
        videos = Video.objects.filter(Q(tag__title__icontains=q))
        if not videos:
            videos = Video.objects.filter(Q(title__icontains=q))
            if not videos:
                videos = Video.objects.filter(Q(description__icontains=q))

        # pagination
        page_number = request.GET.get("page")
        paginator = Paginator(videos, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, "video/search_result.html", {"videos": objects_list})


class DeleteCommentNotifView(View):
    """
    This view deletes the reply notification object
    """

    def get(self, request, pk):
        notif = UserNotification.objects.get(id=pk)
        notif.delete()
        return render(request, 'video/all_videos.html')


class DeleteAdminNotif(View):
    """
    This view removes the user from the public message's receivers
    so the notification is not shown to user anymore
    """

    def get(self, request, pk):
        notif = AdminNotification.objects.get(id=pk)
        notif.receiver.remove(request.user)
        print(list(notif.receiver.all()))
        return render(request, "video/all_videos.html")
