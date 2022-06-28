from django.urls import path
from .views import calculo_distancia

app_name = 'distances'

urlpatterns = [
    path('', calculo_distancia, name='calculate-view')
]
