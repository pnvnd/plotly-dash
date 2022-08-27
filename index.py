from flask import Flask
flaskapp = Flask(__name__, static_url_path="/", static_folder="static", template_folder="templates")

# Navigation
@flaskapp.route("/")
def index():
    return "Hello, world!"

# Get COVID data and plot on chart with Plotly
from covid import covid
flaskapp.register_blueprint(covid)

# Import Plotly Dash application into Flask
from dashboard import init_dashboard
app = init_dashboard(flaskapp)

# This will exceed memory quota on Heroku
# from barchart import init_barchart
# app = init_barchart(flaskapp)

# Run Flask Web Application, new comment
if __name__ == "__main__":
    flaskapp.run()