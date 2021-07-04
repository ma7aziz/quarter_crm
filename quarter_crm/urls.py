from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import userLogin as login
from accounts.views import create_user as signup
# from core.views import handle_404, handle_500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login, name='user_login'),
    path('create_user', signup, name="create_user"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('', include('service.urls')),
    path('', include('accounts.urls')),
    path('install/', include('install.urls')),
    path('repair/', include('repair.urls')),
    path('quarter/', include('quarter.urls')),
    path('files/', include("files.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = handle_404
# handler500 = handle_500
