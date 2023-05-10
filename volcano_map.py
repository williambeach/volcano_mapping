import folium
import pandas


volcanoes = pandas.read_csv("volcanoes.csv")
latitudes = list(volcanoes["Latitude"])
longitudes = list(volcanoes["Longitude"])
elevation = list(volcanoes["Elevation (m)"])
names = list(volcanoes["Volcano Name"])
types = list(volcanoes["Type"])
world_data = open("world.json", "r", encoding='utf-8-sig').read()



def color_by_elev(elv):
    if elv < 0:
        return 'darkblue'
    elif elv >= 0 and elv <= 500:
        return 'blue'
    elif elv > 500 and elv <= 1000:
        return 'lightblue'
    elif elv > 1000 and elv <= 1500:
        return 'lightgreen'
    elif elv > 1500 and elv <= 2000:
        return 'green'
    elif elv > 2000 and elv <= 3000:
        return 'darkgreen'
    elif elv > 3000 and elv <= 4000:
        return 'lightred'
    elif elv > 4000 and elv <= 5000:
        return 'red'
    elif elv > 5000 and elv <= 6000:
        return 'darkred'
    elif elv > 6000 and elv <= 7000:
        return 'orange'
    


map = folium.Map(location=[39.094632662122386, -96.4134528100795], zoom_start=4, 
                 tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=en", attr='Google', max_zoom=100, prefer_canvas=True)




for lat, long, elv, name, type in zip(latitudes, longitudes, elevation, names, types):
    map.add_child(folium.Marker(location=[lat, long],
                  popup=folium.Popup(max_width=100, min_width=100,
                  html=f'<p style="text-align: center;"><a href="https://www.google.com/search?q={name}+volcano" target="_blank"><b>{name}</b></a></p>'
                       f'<p style="text-align: center;">{"Elevation: " + str(elv) + " m"}</p>'
                       f'<p style="text-align: center;">{"Type: " + type}</p>'), 
                  icon=folium.Icon(color=color_by_elev(elv))))



map.add_child(folium.GeoJson(data=world_data, 
                             style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 50000 else 
                                                       'orange' if x['properties']['POP2005'] < 100000 else 
                                                       'red' if x['properties']['POP2005'] < 250000 else 
                                                       'lightblue' if x['properties']['POP2005'] < 500000 else 
                                                       'blue' if x['properties']['POP2005'] < 1000000 else 
                                                       'darkblue' if x['properties']['POP2005'] < 5000000 else 
                                                       'purple' if x['properties']['POP2005'] < 10000000 else 
                                                       'pink' if x['properties']['POP2005'] < 100000000 else 
                                                       'green' if x['properties']['POP2005'] < 500000000 else
                                                       'beige' if x['properties']['POP2005'] < 1000000000 else
                                                       'lightgreen'}))

map.save("index.html")


