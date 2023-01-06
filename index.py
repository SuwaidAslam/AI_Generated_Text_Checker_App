import dash_bootstrap_components as dbc
from dash import Dash
from Layout import AppLayout
from AppCallback import AppCallback



styles = [dbc.themes.BOOTSTRAP]
app = Dash(name = __name__, external_stylesheets=styles)
app.title = "Dashboard"
app.config["suppress_callback_exceptions"] = True
server = app.server

layout = AppLayout()
app.layout = layout.getAppLayout()
AppCallback(app)


if __name__ == "__main__":
    app.run_server(debug=False)