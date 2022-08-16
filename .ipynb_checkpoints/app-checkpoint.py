import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

from openpyxl import Workbook

########### Define your variables ######

tabtitle = 'EIEIO'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/dsbcintuit/306-agriculture-exports-dropdown'
# here's the list of possible columns to choose from.
list_of_columns =[
 'code',
 'state',
 'category',
 'Beef and veal',
 'Pork',
 'Hides and skins',
 'Other livestock products 1/',
 'Dairy products',
 'Broiler meat',
 'Other poultry products 2/',
 'Vegetables, fresh',
 'Vegetables, processed',
 'Fruits, fresh',
 'Fruits, processed',
 'Tree nuts',
 'Rice',
 'Wheat',
 'Corn',
 'Feeds and other feed grains 3/',
 'Grain products, processed',
 'Soybeans',
 'Soybean meal',
 'Vegetable oils',
 'Other oilseeds and products 4/',
 'Cotton',
 'Tobacco',
 'Other plant products 5/',
 'Total agricultural exports 6/',
 'Total animal products',
 'Total plant products']


########## Set up the chart

import pandas as pd
df = pd.read_excel('assets/state_detail_by_commodity_cy.xlsx')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('2020 Agricultural Exports, by State'),
    html.Div([
        html.Div([
                html.H6('Select a variable for analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='corn'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-cancan'),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Exports of {varname} in 2020'
    mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = "Millions USD"

    data=go.Choropleth(
        locations=df['code'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = df[varname].astype(float), # Data to be color-coded
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
