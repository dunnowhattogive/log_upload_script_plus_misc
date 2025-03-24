# Automation Script for Server Upload via SMB

This script processes JSON files containing test results, aggregates the data into Excel files, and uploads the files to an SMB server. The script supports both old and new JSON structures and can aggregate data by month or year.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Required Python packages:
  - `pandas`
  - `openpyxl`
  - `smbprotocol`
  - `matplotlib`

You can install the required packages using pip:

```sh
pip install pandas openpyxl smbprotocol matplotlib
```

## Configuration

The script requires some configuration details to be set. These details are specified at the beginning of the script:

- `BASE_DIR`: The base directory where the JSON files are located.
- `SERVER_URL`: The URL of the server.
- `SERVER_IP`: The IP address of the server.
- `HEADERS`: The authorization headers for the server.
- `SHARE_NAME`: The name of the shared folder on the SMB server.
- `DESTINATION_PATH`: The path within the share to upload the file.
- `USERNAME`: The username for authentication.
- `PASSWORD`: The password for authentication.
- `SERVER_NAME`: The hostname or NetBIOS name of the SMB server.

## Running the Script

### Basic Usage

To run the script with default settings, navigate to the directory containing the script and execute:

```sh
./server_upload_smb.py
```

### Custom Directory

To process JSON files in a custom directory, provide the directory path as an argument:

```sh
./server_upload_smb.py /path/to/custom/directory
```

### Yearly Aggregation

To aggregate data by year, use the `--yearly` flag followed by the custom directory path (if any):

```sh
./server_upload_smb.py --yearly /path/to/custom/directory
```

### New JSON Structure

To process JSON files with the new structure, use the `--battery-test` flag. On Windows machines, the script will look for JSON files in the `current_measurement_test_<Device name>` directory inside the `Documents` folder.

```sh
./server_upload_smb.py --battery-test
```

### Default Directory on Windows

By default, the script looks for JSON files in the `C:\Users\<YourUsername>\Documents\current_measurement_test_<Device name>` directory on Windows machines. Ensure that this path is accessible and contains the JSON files to be processed.

### Default Directory on Linux

By default, the script looks for JSON files in the `/home/<YourUsername>/Documents/current_measurement_test_<Device name>` directory on Linux machines. Ensure that this path is accessible and contains the JSON files to be processed.

### Combined Options

You can combine the options as needed. For example, to process JSON files in a custom directory with yearly aggregation and the new JSON structure:

```sh
./server_upload_smb.py --yearly /path/to/custom/directory --battery-test
```

### Running the Script on Windows

To run the script on Windows, open Command Prompt or PowerShell, navigate to the directory containing the script, and execute:

```sh
python server_upload_smb.py
```

## Scheduling the Script

### Scheduling on Linux

To schedule the script to run once every week (Sunday at 22:30), you can use `cron`. Open the crontab file for editing:

```sh
crontab -e
```

Add the following line to the crontab file:

```sh
30 22 * * 0 /usr/bin/python3 /home/vikas/Projects/Anticimex/automation/server_upload_smb.py
```

### Scheduling on Windows

To schedule the script to run once every week (Sunday at 22:30), you can use Task Scheduler:

1. Open Task Scheduler.
2. Click on "Create Basic Task".
3. Follow the wizard to set the name and description.
4. Choose "Weekly" and set the day to Sunday and the time to 22:30.
5. Choose "Start a Program" and browse to the Python executable (e.g., `C:\Python39\python.exe`).
6. Add the script path (e.g., `C:\path\to\server_upload_smb.py`) as an argument.
7. Finish the wizard to create the task.

## Logging

The script logs messages to both syslog (or Windows Event Log) and the console. The log messages include information and error messages to help you track the script's progress and troubleshoot any issues.

## Example JSON File

Here is an example of a JSON file that the script processes:

```json
{
  "number_of_tests": 1,
  "0": {
    "all_data_dev": 6.5337718007526675,
    "all_data_mean": 7.535710446699999,
    "current_result": "PASSED",
    "current_ua": 6.395607846082475,
    "current_ua_std": 0.8196201082032101,
    "location": "Smart Catch mini",
    "raw_data": [
      6.297284179999999,
      6.2383612,
      6.29935153,
      6.30966985,
      6.255805779999999,
      45.0953052,
      6.28089287,
      6.28077302,
      6.24747184,
      6.3262271000000005,
      6.27543294,
      6.19768485,
      6.33343863,
      6.26957199,
      6.27386802,
      6.28877508,
      6.2317005,
      6.24892613,
      6.31021838,
      6.29060735,
      6.2690442,
      6.36058616,
      6.3728612,
      6.25977915,
      6.30202272,
      6.198496120000001,
      6.26323395,
      6.2886413999999995,
      6.29802861,
      6.2790583,
      6.24667209,
      6.2932416600000005,
      6.237796540000001,
      6.285481610000001,
      6.26760143,
      6.31378381,
      6.29686932,
      43.6438237,
      6.3572535100000005,
      6.27626726,
      6.2280451900000005,
      6.29440325,
      6.29598661,
      6.329059630000001,
      6.36948246,
      6.30183143,
      6.37370013,
      6.2707704500000006,
      6.18681339,
      6.3583666999999995,
      6.3010409,
      6.337543370000001,
      6.27008133,
      44.4579547,
      6.30082887,
      6.30708163,
      6.37381767,
      6.38140027,
      6.27608979,
      6.27065521,
      6.305659599999999,
      6.34153518,
      6.2709917100000006,
      6.377120359999999,
      6.35392316,
      6.29599122,
      6.32577998,
      6.23834046,
      6.2925387200000005,
      7.659164120000001,
      6.29270466,
      6.28920607,
      6.3457759,
      6.34252852,
      6.29346983,
      6.32284605,
      6.33321738,
      6.36873111,
      6.252583749999999,
      6.31556768,
      6.30317509,
      6.28225497,
      6.27552283,
      6.37656492,
      6.34741688,
      14.3019266,
      6.3295182699999994,
      6.256262120000001,
      6.36150806,
      6.27637558,
      6.29328315,
      6.32431878,
      6.26255175,
      6.32100226,
      6.29775665,
      6.35717054,
      6.34100509,
      6.33429138,
      6.28263064,
      6.28197149
    ],
    "test_result": "PASSED",
    "tester": "js",
    "timestamp_begin": 1709195804,
    "timestamp_end": 1709195816,
    "voltage_mv": 3669.8314299999997,
    "voltage_result": "PASSED"
  }
}
```

## Troubleshooting

If you encounter any issues, check the log messages for more information. Common issues include:

- Missing or incorrect configuration details.
- Incorrect file paths or directory structure.
- Issues with SMB server connectivity or authentication.

If you need further assistance, please refer to the documentation for the relevant Python packages or contact your system administrator.
