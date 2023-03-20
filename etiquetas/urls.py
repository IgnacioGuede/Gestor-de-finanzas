from django.urls import path
from . import views

urlpatterns = [
    path('etiquetas/<int:ocultar>', views.etiquetas, name = "etiquetas"),
    path('create/', views.etiquetas_create, name = "create"),
    path('delete/<int:pk>', views.EtiquetasDelete.as_view(), name = "delete"),
    path('search/', views.etiquetas_search, name = "search"),
    path('update/<int:pk>', views.etiquetas_update, name = "update"),
]