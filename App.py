from flask import Flask, render_template
from views.section1 import section1
from views.section2 import section2
from views.section3 import section3
from views.kpi_graph import kpi_graph
from views.power_graph import power_graph
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.embed import server_document




# Initialize the Flask application

app = Flask(__name__)


@app.route('/', methods=['GET'])
def bkapp_page():
    graphs_script = server_document('http://localhost:5006/graphs')
    return render_template("index.html", graphs_script=graphs_script)

def bk_worker():
    bk_apps = {
        '/graphs': kpi_graph
    }
    server = Server(bk_apps, io_loop=IOLoop(), port=5006, allow_websocket_origin=["localhost:8000", "127.0.0.1:8000"])
    server.start()
    server.io_loop.start()






if __name__ == "__main__":
    # Running flask app instance on port 5000
    from threading import Thread
    Thread(target=bk_worker).start()
    app.run(port=8000)
