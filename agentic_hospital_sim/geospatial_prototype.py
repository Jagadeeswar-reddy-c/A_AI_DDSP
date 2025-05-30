import folium
import pandas as pd

# Load the CSV data
df = pd.read_csv(r"C:\Users\user\Desktop\A_AI_DDSP\municipalities_with_coordinates.csv")  # Replace with your actual file name

# Set the initial map center (Germany's approximate location)
map_center = [51.1657, 10.4515]

# Create the map object centered on Germany with zoom level 6
m = folium.Map(location=map_center, zoom_start=6)

# Loop through the dataframe and add markers
for _, row in df.iterrows():
    if pd.notnull(row["latitude"]) and pd.notnull(row["longitude"]):  # Ensure valid coordinates
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=row["Gemeinde"],  # Display the municipality name
            tooltip=row["Gemeinde"]  # Show tooltip on hover
        ).add_to(m)

# Save the map to an HTML file
m.save("map.html")

print("Map has been saved to map.html")