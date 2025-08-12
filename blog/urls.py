from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('search/', views.search, name='search'),
    path('archive/', views.archive, name='archive'),
    path('archive/<int:year>/<int:month>/', views.archive_month, name='archive_month'),
    path('post/<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
]