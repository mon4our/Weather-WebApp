from flask import Flask, render_template, request
import requests

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

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    city="Delhi"
    if request.method=="POST":
        city=request.form["InputCity"]
    weather=get_weather(city)
    return render_template("index.html",place=weather[0],temp=weather[2],weather=weather[4])

if __name__ == '__main__':
    app.run(debug=True)
