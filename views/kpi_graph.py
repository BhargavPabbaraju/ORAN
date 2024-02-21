
from bokeh.embed import components



from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,CustomJSTickFormatter

from bokeh.layouts import gridplot
from get_data  import Database


#Connect to the database
database = Database()

graph_columns , x_values,y_values = database.get_graph_columns(),*database.get_graph_values()

window_size = 5  # Number of data points to display at a time
current_index = window_size - 1

def kpi_graph(doc):
    # prepare some data
    sources = {col: ColumnDataSource(data=dict(x=[], y=[])) for col in graph_columns}
    
    def update():
        global current_index
        current_index += 1
        
        for col in graph_columns:
            # Calculate the start and end index for the current window
            if current_index < len(x_values[col]):
                new_x = [x_values[col][current_index]]
                database.set_current_timestamp(new_x[-1])
                new_y = [y_values[col][current_index]]
                new_data = {'x': new_x, 'y': new_y}
                sources[col].stream(new_data, rollover=window_size)
            
                plot = plots_dict[col]
                plot.xaxis.ticker = sources[col].data['x']

        
           
    plots = []
    plots_dict = {}
    for col in graph_columns:
        initial_end_idx = min(window_size, len(x_values[col]))
        initial_data = {
            'x': x_values[col][:initial_end_idx], 
            'y': y_values[col][:initial_end_idx]
        }
        sources[col] = ColumnDataSource(data=initial_data)

        p = figure(output_backend="webgl",title=col, toolbar_location=None,tools=[],width=300, height=250)
        p.toolbar_location = None
        p.line(x='x', y='y', source=sources[col])
        p.xaxis.major_label_orientation = 45
        plots_dict[col] = p
        p.xaxis.formatter = CustomJSTickFormatter(code="""
            var hours = Math.floor(tick / 3600000);
            var minutes = Math.floor((tick % 3600000) / 60000);
            var seconds = Math.floor((tick % 60000) / 1000);
            var millis = tick % 1000;
            return hours.toString().padStart(2, '0') + ':' + 
                   minutes.toString().padStart(2, '0') + ':' + 
                   seconds.toString().padStart(2, '0') + ':' + 
                   millis.toString().padStart(3, '0');
        """)
        plots.append(p)
        
    grid = gridplot([plots[:3], plots[3:]],toolbar_options=dict(logo=None))
    doc.add_root(grid)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms
    