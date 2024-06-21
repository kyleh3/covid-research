# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input   # pip install dash
import pandas as pd                                                     # pip install pandas
import plotly.express as px
import dash_mantine_components as dmc                                   # pip install dash-mantine-components==0.12.1

# Incorporate data
df = pd.read_csv(r'./org-allmetrics.csv')
df2 = pd.read_csv(r'./country-altmetric.csv')
print(df)
print(df2)

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(external_stylesheets=external_stylesheets)

# App layout
app.layout = dmc.Container([
    dmc.Title('Top Research Organizations for COVID-19: Publications, Citations, and Altmetric', color="blue", size="h3"),
    dmc.RadioGroup(
            [dmc.Radio(i, value=i) for i in ['Publications', 'Citations', 'Altmetric']],
            id='my-dmc-radio-item',
            value='Publications',
            size="sm"
        ),
    dmc.Grid([
        dmc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflow': 'auto'}, sort_action='native')
        ], span=6),
        dmc.Col([
            dcc.Graph(figure={}, id='graph-placeholder')
        ], span=6),
    ]),
html.Div([
    html.H1("COVID-19 Research Impact by Country"),
    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth(
            data_frame=df2,
            locations='country',  # This should match the column name in your DataFrame
            locationmode='country names',  # Set the location mode based on your data
            color='altmetric',  # This sets the color value based on your data
            hover_name='country',  # Hover information based on your data
            title='Global Reach of COVID-19 Research',
            height=700,
            width=1200
        )
    )
])

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Input(component_id='my-dmc-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='Country', y=col_chosen, histfunc='sum').update_xaxes(categoryorder='total descending')
    return fig

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')