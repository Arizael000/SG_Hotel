from django.urls import path
from .views import ListaRoom,CrearRoom,EliminarRoom,ModRoom,manageReservations,editarUsuario


urlpatterns = [
path('adminRoom',ListaRoom.as_view(), name='listarRoom'),
path('anadirRoom',CrearRoom.as_view(), name='anadirRoom'),
path('eliminarRoom/<int:pk>/', EliminarRoom.as_view(), name='eliminarRoom'),
path('modRoom/<int:pk>/', ModRoom.as_view(), name='modRoom'),
path('manageReservation/', manageReservations, name='manageReservation'),
path('editarUsuario/<int:user_id>/', editarUsuario.as_view(), name='editarUsuario'),

]