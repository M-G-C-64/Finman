from django.urls import path
from . import views

urlpatterns = [path('', views.ext, name='ext'),
               path('default', views.default, name='default'),
               path('graphs', views.graphs, name='graphs'),
               path('sql_upload', views.sql_upload, name='sql_upload')]
