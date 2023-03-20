from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registros/", views.registros, name="registros"),
    path('create/', views.registros_create, name = "registros_create"),
    path('delete/<int:pk>', views.RegistrosDelete.as_view(), name = "registros_delete"),
    path('update/<int:pk>', views.registros_update, name = "registros_update"),
    path('search/', views.registros_search , name = "registros_search"),
    path('borrar_todo', views.registros_borrar_todo, name="registros_borrar_todo"),
    path('exportar', views.registros_exportar, name="registros_exportar"),
    path('importar', views.registros_importar, name="registros_importar"),
]
