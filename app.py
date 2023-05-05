import csv
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim

# Load shapefiles & remove 'National' polygon
msa_gdf = gpd.read_file('./msa.shp')
dma_gdf = gpd.read_file('./dma.shp')
dma_gdf = dma_gdf[dma_gdf['Key'] != '000']


# Function to find MSA for a given point
def find_msa(point):
    msa = msa_gdf[msa_gdf.geometry.contains(point)]
    if not msa.empty:
        return msa['NAME'].values[0]
    else:
        return None

# Function to find DMA for a given point
def find_dma(point):
    dma = dma_gdf[dma_gdf.geometry.contains(point)]
    if not dma.empty:
        return dma['NAME'].values[0]
    else:
        return None

# Function to get the latitude and longitude for a given city name
def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="msa_dma_finder", timeout=10)
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

input_csv = 'cities.csv'  # Replace with your input CSV filename
output_csv = 'results.csv'  # Replace with your desired output CSV filename

with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(['City', 'MSA', 'DMA'])  # Write the header row

    for row in reader:
        city_name = row[0]
        latitude, longitude = get_coordinates(city_name)

        if latitude and longitude:
            city_point = Point(longitude, latitude)
            msa = find_msa(city_point)
            dma = find_dma(city_point)

            writer.writerow([city_name, msa, dma])
        else:
            print(f"Couldn't find coordinates for the city '{city_name}'. Skipping.")