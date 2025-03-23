"""Mô phỏng thư viện serial."""
import sys

if 'arm' not in sys.platform:
     print("Không chạy trên Raspberry Pi, import mock serial")
     class Serial:
         """Mô phỏng lớp Serial."""
         def __init__(self, port, baudrate, timeout=None):
             """Khởi tạo đối tượng Serial."""
             self.port = port
             self.baudrate = baudrate
             self.timeout = timeout
             self.is_open = True
             print(f"[MOCK serial] Kết nối với cổng {port} với baudrate {baudrate}")

         def readline(self):
             """Trả về một dòng dữ liệu giả lập."""
             # Thay đổi dữ liệu này để mô phỏng dữ liệu GPS
             #Giả lập vị trí gần Hà Nội
             data = "$GPGGA,123519,2102.2578,N,10551.6662,E,1,08,0.9,545.4,M,46.9,M,,*47\n"
             return data.encode('utf-8')

         def close(self):
             """Đóng kết nối serial."""
             self.is_open = False
             print(f"[MOCK serial] Đóng kết nối với cổng {self.port}")

         def is_open(self):
             """Kiểm tra xem cổng serial có mở không."""
             return self.is_open
else:
    import serial
    import pynmea2 # Ímport ở đây nếu không chạy trên Raspberry Pi