from django.urls import path
from . import views

app_name = 'tsp'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_city/', views.add_city, name='add_city'),
    path('add_distance/', views.add_distance, name='add_distance'),
    path('solve/', views.solve_tsp, name='solve'),
] 