
from get_data  import Database
from bokeh.models import Slider
import random
database = Database()



def accuracy(doc):
    
    
    def update():
        
        # Directly modify the text of 'div'
        slider.value = database.get_accuracy()
        
        

    # Initialize 'div' here so that it's in the scope of 'update'
    slider = Slider(start=0,end=100,value=10,bar_color='blue', disabled=True, sizing_mode="scale_width")
    

    doc.add_root(slider)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms
        