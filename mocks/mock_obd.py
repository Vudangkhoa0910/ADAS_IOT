"""Mô phỏng thư viện obd."""
import sys
import random

if 'arm' not in sys.platform:
     print("Không chạy trên Raspberry Pi, import mock obd")
     class MockQuantity:
          """Giả lập hàm Quantity"""
          def __init__(self, command):
               self.command = command
               self.magnitude = self.get_mock_value() #Giá trị mặc định
          def to(self, unit):
               return self

          def get_mock_value(self):
               """Trả về giá trị ảo ngẫu nhiên."""
               # Thay đổi các giá trị này để mô phỏng dữ liệu OBD-II
               if self.command == "SPEED":
                    return MockData.speed # km/h
               elif self.command == "RPM":
                    return MockData.rpm # RPM
               elif self.command == "COOLANT_TEMP":
                    return MockData.coolant_temp # độ C
               elif self.command == "FUEL_LEVEL":
                    return MockData.fuel_level # %
               else:
                    return "P0000" # DTC

     class MockResponse:
         """Mô phỏng lớp Response."""
         def __init__(self, command):
             """Khởi tạo đối tượng Response."""
             self.value = MockQuantity(command) # Chú ý đã sửa
             self.is_null_value = False

         def is_null(self):
             """Giả lập hàm is_null"""
             return self.is_null_value

     class OBD:
         """Mô phỏng lớp OBD."""
         def __init__(self, port=None, baudrate=None):
             """Khởi tạo đối tượng OBD."""
             self.port = port
             self.baudrate = baudrate
             self.is_connected_value = True
             print(f"[MOCK obd] Kết nối với cổng {port} với baudrate {baudrate}")

         def query(self, command):
             """Trả về một đối tượng Response giả lập."""
             print(f"[MOCK obd] Thực hiện truy vấn: {command}")
             return MockResponse(command)

         def is_connected(self):
             """Kiểm tra xem đã kết nối chưa."""
             return self.is_connected_value

         def close(self):
             """Đóng kết nối."""
             self.is_connected_value = False
             print("[MOCK obd] Đóng kết nối")

     class commands:
         """Mô phỏng lớp commands."""
         SPEED = "SPEED"
         RPM = "RPM"
         COOLANT_TEMP = "COOLANT_TEMP"
         FUEL_LEVEL = "FUEL_LEVEL"
         GET_DTC = "GET_DTC"

     class MockData:
          """Lớp này dùng để tạo giá trị ngẫu nhiên, nó độc lập với OBD"""
          speed = 0
          rpm = 700
          coolant_temp = 70
          fuel_level = 50

          @staticmethod
          def update_data():
               MockData.speed = max(0, min(200, MockData.speed + random.randint(-5, 5)))
               MockData.rpm = max(700, min(4000, MockData.rpm + random.randint(-100, 100)))
               MockData.coolant_temp = max(60, min(110, MockData.coolant_temp + random.randint(-2, 2)))
               MockData.fuel_level = max(0, min(100, MockData.fuel_level + random.randint(-1, 1)))