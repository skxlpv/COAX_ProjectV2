from django.urls import path

from .views import BlackListTokenView, current_user


app_name = 'users'

urlpatterns = [
    path('logout/blacklist/', BlackListTokenView.as_view(), name='blacklist'),
    path('user/', current_user, name='user')
]
