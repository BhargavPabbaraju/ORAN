
from get_data  import Database
from bokeh.models import Div
database = Database()


def format_class(class_output:str):
    return class_output

def classifier_output(doc):
    data = database.log_data
    
    
    def update():
        # Directly modify the text of 'div'
        current_time = database.current_timestamp
        class_output = data.get(current_time, data[min(data.keys(), key=lambda k: abs(k-current_time))])
        div.text = format_class(class_output)


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="")
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms