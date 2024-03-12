from flask import Flask, render_template
from views.kpi_graph import kpi_graph
from views.rbs_assigned import rbs_assigned
from views.classifier_output import classifier_output
from views.slice_type import slice_type
from views.scheduling_policy import scheduling_policy
from views.dl_mcs_level import dl_mcs_level
from views.dl_power_level import dl_power_level
from views.toggle_switch import toggle_switch
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.embed import server_document




# Initialize the Flask application

app = Flask(__name__)


@app.route('/', methods=['GET'])
def bkapp_page():
    graphs_script = server_document('http://localhost:5006/graphs')
    rbs_assigned_script = server_document('http://localhost:5006/rbs_assigned')
    classifier_output_script = server_document('http://localhost:5006/classifier_output')
    scheduling_policy_script = server_document('http://localhost:5006/scheduling_policy')
    toggle_switch_script = server_document('http://localhost:5006/toggle_switch')
    slice_type_script = server_document('http://localhost:5006/slice_type')
    dl_mcs_level_script = server_document('http://localhost:5006/dl_mcs_level')
    dl_power_level_script = server_document('http://localhost:5006/dl_power_level')
    return render_template("index.html", 
                           graphs_script=graphs_script,
                           rbs_assigned_script = rbs_assigned_script,
                           classifier_output_script = classifier_output_script,
                           scheduling_policy_script = scheduling_policy_script,
                           toggle_switch_script = toggle_switch_script,
                           slice_type_script = slice_type_script,
                           dl_mcs_level_script = dl_mcs_level_script,
                           dl_power_level_script = dl_power_level_script,
                           )

def bk_worker():
    bk_apps = {
        '/graphs': kpi_graph,
        '/rbs_assigned' : rbs_assigned,
        '/classifier_output' : classifier_output,
        '/scheduling_policy': scheduling_policy,
        '/toggle_switch': toggle_switch,
        '/slice_type': slice_type,
        '/dl_mcs_level': dl_mcs_level,
        '/dl_power_level': dl_power_level,
    }
    server = Server(bk_apps, io_loop=IOLoop(), port=5006, allow_websocket_origin=["localhost:8000", "127.0.0.1:8000"])
    server.start()
    server.io_loop.start()






if __name__ == "__main__":
    # Running flask app instance on port 5000
    from threading import Thread
    Thread(target=bk_worker).start()
    app.run(port=8000)
