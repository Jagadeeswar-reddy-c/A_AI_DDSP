from model import HospitalPlanningModel
import os

def main():
    base_path = r"C:\Users\user\Desktop\A_AI_DDSP\data\processed"  # Adjust to your actual root folder

    # Paths to required CSV files
    hospital_data_path = os.path.join(base_path, "Krankenha╠êuser in Deutschland (Krankenhausverzeichnis)", "KHV_2022.csv")
    patient_data_path = os.path.join(base_path, "DRG-Statistik (Patientenvolumen)", "SA 40 2022.csv")
    cluster_mapping_path = os.path.join(base_path, "DRG Fachabteilungcluster", "Sheet1.csv")
    forecast_data_path = os.path.join(base_path, "Bevo╠êlkerungsdaten (Destatis)", "Bevölkerung forecasts_VAR 02.csv")
    distance_matrix_path = os.path.join(base_path, "distance_matrix.csv")  # You must create or generate this
    coord_data_path = r"C:\Users\user\Desktop\A_AI_DDSP\municipalities_with_coordinates.csv"


    width = 50
    height = 50

    model = HospitalPlanningModel(
        hospital_data_path=hospital_data_path,
        # patient_data_path=patient_data_path,
        distance_matrix_path=distance_matrix_path,
        # forecast_data_path=forecast_data_path,
        coord_data_path=coord_data_path,
        # cluster_mapping_path=cluster_mapping_path,
        width=width,
        height=height
    )


    steps = 10
    for step in range(steps):
        print(f"\n=== Step {step + 1} ===")
        model.step()

if __name__ == "__main__":
    main()
