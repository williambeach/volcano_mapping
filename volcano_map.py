import folium
import pandas

volcanoes = pandas.read_csv("volcanoes.csv")
latitudes = list(volcanoes["Latitude"])
longitudes = list(volcanoes["Longitude"])
elevation = list(volcanoes["Elevation (m)"])
names = list(volcanoes["Volcano Name"])
types = list(volcanoes["Type"])
map = folium.Map(location=[39.094632662122386, -96.4134528100795], zoom_start=4, 
                 tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=en", attr='Google', max_zoom=50)




for lat, long, elv, name, type in zip(latitudes, longitudes, elevation, names, types):
    map.add_child(folium.Marker(location=[lat, long], 
                  popup=folium.Popup(max_width=100, min_width=100, 
                  html=f'<p style="text-align: center;"><b>{name}</b></p>'
                       f'<p style="text-align: center;">{"Elevation: " + str(elv) + " m"}</p>'
                       f'<p style="text-align: center;">{"Type: " + type}</p>'), 
                  icon=folium.Icon(color='green')))







map.save("index.html")


