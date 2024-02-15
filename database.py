import pandas as pd
import pymongo
import sys
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv


################################## Conneting to MongoDB ############################################# 

# MongoDB connection URI
uri = os.getenv("MONGODB_URI")


try:
  client = pymongo.MongoClient(uri)
  print("succesfully connected to MongoDB")

# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

# use a database named "myDatabase"
db = client.myDatabase

################################## Reading and storing the log file in mongoDB   ############################################# 

# Path to your log file
log_file_path = "data/xapp-logger.log"

log_collection = db['log']

# Read and parse the log file
with open(log_file_path, 'r') as log_file:
    for line in log_file:
        # Split log entry into timestamp, log level, and message
        parts = line.split(" ", 3)
        timestamp_str = f"{parts[0]} {parts[1]}"
        log_level = parts[2]
        message = parts[3].strip()

        # Convert timestamp string to datetime object
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

        # Create a document to insert into MongoDB
        log_entry = {
            "timestamp": timestamp,
            "class": message
        }
         # Insert the document into the MongoDB collection
        log_collection.insert_one(log_entry)



################################## Reading the Excelfile  ############################################# 

df = pd.read_excel("data/1010123456002_metrics.xlsx")
df["TS"] = (df["Timestamp"] / 1000).apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])

# Convert Pandas DataFrame to a list of dictionaries (documents) with the new structure
data_to_insert = [
        {
            "_id": ObjectId(),
            "timestamp": df["Timestamp"].tolist(),
            "values": df[column_name].tolist(),
        }
        for column_name in df.columns[1:]  # Skip the "Timestamp" column
    ]


################################## creating & inserting the collections from the data   ############################################# 

# use a collection named "csv"
my_collection = db["csv"]


# Insert data into MongoDB collection

try: 
 result = my_collection.insert_many(data_to_insert)
 

# return a friendly error if the operation fails
except pymongo.errors.OperationFailure:
  print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
  sys.exit(1)
else:
  inserted_count = len(result.inserted_ids)
  print("I inserted %x documents." %(inserted_count))