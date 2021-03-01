import dash
#from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import geopandas as gpd
from shapely import wkt

########### Define your variables
#df = pd.read_csv(r'https://raw.githubusercontent.com/kkane2425/energy-dash2/master/data/gdf_poly_shape.csv')
df = pd.read_csv("https://github.com/kkane2425/energy-dash2/blob/master/data/gdf_poly_shape.csv?raw=true")
#df = pd.read_csv('./data/gdf_poly_shape.csv')
df['geometry'] = df['str_geom'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df, geometry='geometry').set_index('loc_id')
gdf.set_crs('EPSG:3395', inplace=True)
geo_df = gdf.to_crs('EPSG:4326')


fig_data = px.choropleth(geo_df,
                   geojson=geo_df.geometry,
                   locations=geo_df.index,
                   color="TOTAL_SAVINGS",
                   color_continuous_scale="viridis",
                   range_color=(0, 2000),
                   animation_frame='heat_kwh_max'  ,
                    custom_data=['loc_name','TOTAL_SAVINGS','NONENG_HEAT_KWH_COST', 'NONENG_ELEC_KWH_COST', 'heat_needed_cumulative', 'elec_needed_cumulative',       'Cycle_ON_cumulative','Elev', 'ON_PCT'],
                    #hover_data={'NONENG_HEAT_KWH_COST':':.2f', # customize hover for column of y attribute
                    #         'NONENG_ELEC_KWH_COST':True, # add other column, default formatting
                    #         'heat_needed_cumulative':':.2f', # add other column, customized formatting
                             # data not in dataframe, default formatting
                    #         'elec_needed_cumulative': ':.2f',
                    #         'elec_needed_cumulative': ':.2f',
                    #                'Cycle_ON_cumulative': ':.0f',
                    #            'Elev': ':.0f',
                    #            'ON_PCT': ':.2f'                              
                     #       },
                   #scope="usa",
                    #projection="albers usa",
                   #projection=None,
                    projection="mercator",
                   )
fig_layout= go.Layout(title_text='Enginuity savings',
                   title_x=0.5,
                   width=1000,
                   height=1000)


#figure.update_layout(transition_duration=500)


energy_fig = go.Figure(data=fig_data, layout=fig_layout)

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
energy_fig.update_geos(fitbounds="locations", visible=False)


########### Initiate the app
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://github.com/kkane2425/energy-dash2/blob/master/assets/style.css']
#external_stylesheets = ['./assets/style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title="Enginuity"

########### Set up the layout
app.layout = html.Div(children=[
    html.H1('Enginuity Annual Savings'),
    dcc.Graph(
        id='graph',
        figure=energy_fig,
        style={'width': '90vh', 'height': '90vh'}
    ),
    #html.A('Code on Github', href=githublink),
    #html.Br(),
    #html.A('Data Source', href=sourceurl),
    ]
)

#app.run_server(mode='inline')
if __name__ == '__main__':
    app.run_server()
