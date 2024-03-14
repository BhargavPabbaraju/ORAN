
from get_data  import Database
from bokeh.models import Div
database = Database()




def dl_mcs_level(doc):
  
    def update():
        
        div.text = database.get_dl_mcs_level()
        div.css_classes=database.button_classes
        div.css_classes = ['btn'] + ['btn-secondary'] + \
                            database.button_classes[2:] 
        


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="",css_classes=database.button_classes)

    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms