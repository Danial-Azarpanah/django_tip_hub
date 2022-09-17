from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path('all', views.VideoListView.as_view(), name='all_videos'),
    path('<int:pk>', views.video_detail, name='video_detail'),
    path('category/<slug:slug>', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),
    path('delete-comment-notif/<int:pk>', views.delete_comment_notif, name='delete_comment_notif'),
    path('delete-admin-notif/<int:pk>', views.delete_admin_notif, name='delete_admin_notif'),
]
