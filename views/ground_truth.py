
from get_data  import Database
from bokeh.models import Div
database = Database()




def ground_truth(doc):

    def update():
       
        div.text = database.get_ground_truth()
        div.css_classes=database.button_classes + ['btn-'+database.color_map[div.text]]
        


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="",css_classes=database.button_classes)
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms