from dash import dcc, html
import dash_bootstrap_components as dbc


upload_style = {
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
    }

layout=dbc.Container([
        dbc.Row([
            dbc.Col(html.H4("AI Generated Text Detector"), style={'text-align' : 'center'}),
        ]),
        dbc.Row([
            dbc.Col(dcc.Textarea(
                id='text',
                placeholder="Enter Text Here",
                style={'width': '100%', 'height': 500},
            ), width={"size": 6, "offset": 3}),
        ]),
        dbc.Row(
        [
            dbc.Col([
                dcc.Upload(id='upload_file', children=[
                            'Upload File ',
                            html.A('(.txt, .docx, .pdf)'), 
                ], multiple=False,
                    style=upload_style)
            ], width={"size": 6, "offset": 3}),
        ],
        ),
        dbc.Row([
            dbc.Col(html.H5('Real', className="text-info"), width=4, style={'text-align' : 'right'}),
            dbc.Col(dcc.Loading(id='loading',children=html.Div(''),
                type="default"),
                width=4),
            dbc.Col(html.H5('Fake', className="text-danger"), width=4, style={'text-align' : 'left'}),
        ], style={'margin-top' : '20px'}),
        dbc.Row([
            dbc.Col(dbc.Progress(
            [
                dbc.Progress(id="real_prog", value=50, color="info", bar=True),
                dbc.Progress(id="fake_prog", value=50, color="danger", bar=True),
            ], style={'height' : '25px', 'font-size' : '16px'}
            ), width={"size": 6, "offset": 3}),
        ]),
    ])