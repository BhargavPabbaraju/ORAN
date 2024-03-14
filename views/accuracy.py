
from get_data  import Database
from bokeh.models import Slider,CustomJSTickFormatter
from bokeh.layouts import column


database = Database()



def accuracy(doc):
    
    def update():
        
        # Directly modify the text of 'div'
        value = database.get_accuracy() 
        slider.value = value
        

        
    
    # Initialize 'div' here so that it's in the scope of 'update'
    slider = Slider(start=0,end=100,value=10,bar_color='blue', disabled=True, sizing_mode="scale_width",
                    format=CustomJSTickFormatter(code="return tick.toFixed(2) + '%'"))
    


    #slider.js_on_change('value', callback)
                        

    doc.add_root(slider)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms
        