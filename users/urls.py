from django.urls import path

from .views import BlackListTokenView


app_name = 'users'

urlpatterns = [
    path('logout/blacklist/', BlackListTokenView.as_view(), name='blacklist')
]
