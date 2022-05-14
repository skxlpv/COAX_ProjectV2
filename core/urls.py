from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'), name='base'),
    path('api/', include('api.urls'), name='api'),
]
