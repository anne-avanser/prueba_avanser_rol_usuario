from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_usuario, name='registro_usuario'),
     path('roles/', views.registrar_rol, name='registro_rol'),
]
