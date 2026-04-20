import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(r'D:\project1\Economic Recession Impact on Automobile Sales\automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # الجزء المثبت في الأعلى (Sticky Header)
    html.Div([
        # TASK 2.1: Title
        html.H1(
            "Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24, 'margin-bottom': '10px'}
        ),
        
        # TASK 2.2: Dropdowns Container
        html.Div([
            html.Div([
                html.Label("Select Statistics:", style={'margin-right': '10px', 'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='dropdown-statistics', 
                    options=dropdown_options,
                    placeholder='Select a report type',
                    value='Select Statistics',
                    style={'width': '100%'}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),
            
            html.Div([
                html.Label("Select Year:", style={'margin-right': '10px', 'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='select-year',
                    options=[{'label': i, 'value': i} for i in year_list],
                    placeholder='Select-year',
                    value='Select-year',
                    style={'width': '100%'}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'})
        ], style={'textAlign': 'center'})
        
    ], style={
        'position': 'sticky', 
        'top': '0', 
        'zIndex': '1000', 
        'backgroundColor': '#f9f9f9', 
        'padding': '15px',
        'borderBottom': '2px solid #503D36',
        'boxShadow': '0px 2px 5px rgba(0,0,0,0.1)'
    }),

    # TASK 2.3: Output display (الذي يتحرك بالاسكرول ومرتب كـ Grid)
    html.Div([
        html.Div(id='output-container', className='chart-grid', 
                 style={'display': 'flex', 'flex-wrap': 'wrap', 'justifyContent': 'center'}),
    ], style={'padding': '20px'})
])

# TASK 2.4: Creating Callbacks
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Sales over Recession Period"))

        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                 
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Sales by Vehicle Type"))
        
        # Plot 3: Pie chart for advertising expenditure
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title="Ad Expenditure by Vehicle Type"))

        # Plot 4: Effect of unemployment rate
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', title='Unemployment Rate vs Sales'))

        # Return as 2x2 Grid
        return [
            html.Div(children=R_chart1, style={'width': '50%', 'display': 'inline-block'}),
            html.Div(children=R_chart2, style={'width': '50%', 'display': 'inline-block'}),
            html.Div(children=R_chart3, style={'width': '50%', 'display': 'inline-block'}),
            html.Div(children=R_chart4, style={'width': '50%', 'display': 'inline-block'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == int(input_year)]
                              
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Sales Trend'))
            
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales', title='Monthly Sales in {}'.format(input_year)))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title='Avg Sold by Type in {}'.format(input_year)))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Ad Spend in {}'.format(input_year)))

        # Return as 2x2 Grid
        return [
            html.Div(children=Y_chart1, style={'width': '50%', 'display': 'inline-block'}),
            html.Div(children=Y_chart2, style={'width': '50%', 'display': 'inline-block'}),
            html.Div(children=Y_chart3, style={'width': '50%', 'display': 'inline-block'}),
            html.Div(children=Y_chart4, style={'width': '50%', 'display': 'inline-block'})
        ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)