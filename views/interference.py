
from get_data  import Database
from bokeh.models import Div
database = Database()




def interference(doc):
  
    def update():
        interfere = database.get_policy_and_interference()[1]
        div.text = str(interfere) if interfere else 'None'
       
        


    # Initialize 'div' here so that it's in the scope of 'update'
    div = Div(text="")
    

    doc.add_root(div)
    doc.add_periodic_callback(update, 500)  # Update every 250 ms