from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filmai/', include('moviereviews.urls')),  # Pakeistas į filmo apžvalgų app
    path('', RedirectView.as_view(url='filmai/', permanent=True)),  # Numatytas puslapis
    path('accounts/', include('django.contrib.auth.urls')),  # Django auth sistema
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)