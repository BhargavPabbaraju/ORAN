
from get_data  import Database
from bokeh.models import Div
database = Database()




def classifier_output(doc):
    
    
    def update():
        # Directly modify the text of 'div'
        div.text = database.get_classifier_output()['output']


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="")
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms