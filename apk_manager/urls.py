
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('app_management.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('app_management.urls')),
    path('accounts/', include('accounts.urls')),
)

from django.views.i18n import set_language

urlpatterns += [
    re_path(r'^set_language/$', set_language, name='set_language'),
]