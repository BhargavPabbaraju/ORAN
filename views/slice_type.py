
from get_data  import Database
from bokeh.models import Div
database = Database()




def slice_type(doc):
    
    def update():
      
        div.text = database.get_slice_type()


    div = Div(text="")
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms