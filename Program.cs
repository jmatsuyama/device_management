using Microsoft.EntityFrameworkCore;
using DeviceManagementSystem.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Add DbContext configuration
builder.Services.AddDbContext<DeviceDbContext>(options =>
    options.UseInMemoryDatabase("DeviceDb")); // 開発用にインメモリデータベースを使用

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Device}/{action=Index}/{id?}");

app.Run();