using System;
using System.ComponentModel.DataAnnotations;

namespace DeviceManagementSystem.Models
{
    public class Device
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "箇所名は必須です")]
        [Display(Name = "箇所名")]
        public string Location { get; set; }

        [Required(ErrorMessage = "PC/IDは必須です")]
        [Display(Name = "PC/ID")]
        public string PcId { get; set; }

        [Display(Name = "ステータス")]
        public DeviceStatus Status { get; set; }

        [Display(Name = "解除期限")]
        [DataType(DataType.Date)]
        public DateTime? ExpirationDate { get; set; }

        [Display(Name = "故障機交換")]
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