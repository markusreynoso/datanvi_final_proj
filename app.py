from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

introParagraph = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec at pharetra ante. Vestibulum ut sapien id nibh efficitur pulvinar id in leo. Nullam aliquet, velit at fermentum dictum, neque massa vehicula velit, ac scelerisque nunc mi quis eros. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris finibus volutpat congue. Cras ac gravida dolor. Praesent sed accumsan orci. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Ut porttitor nibh sem, vitae varius orci efficitur eget. Proin tincidunt, nisi et molestie congue, nisi nibh dignissim risus, in malesuada erat massa eu dolor. Vestibulum a quam at libero scelerisque tempus.'

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children=[
        'An Integrated View of',
        html.Br(),
        'Real Estate Pricing',
        html.Br(),
        'and ',
        html.Span('Seismic Events', style={'color': '#ff8484'})
    ]),

    html.Div(children=[
        html.P(introParagraph)
    ]),

    html.Div(id='spacer'),

    html.Div(
        html.H2('Earthquakes')
    ),

    dcc.Dropdown(
        id='quakesDropdown',
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

    html.Div(
        style={'background-color': 'red', 'height': '900px', 'display': 'flex', 'flex-direction': 'column'},  # Flex column layout
        children=[
            html.Div(
                style={'background-color': 'blue',
                       'height': '45%',
                       'display': 'flex',
                       'flex-direction': 'row'},
                children=[
                    html.Div(
                        style={'background-color': 'yellow',
                               'width': '30%',
                               'display': 'flex',
                               'justify-content': 'center',
                               'align-items': 'center'},
                        children=[
                            # ToDo: Pie Graph
                            dcc.Graph(
                                id='quakePie',
                                style={'width': '100%',
                                       'height': '100%'}
                            )
                        ]
                    ),

                    dcc.Graph(
                        id='quakeHist',
                        style={'width': '100%',
                               'height': '100%'}
                    )
                ]
            ),
            html.Div(
                style={'background-color': 'green', 'height': '55%'}
            )
        ]
    ),

    html.Br(),
    html.Br(),
    html.Br(),
])
if __name__ == '__main__':
    app.run(debug=True)
