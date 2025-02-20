import unittest
from src.device_management import DeviceManagementSystem
from src.device import Device

class TestDeviceManagementSystem(unittest.TestCase):
    def setUp(self):
        self.system = DeviceManagementSystem()

    def test_list_devices(self):
        device1 = Device("Location1", "PC1", True)
        device2 = Device("Location2", "PC2", False)
        self.system.devices = [device1, device2]
        self.system.list_devices()
        self.assertEqual(len(self.system.devices), 2)

    def test_add_device(self):
        self.system.add_device("Location1", "PC1", True)
        self.assertEqual(len(self.system.devices), 1)
        self.assertEqual(self.system.devices[0].location_name, "Location1")
        self.assertEqual(self.system.devices[0].pc_id, "PC1")
        self.assertTrue(self.system.devices[0].replacement_flag)

    def test_edit_device(self):
        device = Device("Location1", "PC1", True)
        self.system.devices = [device]
        self.system.edit_device(device.id, location_name="NewLocation", pc_id="NewPC", status="Received", release_deadline="2023-12-31", replacement_flag=False)
        self.assertEqual(self.system.devices[0].location_name, "NewLocation")
        self.assertEqual(self.system.devices[0].pc_id, "NewPC")
        self.assertEqual(self.system.devices[0].status, "Received")
        self.assertEqual(self.system.devices[0].release_deadline, "2023-12-31")
        self.assertFalse(self.system.devices[0].replacement_flag)

    def test_delete_device(self):
        device1 = Device("Location1", "PC1", True)
        device2 = Device("Location2", "PC2", False)
        self.system.devices = [device1, device2]
        self.system.delete_device(device1.id)
        self.assertEqual(len(self.system.devices), 1)
        self.assertEqual(self.system.devices[0].location_name, "Location2")

if __name__ == '__main__':
    unittest.main()
