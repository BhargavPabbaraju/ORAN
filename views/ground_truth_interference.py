
from get_data  import Database
from bokeh.models import Div
database = Database()




def ground_truth_interference(doc):
  
    def update():
        interfere = database.get_ground_truth_interference()
        div.text = 'ON' if interfere else 'OFF'
       
        button_class = 'btn-danger' if interfere else 'btn-light'
        div.css_classes = ['btn'] + [button_class] + \
                            database.button_classes[2:] + ['text-dark']
        
        


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="",css_classes=database.button_classes)
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms