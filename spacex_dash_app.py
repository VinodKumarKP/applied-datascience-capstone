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

launch_site_list = spacex_df['Launch Site'].unique()

dropdown_options = [{'label': 'ALL', 'value': 'ALL'}]
for ls in launch_site_list:
    dropdown_options.append({
        'label': ls, 'value': ls
    })

# print(dropdown_options)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=dropdown_options,
                                             value='ALL',
                                             placeholder="Launch Site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=max_payload, step=100,
                                                marks={x: str(x) for x in range(0, 11000, 1000)},
                                                value=[min_payload, max_payload],
                                                tooltip={"placement": "bottom", "always_visible": True}),
                                html.Br(),
                                html.Br(),
                                html.Div(id='payload_display',
                                         style={'color': 'blue', 'fontSize': 14, 'text-align': 'center'}),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='payload_display', component_property='children'),
              [Input(component_id='payload-slider', component_property='value')])
def get_min_payload(value):
    return f'You have selected min payload {value[0]} and max payload {value[1]}'


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        pie = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='Total Launches for All Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        pie = px.pie(data_frame=filtered_df,
                     names='class',
                     color='class',
                     title=f'Total Launch specific to {entered_site.upper()}')
    return pie


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_slider):
    print(entered_site, payload_slider)
    if entered_site == 'ALL':
        scatter_plot = px.scatter(spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_slider[0])
                                            & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])],
                                  x='class',
                                  y='Payload Mass (kg)',
                                  color="Booster Version Category",
                                  title='Total Launches for All Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        scatter_plot = px.scatter(filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_slider[0])
                                              & (filtered_df['Payload Mass (kg)'] <= payload_slider[1])],
                                  x='class',
                                  y='Payload Mass (kg)',
                                  color="Booster Version Category",
                                  title=f'Total Launch specific to {entered_site.upper()}')
    return scatter_plot


# Run the app
if __name__ == '__main__':
    app.run_server()
