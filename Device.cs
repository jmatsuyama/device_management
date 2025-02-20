using System;

namespace DeviceManagementSystem
{
    public class Device
    {
        public int Id { get; set; }
        public string LocationName { get; set; }
        public string PcId { get; set; }
        public DeviceStatus Status { get; set; }
        public DateTime? ReleaseDeadline { get; set; }
        public bool IsReplacementDevice { get; set; }
    }

    public enum DeviceStatus
    {
        InPreparation,    // 準備中
        WaitingForShipment, // 出荷待ち
        WaitingForReceipt,  // 受取待ち
        Received           // 受取済み
    }
}