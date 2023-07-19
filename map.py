import pandas as pd
import folium
import geocoder

def get_user_location():
    g=geocoder.ip('me')
    
    if g.ok:
        latitude, longitude = g.latlng
        return latitude, longitude
    else:
        return None, None

user_latitude, user_longitude = get_user_location()

man_data = pd.DataFrame({
    "lat": user_latitude, 
    "lon": user_longitude, 
    "name": ["Man Marker"]
})

attribution = 'Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'

m = folium.Map(location=[user_latitude, user_longitude], zoom_start=10, tiles='Stamen Terrain', attr=attribution)

for _, row in man_data.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row["name"],
        icon=folium.CustomIcon('icons/user_location.png', icon_size=(40, 40))
    ).add_to(m)

m.save("map.html")

