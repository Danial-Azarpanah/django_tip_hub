from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from .models import Video, Comment


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
