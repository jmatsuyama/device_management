using Microsoft.EntityFrameworkCore;

namespace DeviceManagementSystem.Models
{
    public class DeviceDbContext : DbContext
    {
        public DeviceDbContext(DbContextOptions<DeviceDbContext> options)
            : base(options)
        {
        }

        public DbSet<Device> Devices { get; set; }
    }
}