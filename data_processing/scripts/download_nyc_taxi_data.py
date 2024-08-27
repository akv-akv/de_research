import os
import urllib.request

# Define the base URL and the destination directory
base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
destination_dir = 'data/raw/nyctaxi'

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

def download_data(taxi_type, year, month):
    # Construct the filename and URL
    file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    url = f"{base_url}/{file_name}"
    destination_file = os.path.join(destination_dir, str(year), file_name)

    # Download the file
    print(f"Downloading {file_name}...")
    urllib.request.urlretrieve(url, destination_file)
    print(f"Downloaded {file_name} to {destination_file}")

# Define the taxi types, years, and months to download
taxi_types = [
    #"yellow",
    #"green",
    #"fhv",
    'fhvhv'
]
years = [
    #2019,2020,2021,2022,
    2023
]
months = range(4, 13)  # January to December

# Download data for each combination of taxi type, year, and month
for taxi_type in taxi_types:
    for year in years:
        for month in months:
            try:
                download_data(taxi_type, year, month)
            except Exception as e:
                print(f"Failed to download data for {taxi_type} {year}-{month:02d}: {e}")

print('Download completed!')
