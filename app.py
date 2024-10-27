from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

introParagraph = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec at pharetra ante. Vestibulum ut sapien id nibh efficitur pulvinar id in leo. Nullam aliquet, velit at fermentum dictum, neque massa vehicula velit, ac scelerisque nunc mi quis eros. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris finibus volutpat congue. Cras ac gravida dolor. Praesent sed accumsan orci. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Ut porttitor nibh sem, vitae varius orci efficitur eget. Proin tincidunt, nisi et molestie congue, nisi nibh dignissim risus, in malesuada erat massa eu dolor. Vestibulum a quam at libero scelerisque tempus.'
offWhite = "#ebebeb"
teal = "#d6fff6"
darkColor = "#022f40"
midBlue = "4dccbd"
brightRed = "d52941"
salmon = "ff8484"

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children=[
        'An Integrated View of',
        html.Br(),
        'Real Estate Pricing, ',
        html.Br(),
        html.Span('Seismic Events,', id='seismicEventsTitle'),
        html.Br(),
        'and ',
        html.Span('Conflicts', id='conflictsTitle')
    ]),

    html.Div(children=[
        html.P(introParagraph)
    ]),

    html.Div(className='spacer'),

    html.Div(children=[
        html.H2(className='sectionTitle', children='Earthquakes - '),
        html.H2(id='quakeRegionText', className='dynamicText'),
    ]),

    dcc.Dropdown(
        id='quakeDropdown',
        className='regionDropdown',
        options=[
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
        ],
    ),

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
                            id='quakeTopRightDiv',
                            children=
                                dcc.Graph(
                                id='quakeHist',
                                figure={}
                            )
                        )
                    ]
                ),
                html.Div(
                    style={'background-color': 'green', 'height': '55%'},
                    children=[
                        dcc.Graph(
                            id='quakeLine',
                            style={'width': '100%', 'height': '100%'}
                        )
                    ]
                )
            ]
        )
    ),

    html.Div(id='spacer'),

    html.Div(children=[
        html.H2(className='sectionTitle', children='Houses - '),
        html.H2(id='houseRegionText', className='sectionTitle'),
    ]),

    dcc.Dropdown(
        id='houseDropdown',
        className='regionDropdown',
        style={
            'font-family': 'Arial, sans-serif',
            'font-size': '12px',
            'color': '#022f40'
        },
        options=[
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
        ],
    ),

    html.Center(
        html.Div(
            style={'background-color': 'red', 'height': '1000px', 'width': '90%', 'display': 'flex',
                   'flex-direction': 'column'},
            children=[
                html.Div(
                    style={'background-color': 'blue', 'height': '45%', 'display': 'flex', 'flex-direction': 'row'},
                    children=[
                        html.Div(
                            style={'background-color': 'yellow', 'width': '40%', 'display': 'flex',
                                   'justify-content': 'center', 'align-items': 'center'},
                            children=[
                                dcc.Graph(
                                    id='housePie',
                                    style={'width': '100%', 'height': '100%'},
                                    figure={}
                                )
                            ]
                        ),
                        dcc.Graph(
                            id='houseBoxplot',
                            style={'width': '100%', 'height': '100%'},
                            figure={}
                        )
                    ]
                ),
                html.Div(
                    style={'background-color': 'green', 'height': '55%'},
                    children=[
                        # dcc.Graph(
                        #     id='houseLine',
                        #     style={'width': '100%', 'height': '100%'}
                        # )
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
    df = pd.read_csv('https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/newPH_housing.csv')
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
        color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#022f40'],
    )

    fig.update_layout(
        title=dict(
            text=f'Top 3 Areas with the Most Houses<br>{region}',
            font=dict(
                size=18,
                color='#022f40',
                family='Arial, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=offWhite,
        legend=dict(
            orientation='v',
            yanchor='middle',
            xanchor='center',
            y=0.5,
            x=0.5,
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(2, 47, 64, 100)',
            borderwidth=0
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
    df = pd.read_csv('https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/newPH_housing.csv')
    df = df.loc[df['region'] == region]


    fig = px.box(
        df,
        x = 'province',
        y = 'price'
    )

    fig.update_layout(
        paper_bgcolor=offWhite,
        title=dict(
            text=f"{region} - House Prices Distribution",
            font=dict(
                size=20,
                color='#022f40',
                family='Arial',
            ),
            x=0.5,
            xanchor='center'
        )
    )

    fig.update_layout(
        paper_bgcolor=offWhite,
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
    df = pd.read_csv('https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/earthquake.csv')
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
        color_discrete_sequence=['#d52941', '#ff8484', '#4dccbd', '#022f40'],
    )



    fig.update_layout(
        title=dict(
            text=f'Top 3 Areas with the Most Occurrences<br>{region}',
            font=dict(
                size=18,
                color='#022f40',
                family='Arial, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=offWhite,
        legend=dict(
            orientation='v',
            yanchor='middle',
            xanchor='center',
            y=0.5,
            x=0.5,
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(2, 47, 64, 100)',
            borderwidth=0
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
    df = pd.read_csv('https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/earthquake.csv')
    df.sort_values('region', ascending=True)
    fig = px.histogram(
        df.loc[df['region'] == region]['magnitude'],
        x='magnitude',
        color_discrete_sequence=['#ff8484'],
    )

    fig.update_layout(
        paper_bgcolor=offWhite,
        title=dict(
            text=f"{region} - Earthquake Magnitude Distribution",
            font=dict(
                size=20,
                color='#022f40',
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
    df = pd.read_csv('https://raw.githubusercontent.com/markusreynoso/datanvi-datasets-server/refs/heads/main/earthquake.csv')
    df = df.loc[df['region'] == region]
    df.groupby('date_time_ph')['magnitude'].count().reset_index()

    fig = px.line(
        df.groupby('date_time_ph')['magnitude'].count().reset_index(),
        x='date_time_ph',
        y='magnitude'
    )

    fig.update_layout(
        paper_bgcolor=offWhite,
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
        line=dict(color='#ff8484')
    )

    return fig



if __name__ == '__main__':
    app.run(debug=True)
