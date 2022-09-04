from django.views.generic import ListView

from .models import Video


class AllVideos(ListView):
    """
    View for all views page
    with pagination capability
    """
    model = Video
    template_name = 'video/all_videos.html'
    paginate_by = 2

