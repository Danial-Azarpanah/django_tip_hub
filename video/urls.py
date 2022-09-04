from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path('all-videos', views.AllVideos.as_view(), name='all_videos')
]
