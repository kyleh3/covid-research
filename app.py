import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Import data from GitHub
df = pd.read_csv(r'./country-altmetric.csv')
print(df)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("COVID-19 Research Impact by Country"),
    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth(
            data_frame=df,
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')