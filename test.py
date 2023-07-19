from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="city-to-coordinates")

city_name = input("Enter a city name:")

location = geolocator.geocode(city_name)

if location:
    latitude = location.latitude
    longitude = location.longitude
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Location not found.")
