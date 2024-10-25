from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

introParagraph = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec at pharetra ante. Vestibulum ut sapien id nibh efficitur pulvinar id in leo. Nullam aliquet, velit at fermentum dictum, neque massa vehicula velit, ac scelerisque nunc mi quis eros. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris finibus volutpat congue. Cras ac gravida dolor. Praesent sed accumsan orci. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Ut porttitor nibh sem, vitae varius orci efficitur eget. Proin tincidunt, nisi et molestie congue, nisi nibh dignissim risus, in malesuada erat massa eu dolor. Vestibulum a quam at libero scelerisque tempus.'

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
        html.Span('Rainfall Levels', id='rainfallLevelsTitle')
    ]),

    html.Div(children=[
        html.P(introParagraph)
    ]),

    html.Div(className='spacer'),

    html.Div(html.H2('Earthquakes')),

    dcc.Dropdown(
        id='quakeDropdown',  # Make sure this ID is referenced in the callback
        className='regionDropdown',
        style={
            'font-family': 'Arial, sans-serif',
            'font-size': '12px',
            'color': '#022f40'
        },
        options=[
            {'label': 'Overall', 'value': 'Overall'},
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
        value='Overall'
    ),

    html.Div(
        style={'background-color': 'red', 'height': '1400px', 'display': 'flex', 'flex-direction': 'column'},
        children=[
            html.Div(
                style={'background-color': 'blue', 'height': '45%', 'display': 'flex', 'flex-direction': 'row'},
                children=[
                    html.Div(
                        style={'background-color': 'yellow', 'width': '40%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
                        children=[
                            dcc.Graph(
                                id='quakePie',
                                style={'width': '100%', 'height': '100%'},
                                figure={}
                            )
                        ]
                    ),
                    dcc.Graph(
                        id='quakeHist',
                        style={'width': '100%', 'height': '100%'},
                        figure={}
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
    ),

    html.Div(id='spacer'),

    html.Div(html.H2('Rainfall')),

    dcc.Dropdown(
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
        value='Overall'
    ),

    html.Br(),
    html.Br(),
    html.Br(),
])


@app.callback(
    Output(component_id='quakePie', component_property='figure'),
    Input(component_id='quakeDropdown', component_property='value')
)
def updateQuakePie(region):
    df = pd.read_csv('datasets/earthquake.csv')
    df.sort_values('region', ascending=True)
    if region == "Overall":
        fig = px.pie(
            df,
            names='region',
            hole=0.8,
        )
    else:
        fig = px.pie(
            df.loc[df['region'] == region].sort_values('region'),
            names='province',
            hole=0.8,
        )

    fig.update_traces(textinfo='none')

    # Move the pie chart up
    fig.update_layout(
        paper_bgcolor='#e6e5e3',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.8,
            xanchor='center',
            x=0.5,
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(255, 255, 255, 0)',
            borderwidth=0
        ),
        margin=dict(t=50, b=50, l=50, r=50)  # Add margin to the layout if needed
    )

    return fig


@app.callback(
    Output(component_id='quakeHist', component_property='figure'),
    Input(component_id='quakeDropdown', component_property='value')
)
def updateQuakeHist(region):
    df = pd.read_csv('datasets/earthquake.csv')
    df.sort_values('region', ascending=True)
    if region == "Overall":
        fig = px.histogram(
            df['magnitude'],
            x='magnitude',
            color_discrete_sequence=['#ff8484']
        )
    else:
        fig = px.histogram(
            df.loc[df['region'] == region]['magnitude'],
            x='magnitude',
            color_discrete_sequence=['#ff8484']
        )

    fig.update_layout(
        paper_bgcolor='#e6e5e3',
    )

    return fig




if __name__ == '__main__':
    app.run(debug=True)
