# Device Management System

This system is designed to manage devices with the following features:

## Features

- **List Display**
  - Display a list of registered devices
  - Export the list to CSV format

- **New Registration**
  - Add new device information with the following attributes:
    - Location name
    - PC/ID
    - Replacement flag for faulty devices

- **Editing**
  - Edit the following information of a device:
    - Location name
    - PC/ID
    - Status (Preparing, Waiting for shipment, Waiting for receipt, Received)
    - Release deadline
    - Replacement flag for faulty devices

- **Deletion**
  - Delete the information of a registered device

## Setup and Running

1. Clone the repository:
   ```sh
   git clone https://github.com/jmatsuyama/device_management.git
   cd device_management
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the system:
   ```sh
   python src/device_management.py
   ```

## Usage Instructions

### List Display

To display the list of registered devices, run the following command:
```sh
python src/device_management.py --list
```

To export the list to CSV format, run the following command:
```sh
python src/device_management.py --export
```

### New Registration

To add a new device, run the following command:
```sh
python src/device_management.py --add --location <location_name> --pcid <pc_id> --replacement <true/false>
```

### Editing

To edit a device's information, run the following command:
```sh
python src/device_management.py --edit --id <device_id> --location <location_name> --pcid <pc_id> --status <status> --deadline <release_deadline> --replacement <true/false>
```

### Deletion

To delete a device, run the following command:
```sh
python src/device_management.py --delete --id <device_id>
```
