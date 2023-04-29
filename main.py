# Import necessary libraries
import json
import geopandas
import requests
import pandas
import folium
from folium import plugins
import matplotlib.pyplot as plt
import time

with open("my_api_key.txt", "r") as secret:
    my_api_key = secret.read()

# Enter API key from airlabs.co account.
api_key = my_api_key

#  TEST TEXT

# url variable store url.
url = "https://airlabs.co/api/v9/flights?"

# GET all flight data from airlabs.co.
# r = requests.get(url+"api_key="+api_key)


def create_flight_heatmap():
    date = time.localtime()


    # Store the data in a JSON file.
    filename = "flights"
    file = filename+".json"
    # f = open(f'{file}', 'wb')
    # f.write(r.content)
    # f.close()

    # Call the JSON file to extract the plane locations into a python dictionary.
    # The latitudes and longitudes are stored in separate arrays with lat and lng keys.
    f = open(file, "r")
    json_file = json.load(f)
    flights = {'lat': [], 'lng': [], 'dir': []}
    for row in json_file["response"]:
        available_columns = row.keys()
        if "status" in available_columns:
            if row["status"] == "en-route":
                flights['dir'].append((row['dir']))
                flights['lat'].append((row['lat']))
                flights['lng'].append((row['lng']))
    f.close()

    # Import the python dictionary into pandas DataFrame.
    df = pandas.DataFrame(data=flights)

    # Turn the DataFrame into GeoDataFrame which enables them to lay their positions on a map.
    geo_df = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lng, df.lat))

    # # Plot the data on a static map.
    # world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    #
    # fig, ax = plt.subplots(figsize=(24,18))
    # world.plot(ax=ax, alpha=0.4, color='grey')
    # geo_df.plot( ax=ax, legend=True)
    # plt.title('Planes')

    # Preparing a heat map.
    map = folium.Map(location = [30,15], tiles='Cartodb dark_matter', zoom_start = 2)

    # Use the data from the GeoDataFrame.
    flight_data = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry ]

    # Apply the data on a heatmap with some customization on symbology.
    plugins.HeatMap(flight_data, blur=10, radius=11, name="Flight Density").add_to(map)


    # Tools for map users.
    folium.LayerControl().add_to(map)
    folium.plugins.Fullscreen().add_to(map)
    folium.plugins.MousePosition().add_to(map)
    # folium.plugins.Geocoder().add_to(map)
    # folium.plugins.MiniMap().add_to(map)
    # folium.plugins.LocateControl().add_to(map)

    system_time = [date[3], date[4], date[5]]
    for i in range(len(system_time)):
        if system_time[i] <= 9:
            system_time[i] = "0"+str(system_time[i])
    hour, minute, second = system_time
    date_string = f"{date[0]}/{date[1]}/{date[2]} - {hour}:{minute}:{second}"
    title = f"Global Flight Density Map"
    title_html = f'<h3 align="center" style="font-size:16px"><b>{title}</b></h3>' \
                 f'<p align="center" style="font-size:16px">{date_string}</p>'
    map.get_root().html.add_child(folium.Element(title_html))

    map.save("map.html")


create_flight_heatmap()
