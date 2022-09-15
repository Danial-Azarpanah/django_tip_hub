from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.views.generic import ListView

from hitcount.views import HitCountMixin
from hitcount.utils import get_hitcount_model

from .models import Video, Comment, Category


class VideoListView(ListView):
    """
    View for all views page
    with pagination capability
    """
    model = Video
    template_name = 'video/all_videos.html'
    paginate_by = 2


def video_detail(request, pk):
    """
    View for video detail view
    with comment and reply capability
    """
    video = get_object_or_404(Video, id=pk)
    context = {"video": video}

    # Hit (visit) counter algorythm
    hit_count = get_hitcount_model().objects.get_for_object(video)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    if request.user.is_authenticated:
        # Check if the video is liked by the user
        if video.likes.filter(email=request.user.email).exists():
            context["is_liked"] = True
        else:
            context["is_liked"] = False

    # if method is POST, so we're getting comment or reply from a user
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        body = request.POST.get("body")
        Comment.objects.create(body=body, video=video, user=request.user, parent_id=parent_id)

    return render(request, "video/video_detail.html", context)


def category_detail(request, slug):
    """
    View for returning videos
     of the selected category
     """
    category = get_object_or_404(Category, slug=slug)
    videos = Video.objects.filter(category__title=category)

    # pagination
    page_number = request.GET.get('page')
    paginator = Paginator(videos, 1)
    objects_list = paginator.get_page(page_number)

    context = {"videos": objects_list, "category": category}
    return render(request, 'video/category_list.html', context)


def search(request):
    """
    A view to search all
    video titles with pagination
    """
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
