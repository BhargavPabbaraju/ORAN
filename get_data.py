
import pymongo 
import certifi

from constants import *


def timestamp_to_millis(timestamp_str):
    hh, mm, ss, mmm = map(int, timestamp_str.split(':'))
    return (hh * 3600 + mm * 60 + ss) * 1000 + mmm


def format_class_output(class_output:str):
    output = class_output.split(" ")[0]
    if output == 'unexpected':
        output = class_output.split(":")[1].split(" ")[1]
    if output == 'cntrl':
        output = 'MMTC'
    if output == 'embb':
        return 'eMBB'
    
    return output.upper()

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self,user_name="SenseORAN",password="SenseORANFeb21",cluster="orancluster.5njsvyr"):
        if hasattr(self, 'uri'):  # Check if instance already initialized
            return
        
        self.uri = f'mongodb+srv://{user_name}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority'
        self.client = pymongo.MongoClient(self.uri,tlsCAFile = certifi.where())

        self.current_timestamp = 0

        self.current_index = 0

        self.load_csv()
        self.load_log_file()

        self.scheduling_policy_map = {
            0:"Round Robin",
            1:"Water Filling",
            2:"Proportionally Fair"
        }

        self.slice_type_map = {
            0:"MMTC",
            1:"URLLC",
            2:"eMBB"
        }

        self.ground_truths_map = {
            'EU' : ['eMBB','MMTC'],
            'EM' : ['eMBB','MMTC'],
            'UE' : ['URLLC','MMTC'],
            'UM' : ['URLLC','MMTC'],
            'ME' : ['MMTC','eMBB'],
            'MU' : ['MMTC','URLLC'],
            'MU' : ['MMTC','URLLC'],
            

        }

        self.color_map = {
            'eMBB':'success',
            'URLLC':'primary',
            'MMTC': 'warning',
        }

        self.selected_db = DBNAME[:2]

        self.accurately_predicted_indices = set()
        self.accuracy = 0

        self.button_classes = ['btn',
                            'd-flex', 'font-weight-bold', 'justify-content-center',
                              'align-middle', 'align-self-center' ,'col-12']



    def load_log_file(self,db_name=LOG_FILE_DBNAME):
        self.db = self.client[db_name]
        for row in self.db['log'].find():
            data = sorted(row['entries'], key=lambda x: x['unix_epoch'])
        
        self.log_data = {}
        for record in data:
            timestamp = timestamp_to_millis(record['readable_timestamp'].split(' ')[1])
            self.log_data[timestamp] = record['class']
        

    def load_other_csv_columns(self,db,column_name):
        output_dic = {}
        for row in db[column_name].find():
            data = sorted(row['data'], key=lambda x: x['unix_epoch'])
        
        for record in data:
            timestamp = timestamp_to_millis(record['readable_timestamp'].split(' ')[1])
            output_dic[timestamp] = record['value']
        
        return output_dic
    

    def format_column_name(self,column_name):
        column_name = column_name.replace('sum_','').replace(' [Mbps]','').replace('_',' ')
        word_groups = column_name.split(" ")

        
        
        
        for i in range(len(word_groups)):
            #All these words should be completely capialized like SINR
            if word_groups[i] in ['rx','dl','prb','tx','sinr','mcs']:
                word_groups[i] = word_groups[i].upper()
            elif word_groups[i] == 'brate':
                word_groups[i] = 'Bitrate'
            else:
                word_groups[i] = word_groups[i][0].upper() + word_groups[i][1:]
            
        if 'Prbs' in word_groups:
            return 'PRB '+word_groups[0]
        
        return " ".join(word_groups)
      

    def load_csv(self,db_name=CSV_FILE_DBNAME):
        self.db = self.client[db_name]
        
        self.graph_columns = ["rx_brate uplink [Mbps]","ul_sinr",
           "sum_requested_prbs","tx_brate downlink [Mbps]",
           "dl_mcs","sum_granted_prbs"]
        
        self.graph_x_values = {}
        self.graph_y_values = {}

        for column_name in self.graph_columns:
            column = self.db[column_name]
            for row in column.find():
                data = sorted(row['data'], key=lambda x: x['unix_epoch'])
            
            self.graph_x_values[self.format_column_name(column_name)] = [timestamp_to_millis(timestamp['readable_timestamp'].split(' ')[1]) for timestamp in data]
            self.graph_y_values[self.format_column_name(column_name)] = [signal_value['value'] for signal_value in data]

        self.rbs_assigned = self.load_other_csv_columns(self.db,'slice_prb')

        self.total_records = len(self.rbs_assigned)
        

        self.scheduling_policy = self.load_other_csv_columns(self.db,'scheduling_policy')

        self.slice_ids = self.load_other_csv_columns(self.db,'slice_id')

        self.graph_columns = [self.format_column_name(column_name) for column_name in self.graph_columns]
        


    def map_scheduling_policy(self,policy):
        if policy == "":
            return ""

        
        return self.scheduling_policy_map[policy]
        

    def set_current_index(self,current_index):
        self.current_index = current_index
        self.calculate_accuracy()

    def get_graph_values(self):
        return self.graph_x_values,self.graph_y_values

    def get_graph_columns(self):
        return self.graph_columns

    def get_rbs_assigned(self):
        return self.get_current_timestamp_data(self.rbs_assigned)

    def get_scheduling_policy(self):
        policy = self.get_current_timestamp_data(self.scheduling_policy)
        return self.scheduling_policy_map[policy]

    def get_slice_type(self):
        slice_id = self.get_current_timestamp_data(self.slice_ids)
        return self.slice_type_map[slice_id]

   
    
    def set_current_timestamp(self,timestamp):
        self.current_timestamp = timestamp
        
    

    def get_current_timestamp_data(self,data):
        #Returns the data with a timestamp closest to the current timestamp
        return data.get(self.current_timestamp, data[min(data.keys(), key=lambda k: abs(k-self.current_timestamp))])


    def get_classifier_output(self):
        class_output = self.get_current_timestamp_data(self.log_data).strip()
        if "with interference" in class_output:
            interference = True
        else:
            interference = False

        return {
            'output':format_class_output(class_output),
            'interference':interference,
            }
        
    
    def get_policy_and_interference(self):
        interfere = self.get_classifier_output()['interference']
        scheduling_policy = self.get_current_timestamp_data(self.scheduling_policy)

        return scheduling_policy,interfere

    def get_dl_mcs_level(self):
        policy, interfere = self.get_policy_and_interference()
        if type(interfere)!=bool:
            return interfere
        
        if policy == 1 or policy == 2 and interfere:
            return "Auto"
        elif policy == 1 or policy == 2 and not interfere:
            return "High(64 QAM)"
        
        elif policy == 0 and interfere:
            return "Low(QPSK)"
        elif policy == 0 and not interfere:
            return "Medium(16 QAM)"
        
        else:
            return f'G={policy} Interefer={str(interfere)[0]}'
            #return "Unexpected"
    
    def get_dl_power_level(self):
        policy, interfere = self.get_policy_and_interference()
        if type(interfere)!=bool:
            return interfere
        
        if not interfere or policy == 0:
            return "Medium"
        elif policy == 1 or policy == 2 and interfere:
            return "High"
        else:
            return f'G={policy} Interefer={str(interfere)[0]}'
            #return "Unexpected Result"

    def get_ground_truth(self):
        if self.current_index < self.total_records // 2:
            truth_index = 0
        else:
            truth_index = 1
        
        ground_truth = self.ground_truths_map[self.selected_db][truth_index]
        
        

        return ground_truth

    def calculate_accuracy(self):
        class_output = self.get_classifier_output()['output']
        ground_truth = self.get_ground_truth()
        if ground_truth == class_output:
            self.accurately_predicted_indices.add(self.current_index)
        
        #print(self.accuracy,len(self.accurately_predicted_indices),self.current_index,ground_truth,class_output)

    def get_accuracy(self):
        return len(self.accurately_predicted_indices) / self.total_records * 100
