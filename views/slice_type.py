
from get_data  import Database
from bokeh.models import Div
database = Database()




def slice_type(doc):
    data = database.get_slice_ids()
    
    
    def update():
        # Directly modify the text of 'div'
        current_time = database.current_timestamp
        slice_id = data.get(current_time, data[min(data.keys(), key=lambda k: abs(k-current_time))])
        div.text = database.get_slice_type_by_id(slice_id)


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="",css_classes=["slice_type"])
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms