from dash import dcc, html
import dash_bootstrap_components as dbc


class AppLayout:
    def __init__(self):
        self.content =  self.generateContentLayout()
        self.sidebar =  self.generateSidebarLayout()
    

    def generateSidebarLayout(self):
        sidebar = html.Div(
            className='sidebar',
            children=[
                    dbc.Nav([
                            dbc.NavLink("Home", href="/", id="page-1-link", active="exact", style={'text-align' : 'center'}),
                        ], vertical=True, pills=True
                    ),
            ],
            # just remove this and uncomment the style for sidebar in style.css if sidebar needs to be displayed
            style={'display': 'none'}
        )
        return sidebar
    # this method generates content Page Layout
    def generateContentLayout(self):
        content = html.Div(id="page-content", className='content')
        return content
    
    # ------This method generates Overall App's Layout ---------
    def getAppLayout(self):
        layout = html.Div(children=[dcc.Location(id="url", refresh=False), self.sidebar, self.content])
        return layout

    # ------------------ Layout Settings End --------------------