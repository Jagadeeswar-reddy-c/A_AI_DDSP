from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from model import HospitalPlanningModel
from agents import HospitalAgent, PatientAgent

def agent_portrayal(agent):
    if isinstance(agent, HospitalAgent):
        return {
            "Shape": "circle",
            "Color": "red",
            "Filled": "true",
            "Layer": 1,
            "r": 0.8
        }
    elif isinstance(agent, PatientAgent):
        color = "blue" if agent.assigned_hospital else "gray"
        return {
            "Shape": "circle",
            "Color": color,
            "Filled": "true",
            "Layer": 0,
            "r": 0.5
        }

grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

server = ModularServer(
    HospitalPlanningModel,
    [grid],
    "Hospital Planning Simulation",
    {
        "hospital_data_path": "data/processed/Krankenha╠êuser in Deutschland (Krankenhausverzeichnis)/KHV_2022.csv",
        "distance_matrix_path": "data/distance_matrix.csv",
        "coord_data_path": "data/processed/DRG-Statistik (Patientenvolumen)/SA 40 2022.csv",
        "width": 50,
        "height": 50
    }
)

server.port = 8521
