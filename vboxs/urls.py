
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/login/', RedirectView.as_view(url='/')),
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('daily/', include('dailylist.urls')),
    path('order/', include('order.urls')),




]


#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)