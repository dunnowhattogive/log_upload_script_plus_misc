import os
import json
import pandas as pd
import requests
import socket
from datetime import datetime

# Configure base directory and server details
BASE_DIR = os.path.expanduser("~/Documents/")
SERVER_URL = "https://example.com/upload"  # Replace with your server URL
HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}  # Replace with your API token or authentication header

def convert_json_to_xlsx(json_path, xlsx_path):
    """Converts a JSON file to an Excel file."""
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Convert JSON data to a pandas DataFrame
        df = pd.DataFrame(data if isinstance(data, list) else [data])
        
        # Save the DataFrame to an Excel file
        df.to_excel(xlsx_path, index=False)
        print(f"Converted {json_path} to {xlsx_path}")
        return True
    except Exception as e:
        print(f"Failed to convert {json_path}: {e}")
        return False

def upload_file(file_path):
    """Uploads a file to the server."""
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(SERVER_URL, files={"file": file}, headers=HEADERS)
        
        if response.status_code == 200:
            print(f"Uploaded {file_path} successfully.")
        else:
            print(f"Failed to upload {file_path}. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

def process_directory():
    """Processes JSON files in the directory structure."""
    today = datetime.now()
    dir_path = os.path.join(BASE_DIR,"node_distributed_test_" + socket.gethostname(), today.strftime("%Y"), today.strftime("%m"), today.strftime("%d"))
    
    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} does not exist.")
        return
    
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".json"):
            json_path = os.path.join(dir_path, file_name)
            xlsx_path = os.path.splitext(json_path)[0] + ".xlsx"
            print(xlsx_path)
            if convert_json_to_xlsx(json_path, xlsx_path):
                upload_file(xlsx_path)

if __name__ == "__main__":
    process_directory()

