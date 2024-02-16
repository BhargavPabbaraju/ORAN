from flask import Flask
from flask import render_template

from views.section1 import section1
from views.section2 import section2
from views.section3 import section3
from views.kpi_graph import kpi_graph
from views.power_graph import power_graph

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the homepage ("/")
@app.route("/")
def dashboard():
    
    # Call section1 and pass its return values to the template
    section1_data = section1()

    section2_data = section2()
    
    section3_data = section3()

    kpi_graph_data = kpi_graph()

    power_graph_data = power_graph()

    # Return all the charts to the HTML template 
    return render_template( 
        template_name_or_list='dashboard.html',

        script1=kpi_graph_data["script1"],
        script2=kpi_graph_data["script2"],
        script3=kpi_graph_data["script3"],
        script4=kpi_graph_data["script4"],
        script5=kpi_graph_data["script5"],
        script6=kpi_graph_data["script6"],
        script7=power_graph_data["script7"],

        kpi1=kpi_graph_data["kpi1"],
        kpi2=kpi_graph_data["kpi2"],
        kpi3=kpi_graph_data["kpi3"],
        kpi4=kpi_graph_data["kpi4"],
        kpi5=kpi_graph_data["kpi5"],
        kpi6=kpi_graph_data["kpi6"],
        power_graph=power_graph_data["power_graph"],

        ground_truth_url=section1_data['ground_truth_url'], 
        classification_output_url=section1_data['classification_output_url'], 
        ewma_accuracy_url=section1_data['ewma_accuracy_url'],

        power_value=section3_data['power_value'],
        power_percentage=section3_data['power_percentage'],

        rb_value=section2_data['rb_value'],
        throughput_impact=section2_data['throughput_impact'],
        throughput_baseline=section2_data['throughput_baseline'],
        power_impact=section2_data['power_impact'],
        power_baseline=section2_data['power_baseline'],
        schedule_policy=section2_data['schedule_policy'],
    ) 








