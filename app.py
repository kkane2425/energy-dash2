import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objs as go
from shapely import wkt

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://github.com/kkane2425/energy-dash2/blob/master/assets/style.css']
#external_stylesheets = ['C:/Users/Owner/Documents/GitHub/energy-dash/assets']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title="Enginuity"

########### Define your variables
df = pd.read_csv("https://github.com/kkane2425/energy-dash2/blob/master/data/gdf_poly_shape.csv?raw=true")
#df=geo_df
df['geometry'] = df['str_geom'].apply(wkt.loads)
geo_df = gpd.GeoDataFrame(df, geometry='geometry').set_index('loc_id')
geo_df.set_crs('EPSG:4326', inplace=True)
geo_df = geo_df.to_crs('EPSG:4326')

#available_indicators = df['Indicator Name'].unique()
available_indicators= ['TOTAL_SAVINGS', 'ON_PCT', 'Cycle_ON_cumulative', 'ON_HRS_cumulative',
    'heat_needed_cumulative','elec_needed_cumulative', 'heat_produced_cumulative',
    'elec_produced_cumulative', 'unmet_heat_needed_cumulative',
    'unmet_elec_needed_cumulative', 'wasted_heat_cumulative',
    'Elev',
    'ENG_ELEC_KWH_COST', 'ENG_HEAT_KWH_COST', 'NONENG_HEAT_KWH_COST','NONENG_ELEC_KWH_COST', 
    'heat_kwh_min', 'heat_kwh_max', 'elec_kwh_max', 'water_heater_max_kwh']



available_kwh=[10,16]

# initialize axes
xaxis_column_name = 'TOTAL_SAVINGS'
yaxis_column_name = 'Cycle_ON_cumulative'
kwh_value = 10

#app.layout = html.Div(dcc.Dropdown(options=[...]), className="dash-bootstrap")

app.layout = html.Div([
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-dropdown-component',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=xaxis_column_name,
                clearable=False,
            )
        ], 
            style={'width': '32%', 'display': 'inline-block','color':'darkgray'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value = yaxis_column_name,
                clearable=False,

            )
        ], 
            style={'width': '32%', 'display': 'inline-block','color':'darkgray'}),
        
        html.Div([
            dcc.RadioItems(
                id='crossfilter-kwh-type',
                options=[{'label': 'max heat kwh='+str(i), 'value': i} for i in available_kwh],
                value=available_kwh[0],
                labelStyle={'display': 'inline-block'}
            )
        ], 
            style={'width': '32%', 'float': 'right', 'display': 'inline-block'}),


    ], 
       style={
        'width': '99%',
        'display': 'inline-block',
        'borderBottom': 'thin lightgrey solid',
        #  'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '5px 5px 5px 5px'}
    ),


        html.Div([
            dcc.Graph(id='x-time-series')
            #dcc.Graph(id='y-time-series'),
            ], style={'float': 'left', 'display': 'inline-block', 'width': '45%', 'padding': '5px 5px 5px 5px'}),    

        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'MYRTLE BEACH AFB'}]}
            )
        ], style={'width': '45%','float': 'right', 'display': 'inline-block', 'padding': '5px 5px 5px 5px'}),        

    #html.Div(dcc.Slider(
    #    id='crossfilter-kwh--slider',
    #    min=df['heat_kwh_max'].min(),
    #    max=df['heat_kwh_max'].max(),
    #    value=df['heat_kwh_max'].max(),
    #    marks={str(kwh): str(kwh) for kwh in df['heat_kwh_max'].unique()},
    #    step=None
    #), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('xaxis-dropdown-component', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-kwh-type', 'value'),
     #dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     #dash.dependencies.Input('crossfilter-kwh--slider', 'value')
    ])
def update_graph(xaxis_column_name, yaxis_column_name,
                 #xaxis_type, yaxis_type,
                 kwh_value):
    dff = df[df['heat_kwh_max'] == kwh_value]

    fig = go.Figure()
    fig.add_trace(go.Histogram2dContour(
        x = dff[xaxis_column_name],
        y = dff[yaxis_column_name],
        colorscale = 'Blues_r',
        reversescale = True,
        xaxis = 'x',
        yaxis = 'y',
        hoverinfo='skip'
        ))
    fig.add_trace(go.Scatter(
        x = dff[xaxis_column_name],
        y = dff[yaxis_column_name],
        xaxis = 'x',
        yaxis = 'y',
        mode = 'markers',
        marker = dict(
            color = 'rgba(0,0,0,0.3)',
            size = 3
        ),
        text=dff['loc_name'],
        hovertemplate=
        "<b>%{text}</b><br><br>" + xaxis_column_name +
        ": %{x:,.2f}<br>" + yaxis_column_name +
        ": %{y:,.2f}<br>" +
        "<extra></extra>",

        ))
    fig.add_trace(go.Histogram(
        y = dff[yaxis_column_name],
        xaxis = 'x2',
        marker = dict(
            color = 'rgba(0,0,0,1)'
        )
        ))
    fig.add_trace(go.Histogram(
        x = dff[xaxis_column_name],
        yaxis = 'y2',
        marker = dict(
            color = 'rgba(0,0,0,1)'
        )
        ))

    fig.update_traces(customdata=dff['loc_name'])

    fig.update_layout(
    autosize = False,
    xaxis = dict(
        zeroline = False,
        domain = [0,0.8],
        showgrid = False
        ),
    yaxis = dict(
        zeroline = False,
        domain = [0,0.8],
        showgrid = False
        ),
    xaxis2 = dict(
        zeroline = False,
        domain = [0.85,1],
        showgrid = False
        ),
    yaxis2 = dict(
        zeroline = False,
        domain = [0.85,1],
        showgrid = False
        ),
    xaxis_title=xaxis_column_name,
    yaxis_title=yaxis_column_name,    
    title='Location density plot',
    #height = 600,
    #width = 600,
    bargap = 0,
    hovermode = 'closest',
    #margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
    showlegend = False
    )


    return fig


def create_us_map(gdff, xaxis_column_name):    
    fig_data = px.choropleth(gdff,
                   geojson=gdff.geometry,
                   locations=gdff.index,
                   #color="TOTAL_SAVINGS",
                   color=xaxis_column_name,
                   color_continuous_scale="viridis",
                   range_color=(gdff[xaxis_column_name].quantile(0.05), gdff[xaxis_column_name].quantile(0.95)),
                   #animation_frame='heat_kwh_max'  ,
                    custom_data=['loc_name','TOTAL_SAVINGS','NONENG_HEAT_KWH_COST', 'NONENG_ELEC_KWH_COST', 'heat_needed_cumulative', 'elec_needed_cumulative',       'Cycle_ON_cumulative','Elev', 'ON_PCT'],
                        projection="mercator",
                       )
    fig_layout= go.Layout(title_text=xaxis_column_name,
                       title_x=0.5,
                       #width=1000,
                       #height=500
                         )

    
    energy_fig = go.Figure(data=fig_data, layout=fig_layout)
    energy_fig.update_geos(#fitbounds="locations", 
                        visible=False,
                            # center=dict(lon=95, lat=30),
                        lataxis_range=[25,50], 
                        lonaxis_range=[-125, -65]
                )

    energy_fig.update_traces(
        hovertemplate="<br>".join([
            "%{customdata[0]}",
            "Annual Savings: %{customdata[1]:$,.0f}",
            "Mkt Heat $/kwh: %{customdata[2]:.3f}",
            "Mkt Elec $/kwh: %{customdata[3]:.3f}",
            "Annual heat kwh needed: %{customdata[4]:,.0f}",
            "Annual elec kwh needed: %{customdata[5]:,.0f}",
            "Annual cycles: %{customdata[6]:,.0f}",
            "Percent ON: %{customdata[8]:%.0f}",
        ])
    )

    #energy_fig.update_layout(transition_duration=500)
    #fig = px.scatter(dff, x=xaxis_column_name, y=yaxis_column_name)
    #fig.update_traces(mode='lines+markers')
    #fig.update_xaxes(showgrid=False)
    #fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #                   xref='paper', yref='paper', showarrow=False, align='left',
    #                   bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    #fig.update_layout(height=500, margin={'l': 20, 'b': 10, 'r': 10, 't': 10})

    return energy_fig

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [#dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('xaxis-dropdown-component', 'value'),
     dash.dependencies.Input('crossfilter-kwh-type', 'value'),
     #dash.dependencies.Input('crossfilter-xaxis-type', 'value')
    ])
#def update_y_timeseries(hoverData, xaxis_column_name):
def update_y_timeseries(xaxis_column_name, kwh_type):
    #loc_name = hoverData['points'][0]['customdata']
    gdff = geo_df[geo_df['heat_kwh_max'] == kwh_type]
    #dff = dff[dff['Indicator Name'] == xaxis_column_name]
    #title = '<b>{}</b><br>{}'.format(loc_name, xaxis_column_name)
    return create_us_map(gdff, xaxis_column_name)



#app.run_server(mode='inline')
if __name__ == '__main__':
    app.run_server()
