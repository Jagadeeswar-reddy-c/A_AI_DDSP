from mesa import Agent
import random

class HospitalAgent(Agent):
    def __init__(self, unique_id, model, location, offered_clusters, max_capacity_per_cluster):
        super().__init__(unique_id, model)
        self.location = location
        self.offered_clusters = offered_clusters
        self.max_capacity_per_cluster = max_capacity_per_cluster
        self.current_patients = []

    def step(self):
        pass  # Hospitals remain passive in this step cycle

class PatientAgent(Agent):
    def __init__(self, unique_id, model, region, age_group, service_cluster, severity_score, mobility_score, demand_probability):
        super().__init__(unique_id, model)
        self.region = region
        self.age_group = age_group
        self.service_cluster = service_cluster
        self.severity_score = severity_score
        self.mobility_score = mobility_score
        self.demand_probability = demand_probability
        self.assigned_hospital = None

    def step(self):
        if self.assigned_hospital is not None:
            return

        # Find the closest hospital that offers the required service cluster
        min_distance = float('inf')
        best_hospital = None

        for hospital in self.model.hospitals:
            if self.service_cluster not in hospital.offered_clusters:
                continue
            distance = self.model.distance_matrix.get((self.region, hospital.unique_id), float('inf'))
            if distance < min_distance:
                min_distance = distance
                best_hospital = hospital

        if best_hospital:
            self.model.add_patient_assignment(self, best_hospital)
            self.assigned_hospital = best_hospital
