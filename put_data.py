import pymongo


import certifi
import pandas as pd
from datetime import datetime
import sys

from constants import *


uri = f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}.mongodb.net/?retryWrites=true&w=majority'





try:
  client = pymongo.MongoClient(uri,tlsCAFile = certifi.where())

# return a friendly error if a URI error is thrown
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)


db = client[CSV_FILE_DBNAME]

def convert_unix_epoch_to_readable_timestamp(epoch):
    return datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

try:
    df = pd.read_csv(CSV_FILE_PATH)


    df["TS"] = (df["Timestamp"] / 1000).apply(convert_unix_epoch_to_readable_timestamp)


    # Iterate over columns and create MongoDB documents
    for column_name in df.columns:
        # Skip the "Timestamp" column
        if column_name == "Timestamp" or 'Unnamed' in column_name:
            continue
    # Create a list of dictionaries for the current column
        column_data = []
        for index, row in df.iterrows():
            entry = {
                "unix_epoch": int(row["Timestamp"] / 1000),
                "readable_timestamp": row["TS"],
                "value": row[column_name]
            }
            column_data.append(entry)

        # Create a MongoDB document for the current column
        column_document = {
            "_id": column_name,
            "data": column_data
        }
        my_collection = db[column_name]
        # Insert the document into the MongoDB collection
        my_collection.update_one({"_id": column_name}, {"$set": column_document}, upsert=True)

    print("CSV file inserted successfully.")
    
except Exception as e:
   print(e)



db = client[LOG_FILE_DBNAME]


# Path to your log file


log_collection = db['log']

# Read the log file and create a list of dictionaries
log_entries = []
try:
    with open(LOG_FILE_PATH , "r") as log_file:
        for line in log_file:
            # Assuming each line has the format "timestamp INFO class: message"
            parts = line.strip().split(" ", 3)
            timestamp_str = parts[0] + " " + parts[1]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
            unix_epoch = int(timestamp.timestamp())
            redable_timestamp = timestamp_str.replace(',',':')
            
            log_entry = {
                "readable_timestamp": redable_timestamp,
                "unix_epoch": unix_epoch,
                "class": parts[3]
            }
            log_entries.append(log_entry)

    # Create a MongoDB document with the name "log_file"
    log_document = {
        "_id": "log_file",
        "entries": log_entries
    }

    # Insert the document into the MongoDB collection
    log_collection.insert_one(log_document)
    log_collection.update_one({"_id": "log_file"}, {"$set":log_document}, upsert=True)

    print("Log file inserted successfully.")

except Exception as e:
   print(e)
