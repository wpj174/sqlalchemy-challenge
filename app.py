# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# Home page route
# - List all routes available
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Wether Observation Home page!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/ - This page<br/>"
        f"/api/v1.0/precipitation - Rainfall observations<br/>"
        f"/api/v1.0/stations - Weather observation stations<br/>"
        f"/api/v1.0/tobs - Temperature observations from the most active station for the past year<br/>"
        f"/api/v1.0/<start>[/<end>] - Returns minimum, average and maximum temperatures for the date range (yyyy-mm-dd)<br/>"
    )


# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)
