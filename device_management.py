import csv
import argparse

# Device data storage
devices = []

# Function to list devices and export to CSV
def list_devices():
    print("Registered Devices:")
    for device in devices:
        print(device)
    
    with open('devices.csv', 'w', newline='') as csvfile:
        fieldnames = ['Location Name', 'PC/ID', 'Replacement Flag', 'Status', 'Release Deadline']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for device in devices:
            writer.writerow(device)
    print("Devices exported to devices.csv")

# Function to register a new device
def register_device(location, pcid, replacement):
    new_device = {
        'Location Name': location,
        'PC/ID': pcid,
        'Replacement Flag': replacement,
        'Status': '',
        'Release Deadline': ''
    }
    devices.append(new_device)
    print("Device registered successfully")

# Function to edit an existing device
def edit_device(location, pcid, status, deadline, replacement):
    for device in devices:
        if device['PC/ID'] == pcid:
            device['Location Name'] = location
            device['Status'] = status
            device['Release Deadline'] = deadline
            device['Replacement Flag'] = replacement
            print("Device edited successfully")
            return
    print("Device not found")

# Function to delete a device
def delete_device(pcid):
    global devices
    devices = [device for device in devices if device['PC/ID'] != pcid]
    print("Device deleted successfully")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Device Management System')
    parser.add_argument('--list', action='store_true', help='List all registered devices')
    parser.add_argument('--register', action='store_true', help='Register a new device')
    parser.add_argument('--edit', action='store_true', help='Edit an existing device')
    parser.add_argument('--delete', action='store_true', help='Delete a registered device')
    parser.add_argument('--location', type=str, help='Location Name')
    parser.add_argument('--pcid', type=str, help='PC/ID')
    parser.add_argument('--replacement', type=str, help='Replacement Flag')
    parser.add_argument('--status', type=str, help='Status')
    parser.add_argument('--deadline', type=str, help='Release Deadline')
    
    args = parser.parse_args()
    
    if args.list:
        list_devices()
    elif args.register:
        if args.location and args.pcid and args.replacement:
            register_device(args.location, args.pcid, args.replacement)
        else:
            print("Missing required fields for registration")
    elif args.edit:
        if args.location and args.pcid and args.status and args.deadline and args.replacement:
            edit_device(args.location, args.pcid, args.status, args.deadline, args.replacement)
        else:
            print("Missing required fields for editing")
    elif args.delete:
        if args.pcid:
            delete_device(args.pcid)
        else:
            print("Missing required field for deletion")
    else:
        print("No valid command provided")

if __name__ == "__main__":
    main()
