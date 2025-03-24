import uuid
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open, CreateDisposition, FileAttributes, ImpersonationLevel, ShareAccess, CreateOptions

def upload_file_smb(file_path, server_name, share_name, destination_path, username, password, port=445):
    """
    Uploads a file to an SMB share using smbprotocol.

    Parameters:
    - file_path: Local path of the file to be uploaded.
    - server_name: Hostname or NetBIOS name of the SMB server.
    - share_name: Name of the shared folder on the SMB server.
    - destination_path: Path within the share to upload the file.
    - username: Username for authentication.
    - password: Password for authentication.
    - port: Port for SMB (default is 445).
    """
    try:
        # Step 1: Establish an SMB connection with a unique GUID
        print(f"Connecting to SMB server {server_name} on port {port}...")
        conn = Connection(server_name=server_name, port=port, guid=uuid.uuid4())
        conn.connect()

        # Step 2: Start a session
        session = Session(connection=conn, username=username, password=password)
        session.connect()

        # Step 3: Connect to the SMB share
        tree = TreeConnect(session=session, share_name=f"\\\\{server_name}\\{share_name}")
        tree.connect()

        # Step 4: Resolve the remote file path
        destination_file_path = f"{destination_path}\\{file_path.split('/')[-1]}"

        # Step 5: Open a file handle for uploading
        file_handle = Open(tree, destination_file_path)
        file_handle.create(
            create_disposition=CreateDisposition.FILE_OVERWRITE_IF,
            file_attributes=FileAttributes.FILE_ATTRIBUTE_NORMAL,
            desired_access=0x001201BF,  # File write access
            impersonation_level=ImpersonationLevel.Impersonation,
            share_access=ShareAccess.FILE_SHARE_WRITE | ShareAccess.FILE_SHARE_READ,
            create_options=CreateOptions.FILE_NON_DIRECTORY_FILE
        )

        # Step 6: Read and write the file in chunks
        print(f"Uploading {file_path} to {destination_file_path}...")
        with open(file_path, "rb") as file:
            offset = 0
            while chunk := file.read(1024):  # Read in 1KB chunks
                file_handle.write(chunk, offset=offset)
                offset += len(chunk)

        # Step 7: Close the file handle
        file_handle.close()
        print(f"File {file_path} uploaded successfully to {destination_file_path}")

        # Step 8: Disconnect resources
        tree.disconnect()
        session.disconnect()
        conn.disconnect()

    except Exception as e:
        print(f"Error uploading {file_path} via SMB: {e}")



# SMB server details
# SERVER_IP = "192.168.1.10"
SERVER_IP = "172.22.41.14"
# SHARE_NAME = "shared_folder"
SHARE_NAME = "AIC-Helsinge"
# DESTINATION_PATH = "uploads"
DESTINATION_PATH = "SMART_CATCH_MINI"
# USERNAME = "your_username"
# USERNAME = "SVC_FileExport@aicprod.local"
USERNAME = "aicprod\AIC-SVC_FileExport"
# PASSWORD = "your_password"
PASSWORD = "Ju$5LKEbreU!"

# SMB server details
SERVER_NAME = "AICPROD-FILE01"
# SERVER_NAME = socket.gethostname()

# File to upload
# FILE_PATH = "/path/to/your/file.xlsx"
FILE_PATH = "/home/vikas/Documents/node_distributed_test_vikas-Sigma-Anticimex/2024/12/04/00124B003430DA89.xlsx"

# Upload file via SMB
upload_file_smb(FILE_PATH, SERVER_NAME, SHARE_NAME, DESTINATION_PATH, USERNAME, PASSWORD)





