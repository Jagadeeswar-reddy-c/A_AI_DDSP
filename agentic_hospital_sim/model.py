from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import pandas as pd
import random

from agents import HospitalAgent, PatientAgent

class HospitalPlanningModel(Model):
    def __init__(
        self,
        hospital_data_path,
        distance_matrix_path,
        coord_data_path,
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

        # Clean column names
        self.coord_df.columns = [c.strip() for c in self.coord_df.columns]

        # Normalize Gemeinde names
        self.hospital_df['Adresse_Ort_Standort'] = self.hospital_df['Adresse_Ort_Standort'].str.strip().str.lower()
        self.coord_df['Gemeinde'] = self.coord_df['Gemeinde'].str.strip().str.lower()

        # Merge coordinates into hospital_df
        self.hospital_df = self.hospital_df.merge(
            self.coord_df[['Gemeinde', 'latitude', 'longitude']],
            left_on='Adresse_Ort_Standort',
            right_on='Gemeinde',
            how='left'
        )

        # Drop rows without coordinates
        self.hospital_df.dropna(subset=['latitude', 'longitude'], inplace=True)

        # Convert lat/long to grid positions
        self.hospital_df['x'] = (self.hospital_df['latitude'].astype(float) * 10).astype(int)
        self.hospital_df['y'] = (self.hospital_df['longitude'].astype(float) * 10).astype(int)

        # Convert distance matrix into lookup dict
        for _, row in self.distance_df.iterrows():
            key = (row['patient_region'], f"hospital_{row['hospital_id']}")
            self.distance_matrix[key] = row['distance']

        self.create_agents()

    def create_agents(self):
        # Create hospital agents
        for i, row in self.hospital_df.iterrows():
            x = max(0, min(self.grid.width - 1, int(row['x'])))
            y = max(0, min(self.grid.height - 1, int(row['y'])))
            location = (x, y)
            offered_clusters = [c for c in ['0100', '0200', '0300'] if row.get(c, 0) > 0]  # Example clusters
            max_capacity = {c: random.randint(5, 15) for c in offered_clusters}

            hospital = HospitalAgent(
                unique_id=f"hospital_{i}",
                model=self,
                location=location,
                offered_clusters=offered_clusters,
                max_capacity_per_cluster=max_capacity
            )
            self.schedule.add(hospital)
            self.grid.place_agent(hospital, location)
            self.hospitals.append(hospital)

        # Create patient agents (example: one per row in distance_df)
        for i, row in self.distance_df.iterrows():
            region = row['patient_region']
            age_group = random.choice(['0-17', '18-64', '65+'])
            service_cluster = random.choice(['0100', '0200', '0300'])
            severity = random.uniform(0.1, 1.0)
            mobility = random.uniform(0.1, 1.0)
            demand_prob = random.uniform(0.5, 1.0)

            patient = PatientAgent(
                unique_id=f"patient_{i}",
                model=self,
                region=region,
                age_group=age_group,
                service_cluster=service_cluster,
                severity_score=severity,
                mobility_score=mobility,
                demand_probability=demand_prob
            )
            self.schedule.add(patient)
            self.patients.append(patient)
            self.grid.place_agent(patient, (random.randint(0, self.grid.width-1), random.randint(0, self.grid.height-1)))

    def add_patient_assignment(self, patient, hospital):
        print(f"Assigning {patient.unique_id} to {hospital.unique_id}")
        if hasattr(hospital, "current_patients"):
            hospital.current_patients.append(patient)
        else:
            hospital.current_patients = [patient]

    def step(self):
        self.schedule.step()
