
from get_data  import Database
from bokeh.models import Div
database = Database()




def dl_mcs_level(doc):
  
    def update():
        
        div.text = database.get_dl_mcs_level()
       
        


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="")
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms