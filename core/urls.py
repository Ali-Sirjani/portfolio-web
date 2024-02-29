from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile_page'),
    path('set-username/', views.set_username_view, name='set_username'),
]
