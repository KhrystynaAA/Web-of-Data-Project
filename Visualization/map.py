import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os


# Prompt for file path input
file_path = input("Please enter the file path: ")

# File processing
try:
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Get the coordinates of the capital
    capital_wkt = data["capitalWKT"].iloc[0]
    capital_label = data["capitalLabel"].iloc[0]
    population = int(data["population"].iloc[0])

    # Parse the WKT coordinates
    capital_coords = [
        float(coord) for coord in capital_wkt.replace("Point(", "").replace(")", "").split()
    ]

except FileNotFoundError:
    print(f"File at {file_path} not found.")
except KeyError as e:
    print(f"Column {e} not found in the file.")
except Exception as e:
    print(f"An error occurred: {e}")


# Create the map
mymap = folium.Map(location=capital_coords[::-1], zoom_start=10)

# Add a marker for the capital
folium.Marker(
    location=capital_coords[::-1],
    popup=f"{capital_label} (Population: {population})",
    tooltip="Capital"
).add_to(mymap)

# Process coordinates of historical sites
site_labels = data["siteLabels"].iloc[0].split(", ")
site_coordinates = data["siteCoordinates"].iloc[0].split(", ")

# Create a cluster for markers
marker_cluster = MarkerCluster().add_to(mymap)

# Add UNESCO heritage sites
for label, coord in zip(site_labels, site_coordinates):
    try:
        coord = coord.replace("Point(", "").replace(")", "")
        lon, lat = map(float, coord.split())
        folium.Marker(
            location=[lat, lon],
            popup=f"UNESCO Site: {label}",
            icon=folium.Icon(color="green", icon="ok-sign")
        ).add_to(marker_cluster)  
    except Exception as e:
        print(f"Error with site: {label}, coordinates: {coord}. Details: {e}")

# Save the map to an HTML file

current_dir = os.path.dirname(os.path.abspath(__file__))

output_file = os.path.join(current_dir, "map_with_results.html")

mymap.save(output_file)

print("The map has been saved to 'map_with_results.html'")
