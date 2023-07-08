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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'site1'}, {'label': 'VAFB SLC-4E', 'value': 'site2'},{'label': 'KSC LC-39A', 'value': 'site3'},{'label': 'CCAFS SLC-40', 'value': 'site4'}],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),

                                
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df_all = spacex_df[spacex_df['class'] == 1]
        counted_outcome_0=len(spacex_df[spacex_df['Launch Site'] == "CCAFS LC-40"])
        counted_outcome_1=len(spacex_df[spacex_df['Launch Site'] == "VAFB SLC-4E"])
        counted_outcome_2=len(spacex_df[spacex_df['Launch Site'] == "KSC LC-39A"])
        counted_outcome_3=len(spacex_df[spacex_df['Launch Site'] == "CCAFS SLC-40"])

        plotted_df = [counted_outcome_0, counted_outcome_1, counted_outcome_2, counted_outcome_3]
        name_list=["CCAFS LC-40", "VAFB SLC-4E", "KSC LC-39A", "CCAFS SLC-40"]
        fig = px.pie(values=plotted_df, 
        names=name_list, 
        title='All Sites - Outcomes')
        return fig
    elif entered_site == 'site1':
        filtered_df_site1 = spacex_df[spacex_df['Launch Site'] == "CCAFS LC-40"] 
        counted_outcome_0=len(filtered_df_site1[filtered_df_site1['class'] == 0])
        counted_outcome_1=len(filtered_df_site1[filtered_df_site1['class'] == 1])
        plotted_df = [counted_outcome_0, counted_outcome_1]
        name_list=["Fail", "Success"]
        fig = px.pie(values=plotted_df, 
        names=name_list, 
        title='Site CCAFS LC-40 - Outcomes')
        return fig
    elif entered_site == 'site2':
        filtered_df_site2 = spacex_df[spacex_df['Launch Site'] == "VAFB SLC-4E"] 
        counted_outcome_0=len(filtered_df_site2[filtered_df_site2['class'] == 0])
        counted_outcome_1=len(filtered_df_site2[filtered_df_site2['class'] == 1])
        plotted_df = [counted_outcome_0, counted_outcome_1]
        name_list=["Fail", "Success"]
        fig = px.pie(values=plotted_df, 
        names=name_list,  
        title='Site VAFB SLC-4E - Outcomes')
        return fig
    elif entered_site == 'site3':
        filtered_df_site3 = spacex_df[spacex_df['Launch Site'] == "KSC LC-39A"] 
        counted_outcome_0=len(filtered_df_site3[filtered_df_site3['class'] == 0])
        counted_outcome_1=len(filtered_df_site3[filtered_df_site3['class'] == 1])
        plotted_df = [counted_outcome_0, counted_outcome_1]
        name_list=["Fail", "Success"]
        fig = px.pie(values=plotted_df, 
        names=name_list, 
        title='Site KSC LC-39A - Outcomes')
        return fig
    else:
    #if entered_site == 'site4':
        filtered_df_site4 = spacex_df[spacex_df['Launch Site'] == "CCAFS SLC-40"] 
        counted_outcome_0=len(filtered_df_site4[filtered_df_site4['class'] == 0])
        counted_outcome_1=len(filtered_df_site4[filtered_df_site4['class'] == 1])
        plotted_df = [counted_outcome_0, counted_outcome_1]
        name_list=["Fail", "Success"]
        fig = px.pie(values=plotted_df, 
        names=name_list, 
        title='Site CCAFS SLC-40 - Outcomes')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_from_slider):
    range_min = payload_from_slider[0]
    range_max = payload_from_slider[1]
    ranged_spacex_df=spacex_df[spacex_df['Payload Mass (kg)'] <=range_max]
    ranged_spacex_df=ranged_spacex_df[ranged_spacex_df['Payload Mass (kg)'] >=range_min]
    if entered_site == 'ALL':
        task4_fig = px.scatter(ranged_spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Outcome by Payload Mass')
        
    elif entered_site == 'site1':
        filtered_df_site1 = ranged_spacex_df[ranged_spacex_df['Launch Site'] == "CCAFS LC-40"]
        task4_fig = px.scatter(filtered_df_site1, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Outcome by Payload Mass')
    elif entered_site == 'site2':
        filtered_df_site2 = ranged_spacex_df[ranged_spacex_df['Launch Site'] == "VAFB SLC-4E"]
        task4_fig = px.scatter(filtered_df_site2, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Outcome by Payload Mass')    
    elif entered_site == 'site3':
        filtered_df_site3 = ranged_spacex_df[ranged_spacex_df['Launch Site'] == "KSC LC-39A"]
        task4_fig = px.scatter(filtered_df_site3, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Outcome by Payload Mass')
    elif entered_site == 'site4':
        filtered_df_site4 = ranged_spacex_df[ranged_spacex_df['Launch Site'] == "CCAFS SLC-40"]
        task4_fig = px.scatter(filtered_df_site4, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Outcome by Payload Mass')
    return task4_fig    


# Run the app
if __name__ == '__main__':
    app.run_server()
