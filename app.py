from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_daq as daq
import json
import requests

housingDataset = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/housingCleaned.csv'
earthquakeDataset = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/earthquakeCleaned.csv'
avgMerged = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/merged_house_eq.csv'
colorSequenceList = ['#d52941', '#ff8484', '#4dccbd', '#EFA00B']
introParagraph1 = ("The Philippines is one of the world’s top earthquake-prone countries according to ")
introParagraph2 = ("Inquirer")
introParagraph3 = (
    "; ensuring house safety is a crucial consideration for homebuyers. Finding a safe and well-priced home requires "
    "more than just a location search. Our website combines real estate listings with seismic data to provide "
    "insights through an integrated view of housing affordability and evaluate earthquake risk in the Philippines. "
    "If you are looking for a home, this can be a tool equipping you to gather essential insights by evaluating "
    "properties not just by price, number of bedrooms and bathrooms, and land size, but also the proximity "
    "of houses to earthquake-prone zones–navigating houses with confidence, balancing budget with security in this dynamic landscape."
    " Our limitation is that there is no data in Region IV-B (MIMAROPA) in the housing dataset, and so, the said region will not be"
    " shown in this website.")

offWhite = "#ebebeb"
offWhite2 = "#fafafa"
gamboge = "#EFA00B"
darkGreen = "#022f40"
midBlue = "#4dccbd"
brightRed = "#d52941"
salmon = "#ff8484"
yale = '#1B4079'

df1 = pd.read_csv(
    'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/earthquakeCleaned.csv')
df2 = pd.read_csv(
    'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/housingCleaned.csv')

url = (
    'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/philippines-with-regions_.geojson')
response = requests.get(url)
phil_regions = response.json()

df2['bedrooms_category'] = df2['bedrooms'].apply(lambda x: '4+' if x > 4 else str(x))
df2['bathrooms_category'] = df2['bathrooms'].apply(lambda x: '4+' if x > 4 else str(x))

app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.Store(
        id='donutHouseIsolateStore',
        data=None
    ),

    dcc.Store(
        id='donutQuakeIsolateStore',
        data=None
    ),

    html.H1(children=[
        'An Integrated View of',
        html.Br(),
        html.Span('House Pricing, ', id='housePricingTitle'),
        html.Br(),
        'and ',
        html.Span('Seismic Events.', id='seismicEventsTitle'),
    ]),

    html.Div(children=html.P([
        introParagraph1,
        html.A(introParagraph2,
               href='https://newsinfo.inquirer.net/1923394/ph-lands-on-list-of-countries-most-prone-to-quakes'),
        introParagraph3
    ])),

    html.Div(className='spacer'),

    html.Br(),

    html.Center(
        html.Div(
            id='mapSectionMainDiv',
            children=[
                html.Div(
                    id='mapSectionMainDivLeft',
                    children=[
                        html.Div(
                            id='mapSectionTitleDiv',
                            children=[
                                html.H2(
                                    id='mapSectionTitle',
                                    children=['Integrated Map']
                                )
                            ]
                        ),

                        html.Div(
                            id='houseControlsDiv',
                            children=[
                                html.H3(
                                    id='houseControlsTitle',
                                    className='mapPanelTitle',
                                    children=[
                                        'Houses'
                                    ]
                                ),

                                dcc.Dropdown(
                                    id='mapHousePanelRegionDrop',
                                    className='mapPanelDrop',
                                    options=[
                                        {'label': 'Region I - Ilocos Region', 'value': 'Region I'},
                                        {'label': 'Region II - Cagayan Valley', 'value': 'Region II'},
                                        {'label': 'Region III - Central Luzon', 'value': 'Region III'},
                                        {'label': 'Region IV-A - CALABARZON', 'value': 'Region IV-A'},
                                        {'label': 'Region V - Bicol Region', 'value': 'Region V'},
                                        {'label': 'Region VI - Western Visayas', 'value': 'Region VI'},
                                        {'label': 'Region VII - Central Visayas', 'value': 'Region VII'},
                                        {'label': 'Region IX - Zamboanga Peninsula', 'value': 'Region IX'},
                                        {'label': 'Region X - Northern Mindanao', 'value': 'Region X'},
                                        {'label': 'Region XI - Davao Region', 'value': 'Region XI'},
                                        {'label': 'Region XII - SOCCSKSARGEN', 'value': 'Region XII'},
                                        {'label': 'Region XIII - Caraga', 'value': 'Region XIII'},
                                        {'label': 'NCR - National Capital Region', 'value': 'NCR'},
                                        {'label': 'CAR - Cordillera Administrative Region', 'value': 'CAR'},
                                        {'label': 'Region XVIII', 'value': 'Region XVIII'}
                                    ],
                                    placeholder='Select region'
                                ),

                                dcc.Dropdown(
                                    id='mapHousePanelBedDrop',
                                    className='mapPanelDrop',
                                    multi=True,
                                    options=[{'label': str(i), 'value': str(i)} for i in ['1', '2', '3', '4+']],
                                    placeholder='Select number of bedrooms'
                                ),

                                dcc.Dropdown(
                                    id='mapHousePanelBathDrop',
                                    className='mapPanelDrop',
                                    multi=True,
                                    options=[{'label': str(i), 'value': str(i)} for i in ['1', '2', '3', '4+']],
                                    placeholder='Select number of bathrooms'
                                ),


                            ]
                        )
                    ]
                ),

                html.Div(
                    id='mapSectionMainDivRight',
                    children=[
                        dcc.Graph(
                            id='mainMap'
                        )
                    ]
                )
            ]
        )
    ),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div(
        children=[
            html.Center(
                children=[
                    html.H2(className='sectionTitle', children='Houses - '),
                    html.H2(id='houseRegionText', className='sectionTitle'),
                    dcc.Dropdown(
                        id='graphsDropdown',
                        className='regionDropdown',
                        options=[
                            {'label': 'Region I - Ilocos Region', 'value': 'Region I'},
                            {'label': 'Region II - Cagayan Valley', 'value': 'Region II'},
                            {'label': 'Region III - Central Luzon', 'value': 'Region III'},
                            {'label': 'Region IV-A - CALABARZON', 'value': 'Region IV-A'},
                            {'label': 'Region V - Bicol Region', 'value': 'Region V'},
                            {'label': 'Region VI - Western Visayas', 'value': 'Region VI'},
                            {'label': 'Region VII - Central Visayas', 'value': 'Region VII'},
                            {'label': 'Region IX - Zamboanga Peninsula', 'value': 'Region IX'},
                            {'label': 'Region X - Northern Mindanao', 'value': 'Region X'},
                            {'label': 'Region XI - Davao Region', 'value': 'Region XI'},
                            {'label': 'Region XII - SOCCSKSARGEN', 'value': 'Region XII'},
                            {'label': 'Region XIII - Caraga', 'value': 'Region XIII'},
                            {'label': 'NCR - National Capital Region', 'value': 'NCR'},
                            {'label': 'CAR - Cordillera Administrative Region', 'value': 'CAR'},
                            {'label': 'Region XVIII', 'value': 'Region XVIII'}
                        ],
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
                                    figure={},
                                    style={
                                        'height': '100%',
                                        'width': '100%',
                                        'overflow' : 'hidden'
                                    }
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
                                dcc.Graph(
                                    id='houseScatterplot',
                                    figure={},
                                    style={
                                        'height': '100%',
                                        'width': '100%',
                                        'overflow' : 'hidden'
                                    }
                                )
                            ]
                        ),

                        html.Div(
                            id='houseDivBottomRight',
                            children=[
                                dcc.Graph(
                                    id='mergedBubblechart',
                                    figure={},
                                    style={
                                        'height': '100%',
                                        'width': '100%',
                                        'overflow' : 'hidden'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ),

    html.Div(
        children=[
            html.Center(
                children=[
                    html.H2(className='sectionTitle', children='Earthquakes - '),
                    html.H2(id='quakeRegionText', className='dynamicText'),

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
                                figure={},
                                style={
                                        'height': '100%',
                                        'width': '100%',
                                        'overflow' : 'hidden'
                                    }
                            )
                        )
                    ]
                ),
                html.Div(
                    id='quakeDivBottom',
                    children=[
                        dcc.Graph(
                            id='quakeLine',
                            style={
                                'height': '100%',
                                'width': '100%',
                                'overflow' : 'hidden'
                            }
                        )
                    ]
                )
            ]
        )
    ),

    html.Br(),
    html.Br(),

    html.Br(),
    html.Br(),
    html.Br(),
])


# Callbacks----------------------------------------------------------------------------------------------------------

@app.callback(
    Output('mainMap', 'figure'),
    [
     Input('mapHousePanelRegionDrop', 'value'),
     Input('mapHousePanelBedDrop', 'value'),
     Input('mapHousePanelBathDrop', 'value')]
)
def updateMap(selectedRegion, selectedBed, selectedBath):
    filtered_df2 = df2.copy()
    if selectedRegion:
        filtered_df2 = filtered_df2[filtered_df2['region'] == selectedRegion]
    if selectedBed:
        filtered_df2 = filtered_df2[filtered_df2['bedrooms_category'].isin(selectedBed)]
    if selectedBath:
        filtered_df2 = filtered_df2[filtered_df2['bathrooms_category'].isin(selectedBath)]

    eq_map = px.choropleth_mapbox(
        df1,
        geojson=phil_regions,
        featureidkey='properties.name',
        locations='province',
        color='average_magnitude',
        hover_name='region',
        hover_data=['average_magnitude'],
        zoom=4,
        height=400,
        center={"lat": 12.8797, "lon": 121.7740},
        mapbox_style='carto-positron',
        color_continuous_scale=["#EFA00B", "#d52941"]
    )
    eq_map.update_layout(
        margin={'r': 50, 't': 0, 'l': 0, 'b': 0},
    )

    hs_map = px.scatter_mapbox(
        filtered_df2,
        lat='latitude',
        lon='longitude',
        hover_name='province',
        hover_data=['city', 'price', 'bedrooms', 'bathrooms', 'floor area', 'land area'],
        size='price',
        zoom=4,
        height=400,
        mapbox_style='carto-positron',
        color_discrete_sequence=["#022f40"]
    )
    hs_map.update_layout(
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
    )

    eq_and_hs_map = go.Figure()
    for trace in eq_map.data:
        eq_and_hs_map.add_trace(trace)
    for trace in hs_map.data:
        eq_and_hs_map.add_trace(trace)
    eq_and_hs_map.update_layout(
        mapbox=dict(
            style='carto-positron',
            zoom=5,
            center={"lat": 12.8797, "lon": 121.7740},
        ),
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        legend=dict(
            font=dict(
                color="white"
            ),
            x=0,
            y=0.95,
            bgcolor="rgba(255,255,255,0.6)",
            bordercolor="#022f40",
            borderwidth=1,
        ),
        coloraxis=dict(
            colorscale=['#4dccbd', '#EFA00B', '#d52941'],
            cmin=df1['average_magnitude'].min(),
            cmax=df1['average_magnitude'].max()
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(color="black"),
            title=dict(
                text="Average Magnitude",
                font=dict(color="#022f40"),
                side='top'
            ),
            x=0.05,
            xanchor='left',  # Align the left side of the color bar at the x position
            y=0.5,  # Center the color bar vertically
            yanchor='middle',  # Align the middle of the color bar at the y position
        )
    )

    return eq_and_hs_map




@app.callback(
    [Output(component_id='housePie', component_property='figure'),
     Output(component_id='houseRegionText', component_property='children'),
     Output(component_id='donutHouseIsolateStore', component_property='data')],
    [Input(component_id='graphsDropdown', component_property='value'),
     Input(component_id='housePie', component_property='clickData'),
     Input(component_id='donutHouseIsolateStore', component_property='data')]
)
def updateHousePie(region, clickData, clickStored):
    df = pd.read_csv(housingDataset)
    filteredDf = df.loc[df['region'] == region]
    provinceCounts = filteredDf['province'].value_counts()
    topProvinces = provinceCounts.nlargest(3)
    othersCount = provinceCounts[~provinceCounts.index.isin(topProvinces.index)].sum()
    if othersCount > 0:
        othersSeries = pd.Series({'Others': othersCount})
        topProvinces = pd.concat([topProvinces, othersSeries])

    topProvinces = topProvinces.sort_values(ascending=False).reset_index()
    topProvinces.rename(columns={topProvinces.columns[0]: 'province', topProvinces.columns[1]: 'count'}, inplace=True)
    topProvinces = topProvinces.reset_index(drop=True)

    # Just to initialize the variable
    toStore = None

    if clickData:
        selected = clickData['points'][0]['label']

        if selected == clickStored:
            toStore = None
            fig = px.pie(
                topProvinces,
                names='province',
                values='count',
                hole=0.8,
                color='province',
                color_discrete_sequence=colorSequenceList,
            )
        else:
            topProvinces = topProvinces.loc[topProvinces['province'] == selected]
            colorIdx = topProvinces.loc[topProvinces['province'] == selected].index[0]
            toStore = selected

            fig = px.pie(
                topProvinces,
                names='province',
                values='count',
                hole=0.8,
                color='province',
                color_discrete_sequence=[colorSequenceList[colorIdx]],
            )
    else:
        fig = px.pie(
            topProvinces,
            names='province',
            values='count',
            hole=0.8,
            color='province',
            color_discrete_sequence=colorSequenceList,
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

    return fig, region, toStore


@app.callback(
    Output(component_id='houseBoxplot', component_property='figure'),
    [Input(component_id='graphsDropdown', component_property='value'),
     Input(component_id='donutHouseIsolateStore', component_property='data')]
)
def updateHouseBoxplot(region, clickStored):
    df = pd.read_csv(housingDataset)
    filteredDf = df.loc[df['region'] == region]
    provinceCounts = filteredDf['province'].value_counts()
    topProvinces = provinceCounts.nlargest(3)
    othersCount = provinceCounts[~provinceCounts.index.isin(topProvinces.index)].sum()
    df1 = filteredDf.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in topProvinces.index.tolist() else 'Others')

    if othersCount > 0:
        others_series = pd.Series({'Others': othersCount})
        topProvinces = pd.concat([topProvinces, others_series])

    topProvinces = topProvinces.reset_index(name='count').sort_values('count', ascending=False)
    topProvinces.rename(columns={topProvinces.columns[0]: 'province'}, inplace=True)
    topProvinces = topProvinces.reset_index(drop=True)

    # If the stored data is not None i.e. an actual province is stored
    if clickStored:
        topProvinces = topProvinces.loc[topProvinces['province'] == clickStored]
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')

        colorIdx = topProvinces.loc[topProvinces['province'] == clickStored].index[0]

        fig = px.box(
            df1,
            x='province',
            y='price',
            color='coloring',
            color_discrete_sequence=[colorSequenceList[colorIdx]]
        )

    else:
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')
        fig = px.box(
            df1,
            x='province',
            y='price',
            color='coloring',
            color_discrete_sequence=colorSequenceList
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=10),

        showlegend=False,
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
        hoverinfo="x+y+text",
        hovertemplate="<b>Category:</b> %{x}<br><b>Value:</b> %{y}<extra></extra>"
    )

    return fig


@app.callback(
    Output(component_id='houseScatterplot', component_property='figure'),
    [Input(component_id='graphsDropdown', component_property='value'),
     Input(component_id='donutHouseIsolateStore', component_property='data')]
)
def updateHouseScatterplot(region, clickStored):
    df = pd.read_csv(housingDataset)
    filtered_df = df.loc[df['region'] == region]
    province_counts = filtered_df['province'].value_counts()
    topProvinces = province_counts.nlargest(3)
    others_count = province_counts[~province_counts.index.isin(topProvinces.index)].sum()
    df1 = filtered_df.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in topProvinces.index.tolist() else 'Others')

    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
        topProvinces = pd.concat([topProvinces, others_series])

    topProvinces = topProvinces.reset_index(name='count').sort_values('count', ascending=False)
    topProvinces.rename(columns={topProvinces.columns[0]: 'province'}, inplace=True)
    topProvinces = topProvinces.reset_index(drop=True)

    # If the stored data is not None i.e. an actual province is stored
    if clickStored:
        topProvinces = topProvinces.loc[topProvinces['province'] == clickStored]
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')

        colorIdx = topProvinces.loc[topProvinces['province'] == clickStored].index[0]

        fig = px.scatter(
            df1,
            x='land area',
            y='price',
            color='coloring',
            color_discrete_sequence=[colorSequenceList[colorIdx]]
        )
    else:
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')

        fig = px.scatter(
            df1,
            x='land area',
            y='price',
            color='coloring',
            color_discrete_sequence=colorSequenceList
        )

    fig.update_layout(
        showlegend=False,
        paper_bgcolor=offWhite2,
        yaxis_title="Prices",
        xaxis_title="Land Area of Houses",
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
    )

    fig.update_traces(
        hoverinfo="x+y+text",  # Customize which information to show
        hovertemplate="<b>Category:</b> %{x}<br><b>Value:</b> %{y}<extra></extra>"
    )

    return fig


@app.callback(
    Output(component_id='mergedBubblechart', component_property='figure'),
    [Input(component_id='graphsDropdown', component_property='value'),
     Input(component_id='donutHouseIsolateStore', component_property='data')]
)
def updateMergedBubbleChart(region, clickStored):
    # Obtaining the top 3
    df = pd.read_csv(housingDataset)
    filtered_df = df.loc[df['region'] == region]
    provinceCounts = filtered_df['province'].value_counts()
    topProvinces = provinceCounts.nlargest(3)
    others_count = provinceCounts[~provinceCounts.index.isin(topProvinces.index)].sum()
    df1 = filtered_df.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in topProvinces.index.tolist() else 'Others')

    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
        topProvinces = pd.concat([topProvinces, others_series])

    # Applying the coloring on the merged averages dataset
    df2 = pd.read_csv(avgMerged)
    df2 = df2.loc[df2['region'] == region]
    df2['coloring'] = df2['province'].apply(lambda x: x if x in topProvinces.index.tolist() else 'Others')

    topProvinces = topProvinces.reset_index(name='count')
    topProvinces = topProvinces.rename(columns={topProvinces.columns[0]: 'coloring'})
    df3 = pd.merge(df2, topProvinces).sort_values('count', ascending=False)

    if clickStored:
        topProvinces = topProvinces.sort_values('count', ascending=False).reset_index(drop=True)
        order = topProvinces['coloring'].tolist()
        df3['coloring'] = pd.Categorical(df3['coloring'], categories=order, ordered=True)
        df3 = df3.sort_values('coloring')
        df3 = df3.loc[df3['coloring'] == clickStored]

        colorIdx = topProvinces.loc[topProvinces['coloring'] == clickStored].index[0]

        fig = px.scatter(
            df3,
            x="average_price",
            y="average_magnitude",
            size="average_land_area",
            color="coloring",
            hover_data='average_land_area',
            color_discrete_sequence=[colorSequenceList[colorIdx]],
            opacity=1.0
        )
    else:
        fig = px.scatter(
            df3,
            x="average_price",
            y="average_magnitude",
            size="average_land_area",
            color="coloring",
            hover_data='average_land_area',
            color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#EFA00B'],
            opacity=1.0
        )

    fig.update_layout(
        showlegend=False,
        paper_bgcolor=offWhite2,
        yaxis_title="Average Earthquake Magnitude",
        xaxis_title="Average House Price (PHP)",
        xaxis=dict(
            scaleanchor=None,
            constrain='domain',
        ),
        yaxis=dict(
            scaleanchor=None,
            constrain='domain',
        ),
        margin=dict(l=200, r=200, t=50, b=50),
    )

    fig.update_traces(
        hoverinfo="x+y+text",  # Customize which information to show
        hovertemplate="<b>Avg Magnitude:</b> %{y}<br>"
                      "<b>Avg House Price:</b> %{x}<br>"
                      "<b>Avg Land Area:</b> %{marker.size}<extra></extra>",
        marker=dict(line=dict(width=0))
    )

    return fig


# Wendell part----------------------------------------------------------------------------------------------------------

@app.callback(
    [Output(component_id='quakePie', component_property='figure'),
     Output(component_id='quakeRegionText', component_property='children'),
     Output(component_id='donutQuakeIsolateStore', component_property='data')],
    [Input(component_id='graphsDropdown', component_property='value'),
     Input(component_id='quakePie', component_property='clickData'),
     Input(component_id='donutQuakeIsolateStore', component_property='data')]
)
def updateQuakePie(region, clickData, clickStored):
    df = pd.read_csv(earthquakeDataset)
    filteredDf = df.loc[df['region'] == region]
    provinceCounts = filteredDf['province'].value_counts()
    topProvinces = provinceCounts.nlargest(3)
    othersCount = provinceCounts[~provinceCounts.index.isin(topProvinces.index)].sum()
    if othersCount > 0:
        others_series = pd.Series({'Others': othersCount})
        topProvinces = pd.concat([topProvinces, others_series])

    topProvinces = topProvinces.sort_values(ascending=False).reset_index()
    topProvinces.rename(columns={topProvinces.columns[0]: 'province', topProvinces.columns[1]: 'count'}, inplace=True)
    topProvinces = topProvinces.reset_index(drop=True)

    # Just to initialize the variable
    toStore = None

    if clickData:
        selected = clickData['points'][0]['label']

        if selected == clickStored:
            toStore = None
            fig = px.pie(
                topProvinces,
                names='province',
                values='count',
                hole=0.8,
                color='province',
                color_discrete_sequence=colorSequenceList,
            )
        else:
            topProvinces = topProvinces.loc[topProvinces['province'] == selected]
            colorIdx = topProvinces.loc[topProvinces['province'] == selected].index[0]
            toStore = selected

            fig = px.pie(
                topProvinces,
                names='province',
                values='count',
                hole=0.8,
                color='province',
                color_discrete_sequence=[colorSequenceList[colorIdx]],
            )
    else:
        fig = px.pie(
            topProvinces,
            names='province',
            values='count',
            hole=0.8,
            color='province',
            color_discrete_sequence=colorSequenceList,
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
    return fig, region, toStore


@app.callback(
    Output(component_id='quakeHist', component_property='figure'),
    [Input(component_id='graphsDropdown', component_property='value'),
     Input(component_id='donutQuakeIsolateStore', component_property='data')]
)
def updateQuakeBox(region, clickStored):
    df = pd.read_csv(earthquakeDataset)
    filteredDf = df.loc[df['region'] == region]
    provinceCounts = filteredDf['province'].value_counts()
    topProvinces = provinceCounts.nlargest(3)
    provinceCounts = provinceCounts[~provinceCounts.index.isin(topProvinces.index)].sum()
    df1 = filteredDf.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in topProvinces.index.tolist() else 'Others')

    if provinceCounts > 0:
        othersSeries = pd.Series({'Others': provinceCounts})
        topProvinces = pd.concat([topProvinces, othersSeries])

    topProvinces = topProvinces.reset_index(name='count').sort_values('count', ascending=False)
    topProvinces.rename(columns={topProvinces.columns[0]: 'province'}, inplace=True)
    topProvinces = topProvinces.reset_index(drop=True)

    # If the stored data is not None i.e. an actual province is stored
    if clickStored:
        topProvinces = topProvinces.loc[topProvinces['province'] == clickStored]
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')

        colorIdx = topProvinces.loc[topProvinces['province'] == clickStored].index[0]

        fig = px.box(
            df1,
            x='province',
            y='magnitude',
            color='coloring',
            color_discrete_sequence=[colorSequenceList[colorIdx]]
        )

    else:
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')

        fig = px.box(
            df1,
            x='province',
            y='magnitude',
            color='coloring',
            color_discrete_sequence=colorSequenceList
        )

    fig.update_layout(
        showlegend=False,
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

    return fig


@app.callback(
    Output(component_id='quakeLine', component_property='figure'),
    [Input(component_id='graphsDropdown', component_property='value'),
     Input(component_id='donutQuakeIsolateStore', component_property='data')]
)
def updateQuakeLine(region, clickStored):
    df = pd.read_csv(earthquakeDataset)
    filteredDf = df.loc[df['region'] == region]
    provinceCounts = filteredDf['province'].value_counts()
    topProvinces = provinceCounts.nlargest(3)
    othersCount = provinceCounts[~provinceCounts.index.isin(topProvinces.index)].sum()

    df1 = filteredDf.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in topProvinces.index.tolist() else 'Others')

    if othersCount > 0:
        othersSeries = pd.Series({'Others': othersCount})
        topProvinces = pd.concat([topProvinces, othersSeries])

    topProvinces = topProvinces.reset_index(name='count').sort_values('count', ascending=False)
    topProvinces.rename(columns={topProvinces.columns[0]: 'province'}, inplace=True)
    topProvinces = topProvinces.reset_index(drop=True)

    if clickStored:
        topProvinces = topProvinces.loc[topProvinces['province'] == clickStored]
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')

        colorIdx = topProvinces.loc[topProvinces['province'] == clickStored].index[0]

        fig = px.line(
            df1.groupby(['date_time_ph', 'coloring'], observed=False)['magnitude'].count().reset_index(name='count'),
            x='date_time_ph',
            y='count',
            color='coloring',
            category_orders={'coloring': order},
            color_discrete_sequence=[colorSequenceList[colorIdx]]
        )

    else:
        order = topProvinces['province'].tolist()
        df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
        df1 = df1.sort_values('coloring')

        fig = px.line(
            df1.groupby(['date_time_ph', 'coloring'], observed=False)['magnitude'].count().reset_index(name='count'),
            x='date_time_ph',
            y='count',
            color='coloring',
            category_orders={'coloring': order},
            color_discrete_sequence=colorSequenceList
        )

    fig.update_layout(
        showlegend=False,
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
    )

    return fig


@app.callback(
    Output(component_id='housePie', component_property='clickData'),
    Input(component_id='graphsDropdown', component_property='value')
)
def resetClickData(value):
    return None


if __name__ == '__main__':
    app.run(debug=True)
