from django.urls import path
from django.conf.urls import url
from . import views
from .views import SearhListView
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', SearhListView.as_view(), name='search'),
    url(r'^search/(?P<id>\d+)/$', views.search_detail, name='search-detail'),
    url(r'^search/(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$', views.searchpreference, name='preference'),
    path('about/', views.about, name='about')
]
