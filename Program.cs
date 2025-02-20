using System;
using System.Linq;

namespace DeviceManagementSystem
{
    class Program
    {
        private static DeviceManagementService _deviceService;

        static void Main(string[] args)
        {
            _deviceService = new DeviceManagementService();
            
            while (true)
            {
                ShowMenu();
                var choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        ListDevices();
                        break;
                    case "2":
                        AddDevice();
                        break;
                    case "3":
                        EditDevice();
                        break;
                    case "4":
                        DeleteDevice();
                        break;
                    case "5":
                        ExportToCsv();
                        break;
                    case "6":
                        Console.WriteLine("アプリケーションを終了します。");
                        return;
                    default:
                        Console.WriteLine("無効な選択です。もう一度お試しください。");
                        break;
                }
            }
        }

        private static void ShowMenu()
        {
            Console.WriteLine("\n=== 端末管理システム ===");
            Console.WriteLine("1. 端末一覧表示");
            Console.WriteLine("2. 新規端末登録");
            Console.WriteLine("3. 端末情報編集");
            Console.WriteLine("4. 端末削除");
            Console.WriteLine("5. CSV出力");
            Console.WriteLine("6. 終了");
            Console.Write("選択してください (1-6): ");
        }

        private static void ListDevices()
        {
            var devices = _deviceService.GetAllDevices().ToList();
            if (!devices.Any())
            {
                Console.WriteLine("登録されている端末はありません。");
                return;
            }

            Console.WriteLine("\n=== 登録端末一覧 ===");
            foreach (var device in devices)
            {
                Console.WriteLine($"ID: {device.Id}");
                Console.WriteLine($"箇所名: {device.LocationName}");
                Console.WriteLine($"PC/ID: {device.PcId}");
                Console.WriteLine($"ステータス: {GetStatusText(device.Status)}");
                Console.WriteLine($"解除期限: {device.ReleaseDeadline?.ToString("yyyy/MM/dd") ?? "未設定"}");
                Console.WriteLine($"故障機交換: {(device.IsReplacementDevice ? "はい" : "いいえ")}");
                Console.WriteLine("-------------------");
            }
        }

        private static void AddDevice()
        {
            Console.WriteLine("\n=== 新規端末登録 ===");
            
            Console.Write("箇所名: ");
            var locationName = Console.ReadLine();

            Console.Write("PC/ID: ");
            var pcId = Console.ReadLine();

            Console.Write("故障機交換 (y/n): ");
            var isReplacement = Console.ReadLine()?.ToLower() == "y";

            var device = _deviceService.AddDevice(locationName, pcId, isReplacement);
            Console.WriteLine($"端末が登録されました。ID: {device.Id}");
        }

        private static void EditDevice()
        {
            Console.WriteLine("\n=== 端末情報編集 ===");
            
            Console.Write("編集する端末のID: ");
            if (!int.TryParse(Console.ReadLine(), out int id))
            {
                Console.WriteLine("無効なIDです。");
                return;
            }

            var device = _deviceService.GetDevice(id);
            if (device == null)
            {
                Console.WriteLine("指定されたIDの端末が見つかりません。");
                return;
            }

            Console.Write($"箇所名 ({device.LocationName}): ");
            var locationName = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(locationName))
                locationName = device.LocationName;

            Console.Write($"PC/ID ({device.PcId}): ");
            var pcId = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(pcId))
                pcId = device.PcId;

            Console.WriteLine("ステータス:");
            Console.WriteLine("1. 準備中");
            Console.WriteLine("2. 出荷待ち");
            Console.WriteLine("3. 受取待ち");
            Console.WriteLine("4. 受取済み");
            Console.Write("選択 (1-4): ");
            var statusChoice = Console.ReadLine();
            var status = statusChoice switch
            {
                "1" => DeviceStatus.InPreparation,
                "2" => DeviceStatus.WaitingForShipment,
                "3" => DeviceStatus.WaitingForReceipt,
                "4" => DeviceStatus.Received,
                _ => device.Status
            };

            Console.Write("解除期限 (yyyy/MM/dd または空欄): ");
            var deadlineStr = Console.ReadLine();
            DateTime? deadline = null;
            if (!string.IsNullOrWhiteSpace(deadlineStr))
            {
                if (DateTime.TryParse(deadlineStr, out DateTime parsedDate))
                    deadline = parsedDate;
            }

            Console.Write($"故障機交換 (y/n) [{(device.IsReplacementDevice ? "y" : "n")}]: ");
            var replacementInput = Console.ReadLine()?.ToLower();
            var isReplacement = replacementInput == "y" || (replacementInput == "" && device.IsReplacementDevice);

            if (_deviceService.UpdateDevice(id, locationName, pcId, status, deadline, isReplacement))
                Console.WriteLine("端末情報が更新されました。");
            else
                Console.WriteLine("端末情報の更新に失敗しました。");
        }

        private static void DeleteDevice()
        {
            Console.WriteLine("\n=== 端末削除 ===");
            
            Console.Write("削除する端末のID: ");
            if (!int.TryParse(Console.ReadLine(), out int id))
            {
                Console.WriteLine("無効なIDです。");
                return;
            }

            if (_deviceService.DeleteDevice(id))
                Console.WriteLine("端末が削除されました。");
            else
                Console.WriteLine("指定されたIDの端末が見つかりません。");
        }

        private static void ExportToCsv()
        {
            Console.WriteLine("\n=== CSV出力 ===");
            
            Console.Write("出力ファイル名 (デフォルト: devices.csv): ");
            var fileName = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(fileName))
                fileName = "devices.csv";

            try
            {
                CsvExporter.ExportToCsv(_deviceService.GetAllDevices(), fileName);
                Console.WriteLine($"CSVファイルが出力されました: {fileName}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"CSVファイルの出力中にエラーが発生しました: {ex.Message}");
            }
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