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

    html.Div(
        style={'background-color': 'red', 'height': '700px', 'display': 'flex'},
        children=[
            html.Div(
                style={'background-color': 'blue',
                       'width': '30%'}
            ),
            html.Div(
                style={'background-color': 'green',
                       'width': '70%'}
            )
        ]
    ),

    dcc.Dropdown(
        id='quakesDropdown'
    ),

    html.Br(),
    html.Br(),
    html.Br(),

    html.Center(
        dcc.Graph(
            id='graph1',
            className='wideGraph'
        )
    )
])

if __name__ == '__main__':
    app.run(debug=True)
