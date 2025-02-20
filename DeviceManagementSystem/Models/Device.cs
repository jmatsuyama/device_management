using System;
using System.ComponentModel.DataAnnotations;

namespace DeviceManagementSystem.Models
{
    public class Device
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "箇所名は必須です")]
        public string Location { get; set; }

        [Required(ErrorMessage = "PC/IDは必須です")]
        public string PcId { get; set; }

        public DeviceStatus Status { get; set; }

        public DateTime? ReleaseDeadline { get; set; }

        public bool IsFaultyReplacement { get; set; }
    }

    public enum DeviceStatus
    {
        準備中,
        出荷待ち,
        受取待ち,
        受取済み
    }
}