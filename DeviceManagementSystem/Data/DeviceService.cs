using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DeviceManagementSystem.Models;
using System.Text;
using System.IO;

namespace DeviceManagementSystem.Data
{
    public class DeviceService
    {
        private List<Device> _devices;
        private int _nextId = 1;

        public DeviceService()
        {
            _devices = new List<Device>();
        }

        public List<Device> GetDevices()
        {
            return _devices;
        }

        public Device GetDevice(int id)
        {
            return _devices.FirstOrDefault(d => d.Id == id);
        }

        public void AddDevice(Device device)
        {
            device.Id = _nextId++;
            _devices.Add(device);
        }

        public void UpdateDevice(Device device)
        {
            var existingDevice = _devices.FirstOrDefault(d => d.Id == device.Id);
            if (existingDevice != null)
            {
                var index = _devices.IndexOf(existingDevice);
                _devices[index] = device;
            }
        }

        public void DeleteDevice(int id)
        {
            var device = _devices.FirstOrDefault(d => d.Id == id);
            if (device != null)
            {
                _devices.Remove(device);
            }
        }

        public string ExportToCsv()
        {
            var csv = new StringBuilder();
            
            // ヘッダー行
            csv.AppendLine("ID,箇所名,PC/ID,ステータス,解除期限,故障機交換");
            
            // データ行
            foreach (var device in _devices)
            {
                csv.AppendLine($"{device.Id}," +
                             $"\"{device.Location}\"," +
                             $"\"{device.PcId}\"," +
                             $"{device.Status}," +
                             $"{device.ReleaseDeadline?.ToString("yyyy-MM-dd") ?? ""}," +
                             $"{(device.IsFaultyReplacement ? "はい" : "いいえ")}");
            }
            
            return csv.ToString();
        }
    }
}