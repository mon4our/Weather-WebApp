import requests
url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

key='e5a233195edf76c4a042ea22ed0d937b'


data=requests.get(url.format('mumbai',key))
print(data.json())