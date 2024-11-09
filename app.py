from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_daq as daq

housingDataset = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/newPH_housing.csv'
earthquakeDataset = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/earthquake.csv'
avgMerged = 'https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/merged_house_eq.csv'
colorSequenceList = ['#d52941', '#ff8484', '#4dccbd', '#EFA00B']
introParagraph1 = ("The Philippines is one of the world’s top earthquake-prone countries according to ")
introParagraph2 = ("Inquirer")
introParagraph3 = ("; ensuring house safety is a crucial consideration for homebuyers. Finding a safe and well-priced home requires "
                  "more than just a location search. Our website combines real estate listings with seismic data to provide "
                  "insights through an integrated view of housing affordability and evaluate earthquake risk in the Philippines. "
                  "If you are looking for a home, this can be a tool equipping you to gather essential insights by evaluating "
                  "properties not just by price, number of bedrooms and bathrooms, and land size, but also the proximity "
                  "of houses to earthquake-prone zones–navigating houses with confidence, balancing budget with security in this dynamic landscape.")


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
gamboge = "#EFA00B"
darkGreen = "#022f40"
midBlue = "4dccbd"
brightRed = "#d52941"
salmon = "#ff8484"
yale = '#1B4079'

app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.Store(
        id='donutIsolateStore',
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
        html.A(introParagraph2, href = 'https://newsinfo.inquirer.net/1923394/ph-lands-on-list-of-countries-most-prone-to-quakes'),
        introParagraph3
    ])),

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
                                0: {'label': '0', 'style': {'color': gamboge}},
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
    html.Center(html.Div(id='mapDiv', children=[dcc.Graph(id='mainMap')])), #TODO Dave

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
                            id='houseDivBottomLeft', # scatterplot
                            children=[
                                dcc.Graph(
                                    id='houseScatterplot',
                                    figure={}
                                )
                            ]
                        ),

                        html.Div(
                            id='houseDivBottomRight', # i still dont know
                            children=[
                                dcc.Graph(
                                    id = 'mergedBubblechart',
                                    figure={}
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


    html.Br(),
    html.Br(),
    html.Br(),
])

# Wendell part----------------------------------------------------------------------------------------------------------


@app.callback(
    [Output(component_id='housePie', component_property='figure'),
     Output(component_id='houseRegionText', component_property='children'),
     Output(component_id='donutIsolateStore', component_property='data')],
    [Input(component_id='houseDropdown', component_property='value'),
     Input(component_id='housePie', component_property='clickData'),
     Input(component_id='donutIsolateStore', component_property='data')]
)
def updateHousePie(region, clickData, clickStored):
    df = pd.read_csv(housingDataset)
    filtered_df = df.loc[df['region'] == region]
    provinceCounts = filtered_df['province'].value_counts()
    topProvinces = provinceCounts.nlargest(3)
    others_count = provinceCounts[~provinceCounts.index.isin(topProvinces.index)].sum()
    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
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
    [Input(component_id='houseDropdown', component_property='value'),
     Input(component_id='donutIsolateStore', component_property='data')]
)
def updateHouseBoxplot(region, clickStored):
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
            x= 'province',
            y= 'price',
            color='coloring',
            color_discrete_sequence=colorSequenceList
        )

    fig.update_layout(
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
    [Input(component_id='houseDropdown', component_property='value'),
     Input(component_id='donutIsolateStore', component_property='data')]
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
    Input(component_id='houseDropdown', component_property = 'value')
)

def updateMergedBubbleChart(region):
    # Obtaining the top 3
    df = pd.read_csv(housingDataset)
    filtered_df = df.loc[df['region'] == region]
    province_counts = filtered_df['province'].value_counts()
    top_provinces = province_counts.nlargest(3)
    others_count = province_counts[~province_counts.index.isin(top_provinces.index)].sum()
    df1 = filtered_df.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in top_provinces.index.tolist() else 'Others')

    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
        top_provinces = pd.concat([top_provinces, others_series])

    # Applying the coloring on the merged averages dataset
    df2 = pd.read_csv(avgMerged)
    df2 = df2.loc[df2['region'] == region]
    df2['coloring'] = df2['province'].apply(lambda x: x if x in top_provinces.index.tolist() else 'Others')

    top_provinces.reset_index().rename(columns={'index': 'coloring'})
    df3 = pd.merge(df2, top_provinces.reset_index(name='count').rename(columns={'index':'coloring'})).sort_values('count', ascending=False)

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
        color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#EFA00B'],
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
def updateQuakeBox(region):
    df = pd.read_csv(earthquakeDataset)
    filtered_df = df.loc[df['region'] == region]
    province_counts = filtered_df['province'].value_counts()
    top_provinces = province_counts.nlargest(3)
    others_count = province_counts[~province_counts.index.isin(top_provinces.index)].sum()
    df1 = filtered_df.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in top_provinces.index.tolist() else 'Others')

    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
        top_provinces = pd.concat([top_provinces, others_series])

    top_provinces = top_provinces.reset_index(name='count').sort_values('count', ascending=False)
    top_provinces.rename(columns={top_provinces.columns[0]: 'province'}, inplace=True)

    order = top_provinces['province'].tolist()
    df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
    df1 = df1.sort_values('coloring')

    fig = px.box(
        df1,
        x='province',
        y='magnitude',
        color='coloring',
        color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#EFA00B']
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
    Input(component_id='quakeDropdown', component_property='value')
)
def updateQuakeLine(region):
    df = pd.read_csv(earthquakeDataset)
    filtered_df = df.loc[df['region'] == region]
    province_counts = filtered_df['province'].value_counts()
    top_provinces = province_counts.nlargest(3)
    others_count = province_counts[~province_counts.index.isin(top_provinces.index)].sum()

    df1 = filtered_df.copy()
    df1['coloring'] = df1['province'].apply(lambda x: x if x in top_provinces.index.tolist() else 'Others')

    if others_count > 0:
        others_series = pd.Series({'Others': others_count})
        top_provinces = pd.concat([top_provinces, others_series])

    top_provinces = top_provinces.reset_index(name='count').sort_values('count', ascending=False)
    top_provinces.rename(columns={top_provinces.columns[0]: 'province'}, inplace=True)

    order = top_provinces['province'].tolist()
    df1['coloring'] = pd.Categorical(df1['coloring'], categories=order, ordered=True)
    df1 = df1.sort_values('coloring')

    fig = px.line(
        df1.groupby(['date_time_ph', 'coloring'])['magnitude'].count().reset_index(name='count'),
        x='date_time_ph',
        y='count',
        color='coloring',
        category_orders={'coloring': order},
        color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#EFA00B']
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
    Input(component_id='houseDropdown', component_property='value')
)
def resetClickData(value):
    return None


if __name__ == '__main__':
    app.run(debug=True)
