from django.urls import path
from analysisapp import views

urlpatterns = [
    # path('', views.splash),
    path('index', views.index),
    path('charts/', views.charts),
    path('charts2/', views.charts2),
    path('start', views.start),
    path('Maps', views.Maps),
    path('table', views.table),
    path('form', views.fileforms),

]