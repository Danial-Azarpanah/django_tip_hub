from video.models import Category


def video(request):
    """
    To have categories on the header of all pages
    """
    categories = Category.objects.all()
    return {"categories": categories}
