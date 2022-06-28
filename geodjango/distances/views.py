from django.shortcuts import render, get_object_or_404
from . models import Medicao
from . forms import DistanceModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo , get_center_coordinates, get_zoom, get_ip_address
import folium


def calculo_distancia(request):
    #valores iniciais
    distancia = None
    destino   = None
    
    obj = get_object_or_404(Medicao, id=11)
    form = DistanceModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='distances')
    
    ip_ = get_ip_address(request)
    print(ip_)
    ip = '187.45.32.235'
    country, city, lat, lon = get_geo(ip)
    
    location = geolocator.geocode(city)
    
    #coordernadas localização
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)
    
    #folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
    #marcador localizacao
    folium.Marker([l_lat, l_lon], tooltip='Cique aqui para mais', popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)
    
    if form.is_valid():
        instance = form.save(commit=False)
        destino  = form.cleaned_data.get('destino')
        destino  = geolocator.geocode(destino)

        #coordernadas destino
        d_lat = destino.latitude
        d_lon = destino.longitude
        pointB = (d_lat, d_lon)
        #calculo distancia
        distancia = round(geodesic(pointA, pointB).km, 2)
        
        #folium map modificacao
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distancia))
        #marcador localizacao
        folium.Marker([l_lat, l_lon], tooltip='Cique aqui para mais', popup=city['city'],
                    icon=folium.Icon(color='purple')).add_to(m)
        #marcador destino
        folium.Marker([d_lat, d_lon], tooltip='Cique aqui para mais', popup=destino,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(m)
        
        #tracar linha localizacao e destino
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)
        
        instance.location  =  location
        instance.distancia = distancia
        instance.save()
        
    m = m._repr_html_()
    
    context = {
        'distancia' : distancia,
        'destino' : destino,
        'form' : form,
        'map' : m,
    }
    
    return render(request, 'distances/main.html', context)
