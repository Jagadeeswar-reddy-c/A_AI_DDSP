import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def get_coordinates_from_placename(placename, geolocator):
    """
    Attempts to get the latitude and longitude for a given placename.
    Includes a retry mechanism for robust geocoding.
    """
    try:
        # Geocode with a user agent and a timeout
        location = geolocator.geocode(placename, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        print(f"Geocoding service timed out for: {placename}. Retrying...")
        time.sleep(2)  # Wait for 2 seconds before retrying
        return get_coordinates_from_placename(placename, geolocator)
    except GeocoderServiceError as e:
        print(f"Geocoding service error for: {placename} - {e}. Skipping.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred for {placename}: {e}. Skipping.")
        return None, None


def geocode_german_municipalities(file_path):
    """
    Reads the CSV file, extracts municipality names, and geocodes them
    to get latitude and longitude.
    """
    # try:
    #     # Read the CSV file
    #     df = pd.read_csv(file_path)
    # except FileNotFoundError:
    #     print(f"Error: The file '{file_path}' was not found.")
    #     return pd.DataFrame()
    # except Exception as e:
    #     print(f"Error reading the CSV file: {e}")
    #     return pd.DataFrame()

    df = file_path

    # Assuming 'Gemeinde' is the column with the municipality names
    # and 'Regionalschlüssel' is the unique identifier for the municipality/district
    # We will use 'Gemeinde' for geocoding, as it's more human-readable for the geocoder.
    # Adresse_Name,Adresse_Name_Standort,Adresse_Strasse_Standort
    if 'Adresse_Name_Standort' not in df.columns or 'Adresse_Strasse_Standort' not in df.columns:
        print("Error: 'Adresse_Name_Standort' or 'Adresse_Strasse_Standort' column not found in the CSV.")
        return pd.DataFrame()

    # Initialize Nominatim geocoder with a unique user agent
    # Replace 'your_app_name' with a meaningful name for your application
    geolocator = Nominatim(user_agent="my-german-pincode-geocoder")

    # Create new columns for latitude and longitude
    df['latitude'] = None
    df['longitude'] = None

    # Get unique municipalities to avoid redundant API calls
    # We'll use a dictionary to store already found coordinates to avoid re-querying
    geocoded_cache = {}

    for index, row in df.iterrows():
        municipality = row['Adresse_Name_Standort']
        regional_key = row['Adresse_Strasse_Standort']

        # Construct a more precise query for German locations
        # For example, "Flensburg, Stadt, Germany" or "Dithmarschen, Germany"
        # The 'Leer' column seems to be a simplified name, using 'Gemeinde' is better.
        query = f"{municipality}, {regional_key}, Germany"

        if query in geocoded_cache:
            lat, lon = geocoded_cache[query]
        else:
            # print(f"Geocoding: {query} (Regionalschlüssel: {regional_key})...")
            lat, lon = get_coordinates_from_placename(query, geolocator)
            geocoded_cache[query] = (lat, lon)
            time.sleep(1)  # Be polite to the Nominatim API (1 second delay per query)

        df.at[index, 'latitude'] = lat
        df.at[index, 'longitude'] = lon

    return df

# Specify the path to your CSV file
# file_path = r"C:\Users\user\Desktop\A_AI_DDSP\data\processed\DRG-Statistik (Patientenvolumen)\SA 40 2021.csv"

# # Run the geocoding process
# geocoded_df = geocode_german_municipalities(file_path)

# # Display the results
# if not geocoded_df.empty:
#     print("\nGeocoding complete. Here are the first few rows with coordinates:")
#     print(geocoded_df[['Regionalschlüssel', 'Gemeinde', 'latitude', 'longitude']].head())

#     # You can save the results to a new CSV file
#     output_file_path = "municipalities_with_coordinates.csv"
#     geocoded_df.to_csv(output_file_path, index=False)
#     print(f"\nResults saved to '{output_file_path}'")
# else:
#     print("\nNo data to display or process due to errors.")