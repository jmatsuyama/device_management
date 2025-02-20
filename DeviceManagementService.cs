using System;
using System.Collections.Generic;
using System.Linq;

namespace DeviceManagementSystem
{
    public class DeviceManagementService
    {
        private List<Device> _devices;

        public DeviceManagementService()
        {
            _devices = new List<Device>();
        }

        // 新規登録
        public Device AddDevice(string locationName, string pcId, bool isReplacementDevice)
        {
            var device = new Device
            {
                Id = _devices.Count + 1,
                LocationName = locationName,
                PcId = pcId,
                Status = DeviceStatus.InPreparation,
                IsReplacementDevice = isReplacementDevice
            };

            _devices.Add(device);
            return device;
        }

        // 一覧取得
        public IEnumerable<Device> GetAllDevices()
        {
            return _devices.ToList();
        }

        // 編集
        public bool UpdateDevice(int id, string locationName, string pcId, 
            DeviceStatus status, DateTime? releaseDeadline, bool isReplacementDevice)
        {
            var device = _devices.FirstOrDefault(d => d.Id == id);
            if (device == null)
                return false;

            device.LocationName = locationName;
            device.PcId = pcId;
            device.Status = status;
            device.ReleaseDeadline = releaseDeadline;
            device.IsReplacementDevice = isReplacementDevice;

            return true;
        }

        // 削除
        public bool DeleteDevice(int id)
        {
            var device = _devices.FirstOrDefault(d => d.Id == id);
            if (device == null)
                return false;

            return _devices.Remove(device);
        }

        // デバイスの取得
        public Device GetDevice(int id)
        {
            return _devices.FirstOrDefault(d => d.Id == id);
        }
    }
}