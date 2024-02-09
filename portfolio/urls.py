from django.urls import path, re_path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.PostListView.as_view(), name='post_category_list'),
    re_path(r'(?P<slug>[-\w]+)/', views.PostDetailView.as_view(), name='post_detail'),
]
