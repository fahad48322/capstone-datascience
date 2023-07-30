import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
min_payload = int(spacex_df['Payload Mass (kg)'].min())
max_payload = int(spacex_df['Payload Mass (kg)'].max())

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'Site 1', 'value': 'site1'},
            {'label': 'Site 2', 'value': 'site2'},
            {'label': 'Site 3', 'value': 'site3'},
            {'label': 'Site 4', 'value': 'site4'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    # Task 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # Task 3: Add the Range Slider to select payload
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload],
        marks={str(payload): str(payload) for payload in range(min_payload, max_payload, 10000)}
    ),

    # Task 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2: Add a callback function to render the success-pie-chart based on selected site dropdown
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        pie_chart_data = spacex_df['class'].value_counts()
    else:
        pie_chart_data = spacex_df[spacex_df['Launch Site'] == selected_site]['class'].value_counts()
    
    # Create the pie chart figure
    fig = {
        'data': [
            {
                'type': 'pie',
                'labels': pie_chart_data.index,
                'values': pie_chart_data.values,
                'hole': 0.5,
                'marker': {'colors': ['#00cc96', '#EF553B']},
            }
        ],
        'layout': {
            'title': 'Total Successful Launches' if selected_site == 'ALL' else 'Success vs. Failed for {}'.format(selected_site),
        }
    }
    return fig
# Task 4: Add a callback function to render the success-payload-scatter-chart based on selected site and payload range
# Task 4: Add a callback function to render the success-payload-scatter-chart based on selected site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1]) &
                                (spacex_df['Launch Site'] == selected_site)]
    
    # Create the scatter chart figure
    fig = {
        'data': [
            {
                'x': filtered_df['Payload Mass (kg)'],
                'y': filtered_df['class'],
                'mode': 'markers',
                'marker': {
                    'color': filtered_df['Booster Version Category'],
                    'size': 10,
                    'colorscale': 'Viridis',
                    'showscale': True
                },
                'text': filtered_df['Launch Site']
            }
        ],
        'layout': {
            'title': 'Payload vs. Launch Success for {}'.format(selected_site),
            'xaxis': {'title': 'Payload Mass (kg)'},
            'yaxis': {'title': 'Launch Success'},
        }
    }
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

