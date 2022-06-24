from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Med Site API",
        default_version=settings.DEFAULT_API_VERSION,
        description="Med Site API docs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_urlpatterns_v1 = [
    path('api/', include('api.urls')),
    path('users/', include('users.urls', namespace='users-app')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('articles/', include(('articles.urls', 'articles'))),
    path('management/', include(('management.urls', 'management'))),
    path('hospitals/', include('hospitals.urls'), name='hospitals'),
    path('events/', include(('events.urls', 'events'))),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('docs/', schema_view.with_ui(cache_timeout=0), name='docs-redoc-schema-ui'),
    path('v1/', include((api_urlpatterns_v1, 'v1')))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
