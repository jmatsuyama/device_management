# Device Management System

This system is designed to manage devices with the following functionalities:

## Functionalities

1. **List Devices**
   - Displays registered devices.
   - Allows CSV export of the device list.

2. **Register Device**
   - Adds new device information with the following fields:
     - Location Name
     - PC/ID
     - Replacement Flag

3. **Edit Device**
   - Modifies device information with the following fields:
     - Location Name
     - PC/ID
     - Status (Preparing, Waiting for Shipment, Waiting for Receipt, Received)
     - Release Deadline
     - Replacement Flag

4. **Delete Device**
   - Removes registered device information.

## Usage Instructions

### List Devices

To list all registered devices and export them to a CSV file, use the following command:

```python
python device_management.py --list
```

### Register Device

To register a new device, use the following command:

```python
python device_management.py --register --location "Location Name" --pcid "PC/ID" --replacement "Replacement Flag"
```

### Edit Device

To edit an existing device, use the following command:

```python
python device_management.py --edit --location "Location Name" --pcid "PC/ID" --status "Status" --deadline "Release Deadline" --replacement "Replacement Flag"
```

### Delete Device

To delete a registered device, use the following command:

```python
python device_management.py --delete --pcid "PC/ID"
```
