from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

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
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        body = request.POST.get("body")
        Comment.objects.create(body=body, video=video, user=request.user, parent_id=parent_id)
    return render(request, "video/video_detail.html", context={"video": video})


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
