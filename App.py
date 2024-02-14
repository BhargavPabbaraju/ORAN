from flask import Flask
from flask import render_template

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the homepage ("/")
@app.route("/")
def dashboard():
    """
    Route to render the dashboard.html template.

    :return: HTML rendered using the dashboard.html template.
    """
    return render_template("dashboard.html")

# Run the Flask application if this file is executed directly
if __name__ == "__main__":
    # Enable debugging mode for easier troubleshooting (Should be turned off in production)
    app.run(debug=True)
