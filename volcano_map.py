import folium
import pandas

volcanoes = pandas.read_csv("volcanoes.csv")
latitude_list = list(volcanoes["Latitude"])
longitude_list = list(volcanoes["Longitude"])
coordinate_list = []
map = folium.Map(location=[39.094632662122386, -96.4134528100795], zoom_start=4, 
                 tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=en", attr='Google', max_zoom=100)

for lat, long in zip(latitude_list, longitude_list):
    map.add_child(folium.Marker(location=[lat, long], popup="Hello", icon=folium.Icon(color='green')))








map.save("map.html")


