
from get_data  import Database
from bokeh.models import Div
database = Database()




def interference(doc):
  
    def update():
        
        div.text = str(database.get_policy_and_interference()[1])
       
        


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="")
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms