import folium
import pandas
from branca.element import Template, MacroElement


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
    



map = folium.Map(location=[39.094632662122386, -96.4134528100795], zoom_start=4, tiles=None)

fg_volcano = folium.FeatureGroup(name="Volcanoes")
fg_population = folium.FeatureGroup(name="Population")

fg_volcano.add_to(map)
fg_population.add_to(map)

folium.TileLayer(name='World Map', tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=en", attr='Google', max_zoom=100,
                 location=[]).add_to(map)



for lat, long, elv, name, type in zip(latitudes, longitudes, elevation, names, types):
    fg_volcano.add_child(folium.Marker(location=[lat, long],
                  popup=folium.Popup(max_width=100, min_width=100,
                  html=f'<p style="text-align: center;"><a href="https://www.google.com/search?q={name}+volcano" target="_blank"><b>{name}</b></a></p>'
                       f'<p style="text-align: center;">{"Elevation: " + str(elv) + " m"}</p>'
                       f'<p style="text-align: center;">{"Type: " + type}</p>'), 
                  icon=folium.Icon(color=color_by_elev(elv))))



fg_population.add_child(folium.GeoJson(data=world_data, name="Population",
                             style_function=lambda x: {'fillColor':'blue' if x['properties']['POP2005'] < 100000000 else 
                                                       'darkgreen' if x['properties']['POP2005'] < 500000000 else
                                                       'red'}))


map.add_child(folium.LayerControl())

map.get_root().html.add_child(folium.Element("""
<head><link rel="icon" href="favicon.png" type="image/png"/></head>"""))


template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Volcano Map</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css"/>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; left: 20px; bottom: 20px;'>
     
<div class='legend-title' style='text-align:center'>Population</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:blue;opacity:0.7;'></span>< 100,000,000</li>
    <li><span style='background:green;opacity:0.7;'></span>< 500,000,000</li>
    <li><span style='background:red;opacity:0.7;'></span>>= 500,000,000</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)
fg_population.add_child(macro)
map.save("index.html")


