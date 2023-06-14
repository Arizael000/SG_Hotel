from django.urls import path
from .views import ListaReservacion, CrearReservacion, ModificarReservacion, EliminarReservacion,EliminarReservacionbyAdmin

urlpatterns = [
    path('crearReservaciones/<int:pk>/', CrearReservacion.as_view(), name='crearReservaciones'),
    path('modificarReservaciones/<int:pk>/', ModificarReservacion.as_view(), name='modificarReservaciones'),
    path('eliminarReservaciones/<int:pk>/', EliminarReservacion.as_view(), name='eliminarReservaaciones'),
    path('reservation/', ListaReservacion.as_view(), name='listarReservaciones'),
    path('EliminarReservacionbyAdmin/<int:pk>/', EliminarReservacionbyAdmin.as_view(), name='EliminarReservacionbyAdmin'),
    
    
]
