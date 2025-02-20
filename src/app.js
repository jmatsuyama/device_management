document.addEventListener('DOMContentLoaded', () => {
    const deviceList = document.querySelector('#list-display tbody');
    const registrationForm = document.querySelector('#registration-form');
    const editForm = document.querySelector('#edit-form');
    const deleteForm = document.querySelector('#delete-form');
    const exportCsvButton = document.querySelector('#export-csv');

    let devices = [];

    // Fetch devices from JSON file
    fetch('data/devices.json')
        .then(response => response.json())
        .then(data => {
            devices = data;
            displayDevices();
        });

    // Display devices in the table
    function displayDevices() {
        deviceList.innerHTML = '';
        devices.forEach(device => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${device.locationName}</td>
                <td>${device.pcId}</td>
                <td>${device.status}</td>
                <td>${device.releaseDeadline}</td>
                <td>${device.replacementFlag ? 'Yes' : 'No'}</td>
                <td>
                    <button onclick="editDevice('${device.pcId}')">Edit</button>
                    <button onclick="deleteDevice('${device.pcId}')">Delete</button>
                </td>
            `;
            deviceList.appendChild(row);
        });
    }

    // Handle new registration
    registrationForm.addEventListener('submit', event => {
        event.preventDefault();
        const newDevice = {
            locationName: registrationForm['location-name'].value,
            pcId: registrationForm['pc-id'].value,
            status: 'preparing',
            releaseDeadline: '',
            replacementFlag: registrationForm['replacement-flag'].checked
        };
        devices.push(newDevice);
        displayDevices();
        registrationForm.reset();
    });

    // Handle edit device
    editForm.addEventListener('submit', event => {
        event.preventDefault();
        const pcId = editForm['edit-pc-id'].value;
        const device = devices.find(device => device.pcId === pcId);
        if (device) {
            device.locationName = editForm['edit-location-name'].value;
            device.status = editForm['edit-status'].value;
            device.releaseDeadline = editForm['edit-release-deadline'].value;
            device.replacementFlag = editForm['edit-replacement-flag'].checked;
            displayDevices();
            editForm.reset();
        }
    });

    // Handle delete device
    deleteForm.addEventListener('submit', event => {
        event.preventDefault();
        const pcId = deleteForm['delete-pc-id'].value;
        devices = devices.filter(device => device.pcId !== pcId);
        displayDevices();
        deleteForm.reset();
    });

    // Export to CSV
    exportCsvButton.addEventListener('click', () => {
        let csvContent = 'data:text/csv;charset=utf-8,';
        csvContent += 'Location Name,PC/ID,Status,Release Deadline,Replacement Flag\n';
        devices.forEach(device => {
            csvContent += `${device.locationName},${device.pcId},${device.status},${device.releaseDeadline},${device.replacementFlag ? 'Yes' : 'No'}\n`;
        });
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', 'devices.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});
