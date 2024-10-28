from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_daq as daq

housingDataset = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/newPH_housing.csv'
earthquakeDataset = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/earthquake.csv'
introParagraph = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec at pharetra ante. Vestibulum ut sapien id nibh efficitur pulvinar id in leo. Nullam aliquet, velit at fermentum dictum, neque massa vehicula velit, ac scelerisque nunc mi quis eros. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris finibus volutpat congue. Cras ac gravida dolor. Praesent sed accumsan orci. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Ut porttitor nibh sem, vitae varius orci efficitur eget. Proin tincidunt, nisi et molestie congue, nisi nibh dignissim risus, in malesuada erat massa eu dolor. Vestibulum a quam at libero scelerisque tempus.'
regionOptions = [
    {'label': 'Region I - Ilocos Region', 'value': 'Region I'},
    {'label': 'Region II - Cagayan Valley', 'value': 'Region II'},
    {'label': 'Region III - Central Luzon', 'value': 'Region III'},
    {'label': 'Region IV-A - CALABARZON', 'value': 'Region IV-A'},
    {'label': 'Region IV-B MIMAROPA', 'value': 'Region IV-B'},
    {'label': 'Region V - Bicol Region', 'value': 'Region V'},
    {'label': 'Region VI - Western Visayas', 'value': 'Region VI'},
    {'label': 'Region VII - Central Visayas', 'value': 'Region VII'},
    {'label': 'Region VIII - Eastern Visayas', 'value': 'Region VIII'},
    {'label': 'Region IX - Zamboanga Peninsula', 'value': 'Region IX'},
    {'label': 'Region X - Northern Mindanao', 'value': 'Region X'},
    {'label': 'Region XI - Davao Region', 'value': 'Region XI'},
    {'label': 'Region XII - SOCCSKSARGEN', 'value': 'Region XII'},
    {'label': 'Region XIII - Caraga', 'value': 'Region XIII'},
    {'label': 'NCR - National Capital Region', 'value': 'NCR'},
    {'label': 'CAR - Cordillera Administrative Region', 'value': 'CAR'},
    {'label': 'BARMM - Bangsamoro Autonomous Region in Muslim Mindanao', 'value': 'BARMM'},
    {'label': 'Region XVIII', 'value': 'Region XVIII'}
]
offWhite = "#ebebeb"
offWhite2 = "#fafafa"
teal = "#d6fff6"
darkGreen = "#022f40"
midBlue = "4dccbd"
brightRed = "#d52941"
salmon = "#ff8484"
africanViolet = '#B18FCF'
yale = '#1B4079'

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children=[
        'An Integrated View of',
        html.Br(),
        'House Pricing, ',
        html.Br(),
        'and ',
        html.Span('Seismic Events.', id='seismicEventsTitle'),
    ]),

    html.Div(children=html.P(introParagraph)),

    html.Div(className='spacer'),

    html.Br(),
    html.Br(),

    html.Center(
        html.Div(
            id='mapControlsDiv',
            children=[
                html.Div(
                    id='mapQuakeControlsDiv',
                    className='mapControlPanel',
                    children=[
                        html.H3(
                            className='mapPanelTitle',
                            children='Earthquakes'
                        ),

                        dcc.Dropdown(
                            id='mapQuakePanelDrop',
                            className='mapPanelDrop',
                            options=regionOptions,
                            placeholder='Select region'
                        ),

                        html.Div(
                            children='Filter by magnitude',
                            id='mapQuakePanelTextDiv'
                        ),

                        dcc.RangeSlider(
                            0,
                            10,
                            0.1,
                            value=[0, 10],
                            marks={
                                0: {'label': '0', 'style': {'color': teal}},
                                10: {'label': '10', 'style': {'color': salmon}}},
                            tooltip={'always_visible': False},
                            id='mapQuakePanelSlider',
                        ),

                        daq.ToggleSwitch(
                            className='mapPanelSwitch',
                            id='mapQuakePanelSwitch',
                            value=False,
                            color='#4dccbd'
                        )
                    ]
                ),

                html.Div(
                    id='mapHouseControlsDiv',
                    className='mapControlPanel',
                    children=[
                        html.H3(
                            className='mapPanelTitle',
                            children='Houses'
                        ),

                        dcc.Dropdown(
                            id='mapHousePanelRegionDrop',
                            className='mapPanelDrop',
                            options=regionOptions,
                            placeholder='Select region'
                        ),

                        dcc.Dropdown(
                            id='mapHousePanelBedDrop',
                            className='mapPanelDrop',
                            multi=True,
                            options=[
                                {'label': '1', 'value': 1},
                                {'label': '2', 'value': 2},
                                {'label': '3', 'value': 3},
                                {'label': '4+', 'value': 4}],
                            placeholder='Select number of bedrooms'
                        ),

                        dcc.Dropdown(
                            id='mapHousePanelBathDrop',
                            className='mapPanelDrop',
                            multi=True,
                            options=[
                                {'label': '1', 'value': 1},
                                {'label': '2', 'value': 2},
                                {'label': '3', 'value': 3},
                                {'label': '4+', 'value': 4}],
                            placeholder='Select number of bathrooms'
                        ),

                        daq.ToggleSwitch(
                            className='mapPanelSwitch',
                            id='mapHousePanelSwitch',
                            value=False,
                            color='#4dccbd'
                        )
                    ]
                )

            ]
        )
    ),
    html.Center(html.Div(id='mapDiv', children=[dcc.Graph(id='mainMap')])),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div(
        children=[
            html.Center(
                children=[
                    html.H2(className='sectionTitle', children='Earthquakes - '),
                    html.H2(id='quakeRegionText', className='dynamicText'),
                    dcc.Dropdown(
                        id='quakeDropdown',
                        className='regionDropdown',
                        options=regionOptions,
                        placeholder='Select region'
                    )
                ]
            )
        ]
    ),

    html.Br(),
    html.Br(),

    html.Center(
        html.Div(
            id='quakeBigDiv',
            children=[
                html.Div(
                    id='quakeDivTop',
                    children=[
                        html.Div(
                            id='quakeDivTopLeft',
                            children=[
                                dcc.Graph(
                                    id='quakePie',
                                    style={'width': '100%', 'height': '100%'},
                                    figure={}
                                )
                            ]
                        ),
                        html.Div(
                            id='quakeDivTopRight',
                            children=
                                dcc.Graph(
                                    id='quakeHist',
                                    figure={}
                            )
                        )
                    ]
                ),
                html.Div(
                    id='quakeDivBottom',
                    children=[
                        dcc.Graph(
                            id='quakeLine',
                        )
                    ]
                )
            ]
        )
    ),

    html.Br(),
    html.Br(),

    html.Div(
        children=[
            html.Center(
                children=[
                    html.H2(className='sectionTitle', children='Houses - '),
                    html.H2(id='houseRegionText', className='sectionTitle'),
                    dcc.Dropdown(
                        id='houseDropdown',
                        className='regionDropdown',
                        options=regionOptions,
                        placeholder='Select region'
                    )
                ]
            )
        ]
    ),

    html.Br(),
    html.Br(),

    html.Center(
        html.Div(
            id='houseBigDiv',
            children=[
                html.Div(
                    id='houseDivTop',
                    children=[
                        html.Div(
                            id='houseDivTopLeft',
                            children=[
                                dcc.Graph(
                                    id='housePie',
                                    style={'width': '100%', 'height': '100%'},
                                    figure={}
                                )
                            ]
                        ),
                        html.Div(
                            id='houseDivTopRight',
                            children=[
                                dcc.Graph(
                                id='houseBoxplot',
                                figure={}
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    id='houseDivBottom',
                    children=[
                        html.Div(
                            id='houseDivBottomLeft',
                            children=[
                                        dcc.Graph()
                            ]
                        ),

                        html.Div(
                            id='houseDivBottomRight',
                            children=[
                                dcc.Graph()
                            ]
                        )
                    ]
                )
            ]
        )
    ),


    html.Br(),
    html.Br(),
    html.Br(),
])

# ---------------------------------------------------------------------------------------------------------------------


@app.callback(
    [Output(component_id='housePie', component_property='figure'),
     Output(component_id='houseRegionText', component_property='children'), ],
    Input(component_id='houseDropdown', component_property='value')
)
def updateHousePie(region):
    df = pd.read_csv(housingDataset)
    filtered_df = df.loc[df['region'] == region]
    province_counts = filtered_df['province'].value_counts()
    top_provinces = province_counts.nlargest(3)
    others_count = province_counts[~province_counts.index.isin(top_provinces.index)].sum()
    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
        top_provinces = pd.concat([top_provinces, others_series])

    top_provinces = top_provinces.sort_values(ascending=False)

    fig = px.pie(
        names=top_provinces.index,
        values=top_provinces.values,
        hole=0.8,
        color=top_provinces.index,
        color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#d6fff6'],
    )

    fig.update_layout(
        title=dict(
            text=f'Top 3 Areas with the Most Houses<br>',
            font=dict(
                size=18,
                color=offWhite,
                family='Arial, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=darkGreen,
        legend=dict(
            orientation='v',
            yanchor='middle',
            xanchor='center',
            y=0.5,
            x=0.5,
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(2, 47, 64, 100)',
            borderwidth=0,
            font=dict(color=offWhite)
        ),
        margin=dict(t=120, b=100, l=10, r=10)
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
        textinfo='none'
    )
    return fig, region


@app.callback(
Output(component_id='houseBoxplot', component_property='figure'),
    Input(component_id='houseDropdown', component_property='value')
)
def updateHouseBoxplot(region):
    df = pd.read_csv(housingDataset)
    df = df.loc[df['region'] == region]

    fig = px.box(
        df,
        x = 'province',
        y = 'price'
    )

    fig.update_layout(
        paper_bgcolor=offWhite2,
        title=dict(
            text=f"House Prices Distribution",
            font=dict(
                size=20,
                color=darkGreen,
                family='Arial',
            ),
            x=0.5,
            xanchor='center'
        )
    )

    fig.update_layout(
        paper_bgcolor=offWhite2,
        yaxis_title="Average Price of a House",
        xaxis_title="Provinces",
        xaxis=dict(
            scaleanchor=None,
            constrain='domain'
        ),
        yaxis=dict(
            scaleanchor=None,
            constrain='domain'
        ),
        margin=dict(l=200, r=200, t=50, b=50),
    )

    fig.update_traces(
        hovertemplate="<b>Year:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>",
        line=dict(color='#ff8484'),
        marker_color ='#ff8484',
    )

    fig.update_traces(
        hoverinfo="x+y+text",  # Customize which information to show
        hovertemplate="<b>Category:</b> %{x}<br><b>Value:</b> %{y}<extra></extra>"
    )

    return fig

@app.callback(
    [Output(component_id='quakePie', component_property='figure'),
     Output(component_id='quakeRegionText', component_property='children'), ],
    Input(component_id='quakeDropdown', component_property='value')
)
def updateQuakePie(region):
    df = pd.read_csv(earthquakeDataset)
    filtered_df = df.loc[df['region'] == region]
    province_counts = filtered_df['province'].value_counts()
    top_provinces = province_counts.nlargest(3)
    others_count = province_counts[~province_counts.index.isin(top_provinces.index)].sum()
    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
        top_provinces = pd.concat([top_provinces, others_series])

    top_provinces = top_provinces.sort_values(ascending=False)

    fig = px.pie(
        names=top_provinces.index,
        values=top_provinces.values,
        hole=0.8,
        color=top_provinces.index,
        color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#d6fff6'],
    )

    fig.update_layout(
        title=dict(
            text=f'Top 3 Areas with the Most Earthquakes<br>',
            font=dict(
                size=18,
                color=offWhite,
                family='Arial, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=darkGreen,
        legend=dict(
            orientation='v',
            yanchor='middle',
            xanchor='center',
            y=0.5,
            x=0.5,
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(2, 47, 64, 100)',
            borderwidth=0,
            font=dict(color=offWhite)
        ),
        margin=dict(t=120, b=100, l=10, r=10)
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
        textinfo='none'
    )
    return fig, region


@app.callback(
    Output(component_id='quakeHist', component_property='figure'),
    Input(component_id='quakeDropdown', component_property='value')
)
def updateQuakeHist(region):
    df = pd.read_csv(earthquakeDataset)
    df.sort_values('region', ascending=True)
    fig = px.histogram(
        df.loc[df['region'] == region]['magnitude'],
        x='magnitude',
        color_discrete_sequence=[africanViolet],
    )

    fig.update_layout(
        paper_bgcolor=offWhite2,
        title=dict(
            text=f"Earthquake Magnitude Distribution",
            font=dict(
                size=20,
                color=darkGreen,
                family='Arial',
            ),
            x=0.5,
            xanchor='center'
        )
    )

    fig.update_traces(
        hovertemplate="<b>Magnitude:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>"
    )

    return fig


@app.callback(
    Output(component_id='quakeLine', component_property='figure'),
    Input(component_id='quakeDropdown', component_property='value')
)
def updateQuakeLine(region):
    df = pd.read_csv(earthquakeDataset)
    df = df.loc[df['region'] == region]
    df.groupby('date_time_ph')['magnitude'].count().reset_index()

    fig = px.line(
        df.groupby('date_time_ph')['magnitude'].count().reset_index(),
        x='date_time_ph',
        y='magnitude'
    )

    fig.update_layout(
        paper_bgcolor=offWhite2,
        yaxis_title="Number of Earthquakes",
        xaxis_title="Year",
        xaxis=dict(
            scaleanchor=None,
            constrain='domain'
        ),
        yaxis=dict(
            scaleanchor=None,
            constrain='domain'
        ),
        margin=dict(l=200, r=200, t=50, b=50),
    )

    fig.update_traces(
        hovertemplate="<b>Year:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>",
        line=dict(color=africanViolet)
    )

    return fig



if __name__ == '__main__':
    app.run(debug=True)
