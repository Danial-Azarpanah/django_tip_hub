from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from social_django.models import Association, Nonce, UserSocialAuth

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('video/', include('video.urls')),
    path('google/', include('social_django.urls', namespace='social')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# For unregistering social auth models from admin panel
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
