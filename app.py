from flask import Flask, render_template, request, flash
import requests
import folium

url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
key = 'e5a233195edf76c4a042ea22ed0d937b'

def get_weather(place):
    data = requests.get(url.format(place, key))
    if data.status_code == 200:
        json_file = data.json()
        place = json_file['name']
        country = json_file['sys']['country']
        kelvin_temp = json_file['main']['temp']
        celcius_temp = kelvin_temp - 273.15
        celcius_temp = round(celcius_temp, 2)
        fahrenheit = (kelvin_temp - 273.15) * 9/5 + 32
        weather = json_file['weather'][0]['description']
        latitude = json_file['coord']['lat']
        longitude = json_file['coord']['lon']
        final = (place, country, celcius_temp, fahrenheit, weather, latitude, longitude)
        return final
    return None

app = Flask(__name__, static_folder='static')

app.secret_key = 'your_secret_key' #Secret key for flash messages  

@app.route('/', methods=["GET", "POST"])
def index():
    city = "Delhi"
    if request.method == "POST":
        city = request.form["InputCity"]

    weather = get_weather(city)

    # Checking if weather data is available for the location
    if weather is None:
        flash("Weather data not available for this location. Check the spelling or try another location.")
        city = "NA"
        temp = "NA"
        weather_description = "NA"
        country = "NA"
        latitude, longitude = 28.6139, 77.2090
    else:
        city, country, temp, _, weather_description, latitude, longitude = weather

    m = folium.Map(location=[latitude, longitude], zoom_start=10, tiles='Stamen Terrain',attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.')

    map_filename = "static/temp_map.html"
    m.save(map_filename)

    return render_template("index.html", place=city, temp=temp, weather=weather_description, map_filename=map_filename, country_code=country)


if __name__ == '__main__':
    app.run(debug=True)
