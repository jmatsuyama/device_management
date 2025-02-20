using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace DeviceManagementSystem
{
    public class CsvExporter
    {
        public static void ExportToCsv(IEnumerable<Device> devices, string filePath)
        {
            var csvLines = new List<string>
            {
                // ヘッダー行
                "ID,箇所名,PC/ID,ステータス,解除期限,故障機交換"
            };

            foreach (var device in devices)
            {
                var line = string.Join(",",
                    device.Id,
                    EscapeCsvField(device.LocationName),
                    EscapeCsvField(device.PcId),
                    GetStatusText(device.Status),
                    device.ReleaseDeadline?.ToString("yyyy/MM/dd") ?? "",
                    device.IsReplacementDevice ? "はい" : "いいえ"
                );
                csvLines.Add(line);
            }

            File.WriteAllLines(filePath, csvLines, Encoding.UTF8);
        }

        private static string EscapeCsvField(string field)
        {
            if (string.IsNullOrEmpty(field)) return "";
            if (field.Contains(",") || field.Contains("\"") || field.Contains("\n"))
            {
                return $"\"{field.Replace("\"", "\"\"")}\"";
            }
            return field;
        }

        private static string GetStatusText(DeviceStatus status)
        {
            return status switch
            {
                DeviceStatus.InPreparation => "準備中",
                DeviceStatus.WaitingForShipment => "出荷待ち",
                DeviceStatus.WaitingForReceipt => "受取待ち",
                DeviceStatus.Received => "受取済み",
                _ => "不明"
            };
        }
    }
}