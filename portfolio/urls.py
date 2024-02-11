from django.urls import path, re_path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('blog/', views.PostListView.as_view(), name='post_list'),
    path('blog/search/', views.PostSearchView.as_view(), name='post_search'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    re_path(r'blog/category/(?P<slug>[-\w]+)/', views.PostListView.as_view(), name='post_category_list'),
    re_path(r'blog/(?P<slug>[-\w]+)/', views.PostDetailView.as_view(), name='post_detail'),
    re_path(r'projects/(?P<slug>[-\w]+)/', views.ProjectDetailView.as_view(), name='project_detail'),
]
