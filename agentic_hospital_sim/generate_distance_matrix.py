import pandas as pd
import numpy as np
from math import radians, cos, sin, sqrt, atan2

# === Haversine Distance Function ===
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# === Load Gemeinde Coordinates ===
gemeinde_coords = pd.read_csv(r"C:\Users\user\Desktop\A_AI_DDSP\municipalities_with_coordinates.csv")
gemeinde_coords = gemeinde_coords[['Gemeinde', 'latitude', 'longitude']]
gemeinde_coords = gemeinde_coords.dropna().drop_duplicates('Gemeinde')
gemeinde_to_coords = gemeinde_coords.set_index('Gemeinde')[['latitude', 'longitude']].to_dict('index')

# === Load Hospital Data ===
hospital_df = pd.read_csv(r"C:\Users\user\Desktop\A_AI_DDSP\data\processed\Krankenha╠êuser in Deutschland (Krankenhausverzeichnis)\KHV_2022.csv")
hospital_df['hospital_id'] = hospital_df.index  # Add ID if missing
# hospital_df = hospital_df[hospital_df['Gemeinde'].notnull()]
# hospital_df['Gemeinde'] = hospital_df['Gemeinde'].astype(str).str.strip()
# New:
hospital_df = hospital_df[hospital_df['Adresse_Ort_Standort'].notnull()]
hospital_df['Gemeinde'] = hospital_df['Adresse_Ort_Standort'].astype(str).str.strip()


# === Load Patient Region Data ===
region_df = pd.read_csv(r"C:\Users\user\Desktop\A_AI_DDSP\data\processed\DRG-Statistik (Patientenvolumen)\SA 40 2022.csv")
region_df = region_df[region_df['Gemeinde'].notnull()]
region_df['Gemeinde'] = region_df['Gemeinde'].str.strip()

# === Compute Distance Matrix ===
records = []
for reg_name in region_df['Gemeinde'].unique():
    if reg_name not in gemeinde_to_coords:
        continue
    reg_coords = gemeinde_to_coords[reg_name]
    for _, hosp in hospital_df.iterrows():
        hosp_name = hosp['Gemeinde']
        if hosp_name not in gemeinde_to_coords:
            continue
        hosp_coords = gemeinde_to_coords[hosp_name]
        dist_km = haversine(reg_coords['latitude'], reg_coords['longitude'],
                            hosp_coords['latitude'], hosp_coords['longitude'])
        records.append({
            'patient_region': reg_name,
            'hospital_id': hosp['hospital_id'],
            'distance': round(dist_km, 2)
        })

print(f"✅ Computed {len(records)} distances between {len(region_df['Gemeinde'].unique())} regions and {len(hospital_df)} hospitals.")
# === Save Output ===
distance_df = pd.DataFrame(records)
distance_df.to_csv(r"C:\Users\user\Desktop\A_AI_DDSP\data\processed\distance_matrix.csv", index=False)
print("✅ Distance matrix with real coordinates saved.")
