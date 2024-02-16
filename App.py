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

#################
    # create a new plot with a title and axis labels
    kpi1 = figure(title="KPI Graph 1", x_axis_label='x', y_axis_label='y', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi1.line(x, y, legend_label="Temp.", line_width=2, color="red")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi2 = figure(title="KPI Graph 2", x_axis_label='x', y_axis_label='y', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi2.line(x, y, legend_label="Temp.", line_width=2, color="red")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi3 = figure(title="KPI Graph 3", x_axis_label='x', y_axis_label='y', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi3.line(x, y, legend_label="Temp.", line_width=2, color="red")
#################

#################
    # create a new plot with a title and axis labels
    kpi4 = figure(title="KPI Graph 4", x_axis_label='x', y_axis_label='y', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi4.line(x, y, legend_label="Temp.", line_width=2, color="red")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi5 = figure(title="KPI Graph 5", x_axis_label='x', y_axis_label='y', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi5.line(x, y, legend_label="Temp.", line_width=2, color="red")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi6 = figure(title="KPI Graph 6", x_axis_label='x', y_axis_label='y', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi6.line(x, y, legend_label="Temp.", line_width=2, color="red")
#################

    # create a new plot with a title and axis labels
    p7 = figure(title="Power Graph", x_axis_label='x', y_axis_label='y', toolbar_location=None)

    # add a line renderer with legend and line thickness to the plot
    p7.line(x, y, legend_label="Temp.", line_width=2, color="yellow")

    script1, div1 = components(kpi1)
    script2, div2 = components(kpi2)
    script3, div3 = components(kpi3)
    script4, div4 = components(kpi4)
    script5, div5 = components(kpi5)
    script6, div6 = components(kpi6)
    script7, div7 = components(p7)

    # Return all the charts to the HTML template 
    return render_template( 
        template_name_or_list='dashboard.html', 
        script1=script1, div1=div1, 
        script2=script2, div2=div2,
        script3=script3, div3=div3,
        script4=script4, div4=div4,
        script5=script5, div5=div5,
        script6=script6, div6=div6,
        script7=script7, div7=div7

    ) 


# Run the Flask application if this file is executed directly
if __name__ == "__main__":
    # Enable debugging mode for easier troubleshooting (Should be turned off in production)
    app.run(debug=True)
