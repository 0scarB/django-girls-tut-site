from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.maze_list, name='maze_list'),
]
