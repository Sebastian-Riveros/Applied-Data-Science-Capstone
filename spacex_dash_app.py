# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {"label": "All Sites", "value": "ALL"},
            {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
            {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
            {"label": "KSC LC-39A", "value": "KSC LC-39A"},
            {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"}
        ],
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # Div for pie chart container
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Range Slider for Payload selection
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f"{i}" for i in range(0, 10001, 2000)},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # Scatter chart for Payload vs Class
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for pie chart
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f"Success vs Failure for site {entered_site}"
        )
    return fig

# Callback for scatter chart
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [Input(component_id="site-dropdown", component_property="value"),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    # Filtrate per Payload Range
    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= payload_range[0]) &
        (spacex_df["Payload Mass (kg)"] <= payload_range[1])
    ]

    if entered_site == "ALL":
        # Scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload and Success for All Sites',
        )
    else:
        # Filtrate per Selected Site
        site_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f"Correlation Between Payload and Success for site {entered_site}",
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




#html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app

