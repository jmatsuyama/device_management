import csv
import argparse
from device import Device

class DeviceManagementSystem:
    def __init__(self):
        self.devices = []

    def list_devices(self):
        for device in self.devices:
            print(device)

    def export_devices_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Location Name', 'PC/ID', 'Replacement Flag', 'Status', 'Release Deadline'])
            for device in self.devices:
                writer.writerow([device.location_name, device.pc_id, device.replacement_flag, device.status, device.release_deadline])

    def add_device(self, location_name, pc_id, replacement_flag):
        new_device = Device(location_name, pc_id, replacement_flag)
        self.devices.append(new_device)

    def edit_device(self, device_id, location_name=None, pc_id=None, status=None, release_deadline=None, replacement_flag=None):
        for device in self.devices:
            if device.id == device_id:
                if location_name:
                    device.location_name = location_name
                if pc_id:
                    device.pc_id = pc_id
                if status:
                    device.status = status
                if release_deadline:
                    device.release_deadline = release_deadline
                if replacement_flag is not None:
                    device.replacement_flag = replacement_flag
                break

    def delete_device(self, device_id):
        self.devices = [device for device in self.devices if device.id != device_id]

def main():
    parser = argparse.ArgumentParser(description='Device Management System')
    parser.add_argument('--list', action='store_true', help='List all devices')
    parser.add_argument('--export', type=str, help='Export devices to CSV file')
    parser.add_argument('--add', action='store_true', help='Add a new device')
    parser.add_argument('--edit', action='store_true', help='Edit an existing device')
    parser.add_argument('--delete', action='store_true', help='Delete a device')
    parser.add_argument('--location', type=str, help='Location name of the device')
    parser.add_argument('--pcid', type=str, help='PC/ID of the device')
    parser.add_argument('--replacement', type=bool, help='Replacement flag for faulty devices')
    parser.add_argument('--id', type=int, help='ID of the device to edit or delete')
    parser.add_argument('--status', type=str, help='Status of the device')
    parser.add_argument('--deadline', type=str, help='Release deadline of the device')

    args = parser.parse_args()
    system = DeviceManagementSystem()

    if args.list:
        system.list_devices()
    elif args.export:
        system.export_devices_to_csv(args.export)
    elif args.add:
        if args.location and args.pcid and args.replacement is not None:
            system.add_device(args.location, args.pcid, args.replacement)
        else:
            print("Please provide location, PC/ID, and replacement flag for the new device.")
    elif args.edit:
        if args.id:
            system.edit_device(args.id, args.location, args.pcid, args.status, args.deadline, args.replacement)
        else:
            print("Please provide the ID of the device to edit.")
    elif args.delete:
        if args.id:
            system.delete_device(args.id)
        else:
            print("Please provide the ID of the device to delete.")

if __name__ == '__main__':
    main()
