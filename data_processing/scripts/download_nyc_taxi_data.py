import os
import urllib.request
import typer

# Define the base URL and the destination directory
base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
destination_dir = '../data/raw/nyctaxi'

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

def download_data(taxi_type: str, year: int, month: int):
    # Construct the filename and URL
    file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    url = f"{base_url}/{file_name}"
    destination_file = os.path.join(destination_dir, str(year), file_name)

    # Download the file
    print(f"Downloading {file_name}...")
    urllib.request.urlretrieve(url, destination_file)
    print(f"Downloaded {file_name} to {destination_file}")

def parse_comma_separated_list(value: str):
    return [item.strip() for item in value.split(",")]

def main(
    taxi_types: str = typer.Option('yellow,green,fhv,fhvhv', help="Comma-separated list of taxi types to download data for."),
    years: str = typer.Option('2023', help="Comma-separated list of years to download data for."),
    months: str = typer.Option("1,2,3,4,5,6,7,8,9,10,11,12", help="Comma-separated list of months to download data for.")
):
    # Parse the comma-separated values into lists
    taxi_types_list = parse_comma_separated_list(taxi_types)
    years_list = [int(year) for year in parse_comma_separated_list(years)]
    months_list = [int(month) for month in parse_comma_separated_list(months)]

    # Download data for each combination of taxi type, year, and month
    for taxi_type in taxi_types_list:
        for year in years_list:
            for month in months_list:
                try:
                    download_data(taxi_type, year, month)
                except Exception as e:
                    print(f"Failed to download data for {taxi_type} {year}-{month:02d}: {e}")
    print('Download completed!')

if __name__ == "__main__":
    typer.run(main)
