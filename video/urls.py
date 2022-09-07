from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path('all-videos', views.VideoListView.as_view(), name='all_videos'),
    path('video/<int:pk>', views.video_detail, name='video_detail'),
    path('category/<slug:slug>', views.category_detail, name='category_detail'),
]
