from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path('all', views.VideoListView.as_view(), name='all_videos'),
    path('<int:pk>', views.VideoDetailView.as_view(), name='video_detail'),
    path('category/<slug:slug>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('delete-comment-notif/<int:pk>', views.DeleteCommentNotifView.as_view(), name='delete_comment_notif'),
    path('delete-admin-notif/<int:pk>', views.DeleteAdminNotif.as_view(), name='delete_admin_notif'),
]
