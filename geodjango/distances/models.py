from django.db import models

class Medicao(models.Model):
    location = models.CharField(max_length=200)
    destino  = models.CharField(max_length=200)
    distancia= models.DecimalField(max_digits=10, decimal_places=2)
    created  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Distância de {self.location} a {self.destino} é {self.distancia} km"
