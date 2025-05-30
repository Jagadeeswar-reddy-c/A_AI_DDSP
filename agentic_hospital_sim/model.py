from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import pandas as pd

from agents import HospitalAgent, PatientAgent

from geolocations_generator import geocode_german_municipalities


class HospitalPlanningModel(Model):
    def __init__(
        self,
        hospital_data_path,
        distance_matrix_path,
        coord_data_path,
        age_groups_path,
        width=50,
        height=50
    ):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.hospitals = []
        self.patients = []
        self.distance_matrix = {}

        self.hospital_df = pd.read_csv(hospital_data_path)
        self.distance_df = pd.read_csv(distance_matrix_path)
        self.coord_df = pd.read_csv(coord_data_path)
        self.age_groups_df = pd.read_csv(age_groups_path)

        # Clean column names
        self.coord_df.columns = [c.strip() for c in self.coord_df.columns]

        print(f"✅ - 1 Loaded {len(self.hospital_df)} hospitals, {len(self.distance_df)} distances, and {len(self.coord_df)} coordinates.")
        # Normalize Gemeinde names
        self.hospital_df['Adresse_Ort_Standort'] = self.hospital_df['Adresse_Ort_Standort'].str.strip().str.lower()
        self.coord_df['Gemeinde'] = self.coord_df['Gemeinde'].str.strip().str.lower()

        print(f"✅ - 2 Loaded {len(self.hospital_df)} hospitals, {len(self.distance_df)} distances, and {len(self.coord_df)} coordinates.")

        self.hospital_df = geocode_german_municipalities(self.hospital_df)
        
        print(f"✅ = 3 Loaded {len(self.hospital_df)} hospitals, {len(self.distance_df)} distances, and {len(self.coord_df)} coordinates.")


        # Merge coordinates into hospital_df
        # self.hospital_df = self.hospital_df.merge(
        #     self.coord_df[['Gemeinde', 'latitude', 'longitude']],
        #     left_on='Adresse_Ort_Standort',
        #     right_on='Gemeinde',
        #     how='left'
        # )

        print(f"✅ - 4 Loaded {len(self.hospital_df)} hospitals, {len(self.distance_df)} distances, and {len(self.coord_df)} coordinates.")

        # geocode_german_municipalities

        # Drop rows without coordinates
        self.hospital_df.dropna(subset=['latitude', 'longitude'], inplace=True)

        print(f"✅ Loaded {len(self.hospital_df)} hospitals, {len(self.distance_df)} distances, and {len(self.coord_df)} coordinates.")
        

        # Convert lat/long to grid positions
        # Normalize latitude and longitude to fit within the grid
        min_lat, max_lat = self.hospital_df['latitude'].min(), self.hospital_df['latitude'].max()
        min_lon, max_lon = self.hospital_df['longitude'].min(), self.hospital_df['longitude'].max()

        self.hospital_df['x'] = ((self.hospital_df['latitude'] - min_lat) / (max_lat - min_lat) * (self.grid.width - 1)).astype(int)
        self.hospital_df['y'] = ((self.hospital_df['longitude'] - min_lon) / (max_lon - min_lon) * (self.grid.height - 1)).astype(int)

        # Convert distance matrix into lookup dict
        for _, row in self.distance_df.iterrows():
            key = (row['patient_region'], f"hospital_{row['hospital_id']}")
            self.distance_matrix[key] = row['distance']

        self.create_agents()

    def create_agents(self):
        hospital_df = self.hospital_df
        distance_df = self.distance_df
        coord_df = self.coord_df
        age_codes = self.age_groups_df["code"].dropna().values.tolist()
        cluster_columns = [col for col in hospital_df.columns if col.isdigit()]

        print(f"Creating agents for {len(hospital_df)} hospitals and {len(distance_df)} patients...")
        # Create Hospital Agents
        for i, row in hospital_df.iterrows():
            hospital_id = i
            hospital_name = row["Adresse_Name"]
            x = row["x"]
            y = row["y"]

            offered_clusters = [col for col in cluster_columns if pd.notna(row[col]) and float(row[col]) > 0]
            max_capacity = {col: int(row[col]) for col in offered_clusters}

            hospital_agent = HospitalAgent(
                unique_id=f"hospital_{hospital_id}",
                model=self,
                name=hospital_name,
                location=(x, y),
                offered_clusters=offered_clusters,
                max_capacity_per_cluster=max_capacity
            )
            self.schedule.add(hospital_agent)
            self.grid.place_agent(hospital_agent, (x, y))

        # Create Patient Agents
        for i, row in distance_df.iterrows():
            region_name = row["patient_region"]
            hospital_id = row["hospital_id"]
            distance = float(row["distance"])

            region_coords = coord_df[coord_df["Gemeinde"] == region_name.lower()]
            if region_coords.empty or pd.isna(region_coords["latitude"].values[0]):
                continue

            lat = float(region_coords["latitude"].values[0])
            lon = float(region_coords["longitude"].values[0])
            x = int(lat * 10)
            y = int(lon * 10)

            # Clip to grid bounds
            x = max(0, min(x, self.grid.width - 1))
            y = max(0, min(y, self.grid.height - 1))

            age_code = age_codes[i % len(age_codes)]
            age_group = self.age_groups_df[self.age_groups_df["code"] == age_code]["age_group"].values[0]

            if hospital_id not in hospital_df.index:
                continue

            hospital_row = hospital_df.loc[hospital_id]
            available_clusters = [col for col in cluster_columns if pd.notna(hospital_row[col]) and float(hospital_row[col]) > 0]
            if not available_clusters:
                continue

            cluster = available_clusters[0]  # You may randomize or rotate this

            patient_agent = PatientAgent(
                unique_id=f"patient_{i}",
                model=self,
                age_group=age_group,
                region=region_name,
                cluster=cluster,
                location=(x, y),
                target_hospital_id=f"hospital_{hospital_id}",
                distance=distance
            )
            self.schedule.add(patient_agent)
            self.grid.place_agent(patient_agent, (x, y))

    def add_patient_assignment(self, patient, hospital):
        # print(f"Assigning {patient.unique_id} to {hospital.unique_id}")
        if hasattr(hospital, "current_patients"):
            hospital.current_patients.append(patient)
        else:
            hospital.current_patients = [patient]

    def step(self):
        self.schedule.step()
