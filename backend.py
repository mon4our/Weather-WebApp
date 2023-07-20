from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim
import folium
import geocoder
import pandas as pd

geolocator = Nominatim(user_agent="city-to-coordinates")

url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

key='e5a233195edf76c4a042ea22ed0d937b'

def get_weather(place):
    data=requests.get(url.format(place,key))
    if data:
        json_file=data.json()
        place=json_file['name']
        country=json_file['sys']['country']
        kelvin_temp=json_file['main']['temp']
        celcius_temp=int(kelvin_temp)-273.15
        celcius_temp=round(celcius_temp,2)
        fahrenheit=(int(kelvin_temp)-273.15)*9/5+32
        weather=json_file['weather'][0]['description']
        final=(place,country,celcius_temp,fahrenheit,weather)
        return final
    else:
        return None

def city_to_coordinates(city):
    location = geolocator.geocode(city)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    city="Delhi"
    if request.method=="POST":
        city=request.form["InputCity"]
        
    weather=get_weather(city)
    
    latitude, longitude = city_to_coordinates(city)
    if latitude is None or longitude is None:
        latitude, longitude = 28.6139, 77.2090

    m = folium.Map(location=[latitude, longitude], zoom_start=10, tiles='Stamen Terrain', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.')
    folium.Marker(location=[latitude, longitude], popup='User Location', icon=folium.Icon(color='blue')).add_to(m)

    # Save the map to a temporary HTML file
    map_filename = "static/temp_map.html"
    m.save(map_filename)
    
    return render_template("index.html",place=weather[0],temp=weather[2],weather=weather[4], map_filename=map_filename)

if __name__ == '__main__':
    app.run(debug=True)
