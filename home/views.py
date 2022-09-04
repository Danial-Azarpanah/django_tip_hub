from django.views.generic import TemplateView

from video.models import Video


class HomeView(TemplateView):
    """
    View for home page
    with some
    """
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.all()[:6]
        return context

