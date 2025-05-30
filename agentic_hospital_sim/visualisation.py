# app.py
from flask import Flask
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import pandas as pd

# Import your model class
from model import HospitalPlanningModel

# Fake initial data for demo (replace with your real data load)
patients_data = [
    {'unique_id': 'p_1', 'region': 'Berlin-Mitte', 'age_group': '19-64', 'service_cluster': 'cardiology',
     'severity_score': 2.5, 'mobility_score': 0.8, 'demand_probability': 0.3},
    {'unique_id': 'p_2', 'region': 'Berlin-Pankow', 'age_group': '65-74', 'service_cluster': 'orthopedics',
     'severity_score': 1.2, 'mobility_score': 0.6, 'demand_probability': 0.2},
]

hospitals_data = [
    {'unique_id': 'h_1', 'location': (5, 5), 'offered_clusters': ['cardiology', 'orthopedics'],
     'max_capacity_per_cluster': {'cardiology': 200, 'orthopedics': 150}},
    {'unique_id': 'h_2', 'location': (10, 10), 'offered_clusters': ['cardiology'],
     'max_capacity_per_cluster': {'cardiology': 100}},
]

distance_matrix = {
    ('Berlin-Mitte', 'h_1'): 3.2,
    ('Berlin-Pankow', 'h_1'): 7.8,
    ('Berlin-Mitte', 'h_2'): 2.5,
    ('Berlin-Pankow', 'h_2'): 6.0,
}

planners_data = [{}]

# Grid size
WIDTH, HEIGHT = 20, 20

# Create Flask server
server = Flask(__name__)

# Create Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Initialize model globally
model = HospitalPlanningModel(patients_data, hospitals_data, planners_data, WIDTH, HEIGHT, distance_matrix)

# Layout with controls and outputs
app.layout = html.Div([
    html.H1("Hospital Planning Simulation Dashboard"),
    
    # Controls to change demand probabilities for regions
    html.Div([
        html.H3("Adjust Regional Demand Probability"),
        html.Label("Berlin-Mitte:"),
        dcc.Slider(id='demand-berlin-mitte', min=0, max=1, step=0.05, value=0.3,
                   marks={i/10: f'{i/10:.1f}' for i in range(0,11)}),
        html.Label("Berlin-Pankow:"),
        dcc.Slider(id='demand-berlin-pankow', min=0, max=1, step=0.05, value=0.2,
                   marks={i/10: f'{i/10:.1f}' for i in range(0,11)}),
        html.Button('Run Simulation Step', id='run-step', n_clicks=0),
    ], style={'width': '30%', 'float': 'left', 'padding': '20px'}),
    
    # Output plots
    html.Div([
        dcc.Graph(id='hospital-load-chart'),
        dcc.Graph(id='patient-assignment-chart')
    ], style={'width': '65%', 'float': 'right'}),
    
    html.Div(style={'clear': 'both'})
])


@app.callback(
    [Output('hospital-load-chart', 'figure'),
     Output('patient-assignment-chart', 'figure')],
    [Input('run-step', 'n_clicks')],
    [State('demand-berlin-mitte', 'value'),
     State('demand-berlin-pankow', 'value')]
)
def update_simulation(n_clicks, demand_mitte, demand_pankow):
    if n_clicks == 0:
        # Initial state
        pass
    else:
        # Update patients' demand_probability based on slider values
        for patient in model.patients:
            if patient.region == "Berlin-Mitte":
                patient.demand_probability = demand_mitte
            elif patient.region == "Berlin-Pankow":
                patient.demand_probability = demand_pankow

        # Run one simulation step
        model.step()

    # Collect hospital load (example: sum of patients assigned per hospital cluster)
    hospital_load = []
    for hosp in model.hospitals:
        total_load = sum(hosp.current_load_per_cluster.values()) if hasattr(hosp, 'current_load_per_cluster') else 0
        hospital_load.append({'hospital': hosp.unique_id, 'load': total_load})

    # Convert to DataFrame
    df_load = pd.DataFrame(hospital_load)

    # Bar chart of hospital loads
    load_fig = go.Figure(data=[
        go.Bar(x=df_load['hospital'], y=df_load['load'], name='Hospital Load')
    ])
    load_fig.update_layout(title='Hospital Load After Simulation Step',
                           yaxis_title='Load (Patients)')

    # Patient assignments by region (just counts by region)
    region_counts = {}
    for patient in model.patients:
        region_counts[patient.region] = region_counts.get(patient.region, 0) + 1

    df_patients = pd.DataFrame(list(region_counts.items()), columns=['Region', 'Patient Count'])

    assign_fig = go.Figure(data=[
        go.Bar(x=df_patients['Region'], y=df_patients['Patient Count'], name='Patients per Region')
    ])
    assign_fig.update_layout(title='Patient Distribution by Region')

    return load_fig, assign_fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
