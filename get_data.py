
import pymongo 
import certifi


def timestamp_to_millis(timestamp_str):
    hh, mm, ss, mmm = map(int, timestamp_str.split(':'))
    return (hh * 3600 + mm * 60 + ss) * 1000 + mmm



class Database:
    def __init__(self,user_name="SenseORAN",password="SenseORANFeb21",cluster="orancluster.5njsvyr"):
        self.uri = f'mongodb+srv://{user_name}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority'
        self.client = pymongo.MongoClient(self.uri,tlsCAFile = certifi.where())

        self.load_csv()

    def load_csv(self,db_name='csv'):
        self.db = self.client[db_name]
        
        self.graph_columns = ["rx_brate uplink [Mbps]","ul_sinr",
           "sum_requested_prbs","tx_brate downlink [Mbps]",
           "ul_mcs","sum_granted_prbs"]
        
        self.graph_x_values = {}
        self.graph_y_values = {}

        for column_name in self.graph_columns:
            column = self.db[column_name]
            for row in column.find():
                data = sorted(row['data'], key=lambda x: x['unix_epoch'])
            
            self.graph_x_values[column_name] = [timestamp_to_millis(timestamp['readable_timestamp'].split(' ')[1]) for timestamp in data]
            self.graph_y_values[column_name] = [signal_value['value'] for signal_value in data]
        

    def get_graph_values(self):
        return self.graph_x_values,self.graph_y_values

    def get_graph_columns(self):
        return self.graph_columns
    

