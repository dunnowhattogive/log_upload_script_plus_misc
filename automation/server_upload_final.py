import os
import json
import pandas as pd
import requests
import socket
import uuid
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open, CreateDisposition, FileAttributes, ImpersonationLevel, ShareAccess, CreateOptions
from datetime import datetime

# Configure base directory and server details
BASE_DIR = os.path.expanduser("~/Documents/")
SERVER_URL = "172.22.41.14/AICPROD-FILE01/DATA"  # Replace with your server URL
SERVER_IP = "172.21.41.14"
HEADERS = {"Authorization": "SVC_FileExport@aicprod.local Ju$5LKEbreU!"}  # Replace with your API token or authentication header

# SMB server details
SERVER_NAME = "FILE01.AICPROD.LOCAL"
SHARE_NAME = "\AICPROD-FILE01\Data$\AIC-Helsinge"
DESTINATION_PATH = "SMART_CATCH_MINI"
# USERNAME = "SVC_FileExport@aicprod.local"
USERNAME = "aicprod\SVC_FileExport"
PASSWORD = "Ju$5LKEbreU!"
SERVER_IP = "172.22.41.14"


def parse_test_data(test_data):
    """Parse the structured test data into a flat dictionary."""
    parsed_data = {
        "Device Type": test_data.get("devicetype"),
        "Firmware Version": test_data.get("firmwareversion"),
        "Hardware Info": test_data.get("hardwareinfo"),
    }
    tests = ["power_up", "connect", "pirtest", "factorymode", "delete", "PRODUCT_INFO"]
    
    for test in tests:
        if test in test_data:
            test_info = test_data[test]
            if isinstance(test_info.get("results"), list):
                parsed_data[f"{test} Results"] = ", ".join(test_info["results"])
            else:
                parsed_data[f"{test} Results"] = test_info.get("results")
            parsed_data[f"{test} Failures"] = test_info.get("number_of_fails", "N/A")
            parsed_data[f"{test} Timestamp Start"] = test_info.get("timestamp_begin")
            parsed_data[f"{test} Timestamp End"] = test_info.get("timestamp_end")
    
    return parsed_data

def convert_json_to_xlsx(json_path, xlsx_path):
    """Converts JSON file to a methodical Excel sheet."""
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        # Parse all tests
        records = []
        for test_id in range(data["number_of_tests"]):
            if str(test_id) in data:
                records.append(parse_test_data(data[str(test_id)]))
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        df.to_excel(xlsx_path, index=False)
        print(f"Converted {json_path} to {xlsx_path}")
        return True
    except Exception as e:
        print(f"Failed to convert {json_path}: {e}")
        return False

def upload_file(file_path):
    """Uploads a file to the server with enhanced error handling."""
    try:
        with open(file_path, 'rb') as file:
            print(f"Attempting to upload {file_path} to {SERVER_URL}")
            response = requests.post(SERVER_URL, files={"file": file}, headers=HEADERS, timeout=30)

        if response.status_code == 200:
            print(f"Uploaded {file_path} successfully.")
        else:
            print(f"Failed to upload {file_path}. Status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.ConnectTimeout:
        print(f"Connection timed out while uploading {file_path}. Check server availability.")
    except requests.exceptions.RequestException as e:
        print(f"Error uploading {file_path}: {e}")

def upload_file_tcp(file_path, server_ip, server_port):
    """Uploads a file to the server using a TCP socket."""
    try:
        # Open a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to the server
            print(f"Connecting to TCP server {server_ip}:{server_port}")
            sock.connect((server_ip, server_port))

            # Read and send the file content
            with open(file_path, 'rb') as file:
                print(f"Uploading {file_path} via TCP")
                while chunk := file.read(1024):  # Read in 1KB chunks
                    sock.sendall(chunk)

            # Notify completion
            print(f"File {file_path} uploaded successfully via TCP")
    except Exception as e:
        print(f"Error during TCP upload: {e}")

def upload_file_smb(file_path, server_name, share_name, destination_path, username, password, server_ip, domain="", port=139):
    """
    Uploads a file to an SMB share.

    Parameters:
    - file_path: Local path of the file to be uploaded.
    - server_name: Name of the SMB server.
    - share_name: Name of the shared folder on the SMB server.
    - destination_path: Path within the share to upload the file.
    - username: Username for authentication.
    - password: Password for authentication.
    - server_ip: IP address of the SMB server.
    - domain: Domain for authentication (optional).
    - port: Port for SMB (default is 139).
    """
    try:
        # Establish SMB connection
        conn = SMBConnection(username, password, "local_machine_name", server_name, domain=domain, use_ntlm_v2=True)
        assert conn.connect(server_ip, port), "SMB connection failed!"

        # Upload file
        with open(file_path, 'rb') as file:
            remote_file_path = f"{destination_path}/{file_path.split('/')[-1]}"
            conn.storeFile(share_name, remote_file_path, file)

        print(f"File {file_path} uploaded successfully to {remote_file_path} on {server_name}")
        conn.close()
    except Exception as e:
        print(f"Error uploading {file_path} via SMB: {e}")


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
            
            if convert_json_to_xlsx(json_path, xlsx_path):
                # upload_file(xlsx_path)
                # upload_file_tcp(xlsx_path,)
                upload_file_smb(xlsx_path, SERVER_NAME, SHARE_NAME, DESTINATION_PATH, USERNAME, PASSWORD, SERVER_IP)

if __name__ == "__main__":
    process_directory()

