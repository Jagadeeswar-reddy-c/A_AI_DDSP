import pandas as pd

# Step 1: Load DRG to Service Cluster mapping file
def load_drg_service_map(filepath):
    df = pd.read_csv(filepath)  # read csv file into DataFrame
    # Convert the mapping to a dictionary for quick lookup
    drg_map = dict(zip(df['Hauptdiagnose'], df['Ausland-unbekannt-ohne Angabe']))
    return drg_map

# Step 2: Function to get service cluster for a DRG code
def get_service_cluster(drg_code, drg_map):
    return drg_map.get(drg_code, 'Unknown')  # returns 'Unknown' if code not found

# Example Usage
if __name__ == "__main__":
    drg_map = load_drg_service_map(r'C:\Users\user\Desktop\A_AI_DDSP\data\processed\DRG-Statistik (Patientenvolumen)\hd3 aus_unbek.csv')
    test_drg = 'A01'
    print(f"DRG {test_drg} belongs to service cluster: {get_service_cluster(test_drg, drg_map)}")

#Step 1: Define DRG → Service Cluster mapping

#Step 2: Calculate demand normalized by population

#Step 3: Confirm Mesa as simulation platform

# Step 4: Visualize regional demand on a map using Folium

# Step 1: Load DRG counts and population data
def load_regional_data(drg_filepath, population_filepath):
    drg_df = pd.read_csv(drg_filepath)
    pop_df = pd.read_csv(population_filepath)

    # Sum across all regional columns to get total population per Hauptdiagnose
    pop_df["Population"] = pop_df.iloc[:, 2:].sum(axis=1)  # Exclude Hauptdiagnose column
    return drg_df, pop_df[["Hauptdiagnose", "Population"]]

# Step 2: Merge DRG counts with population by region
def calculate_demand_per_1000(drg_df, pop_df):
    # Merge on Hauptdiagnose column
    merged_df = drg_df.merge(pop_df, on="Hauptdiagnose", how="left")

    # Calculate demand per 1000 residents
    merged_df["Demand_per_1000"] = (merged_df["Ausland-unbekannt-ohne Angabe"] / merged_df["Population"]) * 1000
    return merged_df

# Example usage
if __name__ == "__main__":
    file1 = r'C:\Users\user\Desktop\A_AI_DDSP\data\processed\DRG-Statistik (Patientenvolumen)\hd3 aus_unbek.csv'
    file2 = r'C:\Users\user\Desktop\A_AI_DDSP\data\processed\DRG-Statistik (Patientenvolumen)\hd3 kreis BBTH 1216.csv'

    drg_df, pop_df = load_regional_data(file1, file2)
    demand_df = calculate_demand_per_1000(drg_df, pop_df)

    demand_df.to_csv("demandpopulationcluster.csv",index=False)
    
    print(demand_df.head())  # Preview first few rows


import folium
import pandas as pd

# Load CSV data
drg_df = pd.read_csv(r'C:\Users\user\Desktop\A_AI_DDSP\data\processed\DRG-Statistik (Patientenvolumen)\hd3 kreis BBTH 1216.csv')
demand_df = pd.read_csv(r'C:\Users\user\Desktop\A_AI_DDSP\demandpopulationcluster.csv')
locations_df = pd.read_csv(r'C:\Users\user\Desktop\A_AI_DDSP\municipalities_with_coordinates.csv')

# Transpose DRG data: Convert Regionalschlüssel from column headers to rows
drg_df_melted = drg_df.melt(id_vars=['Hauptdiagnose'], var_name='Regionalschlüssel', value_name='Count')

# Merge demand data using Hauptdiagnose
merged_df = drg_df_melted.merge(demand_df, on='Hauptdiagnose', how='left')


# Ensure both datasets have Regionalschlüssel as strings
merged_df["Regionalschlüssel"] = merged_df["Regionalschlüssel"].astype(str)
locations_df["Regionalschlüssel"] = locations_df["Regionalschlüssel"].astype(str)

# Now merge
map_data = merged_df.merge(locations_df, on='Regionalschlüssel', how='left')

# Remove rows where 'Regionalschlüssel' contains 'Unnamed: 0'
map_data = map_data[map_data["Regionalschlüssel"] != "Unnamed: 0"]

# Display first few rows to verify changes
print(map_data.head())

# Create a Folium map centered on Germany
m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)


# Plot markers for demand levels
for _, row in map_data.head(10000).iterrows():
    if pd.notnull(row["latitude"]) and pd.notnull(row["longitude"]):  # Ensure valid coordinates
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=row["Gemeinde"],  # Shows the municipality name when clicked
            tooltip=f"{row['Gemeinde']} - Demand: {row['Demand_per_1000']}",  # Shows demand info when hovered
            icon=folium.Icon(color="blue", icon="info-sign")  # Custom marker appearance
        ).add_to(m)


# Save the map
m.save('regional_demand_map.html')
print("Map saved as regional_demand_map.html")