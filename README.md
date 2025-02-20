# Device Management System

This system is designed to manage devices with the following features:

## Features

### List Display
- Display a list of registered devices
- Export the list to CSV

### New Registration
- Add new device information with the following details:
  - Location name
  - PC/ID
  - Replacement flag for broken devices

### Editing
- Edit the following information of a device:
  - Location name
  - PC/ID
  - Status (Preparing, Waiting for shipment, Waiting for receipt, Received)
  - Release deadline
  - Replacement flag for broken devices

### Deletion
- Delete the information of a registered device

## Setup and Run

1. Clone the repository:
   ```
   git clone https://github.com/jmatsuyama/device_management.git
   ```
2. Navigate to the project directory:
   ```
   cd device_management
   ```
3. Install the required dependencies:
   ```
   npm install
   ```
4. Run the system:
   ```
   npm start
   ```

## Dependencies

- Node.js (version 14.x or higher)
- npm (version 6.x or higher)
