from flask import Flask
from flask import render_template
from bokeh.plotting import figure
from bokeh.embed import components


# Initialize the Flask application
app = Flask(__name__)

# Define a route for the homepage ("/")
@app.route("/")
def dashboard():

    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # create a new plot with a title and axis labels
    p1 = figure(title="Plot 1", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness to the plot
    p1.line(x, y, legend_label="Temp.", line_width=2, color="red")


    # # show the results
    # show(p)

    script1, div1 = components(p1)

    # Return all the charts to the HTML template 
    return render_template( 
        template_name_or_list='dashboard.html', script1=script1, div1=div1
    ) 


# Run the Flask application if this file is executed directly
if __name__ == "__main__":
    # Enable debugging mode for easier troubleshooting (Should be turned off in production)
    app.run(debug=True)
