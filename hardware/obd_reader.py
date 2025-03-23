"""OBD Reader."""
import sys
#Kiểm tra xem có chạy trên Raspberry Pi không
if 'arm' not in sys.platform:
    print("[obd_reader.py] Không chạy trên Raspberry Pi, sử dụng thư viện ảo.")
    import mocks.mock_obd as obd
else:
    import obd

class OBDReader:
    def __init__(self, port=None, baudrate=None):
        """
        Khởi tạo OBD Reader.

        Args:
            port (str): Cổng Bluetooth (ví dụ: /dev/rfcomm0). None để tự động tìm.
            baudrate (int): Tốc độ baudrate OBD (nếu cần).
        """
        self.port = port
        self.baudrate = baudrate
        self.connection = None #Khởi tạo connection là None

        try:
            if self.port:
                if self.baudrate:
                    self.connection = obd.OBD(self.port, baudrate=self.baudrate) #Chỉ định cả port và baudrate
                else:
                    self.connection = obd.OBD(self.port) #Chỉ định port
            else:
                self.connection = obd.OBD()  # Tự động tìm cổng
            if self.connection.is_connected():
                print(f"Kết nối OBD-II thành công tại cổng {self.port}")
            else:
                print(f"Không thể kết nối OBD-II tại cổng {self.port}")
                self.connection = None # Đặt connection thành None nếu kết nối thất bại
        except Exception as e:
            print(f"Lỗi kết nối OBD-II: {e}")
            self.connection = None  # Đặt connection thành None nếu có lỗi

    def is_connected(self):
        return self.connection is not None and self.connection.is_connected()

    def get_speed(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.SPEED
        response = self.connection.query(cmd)
        return response.value.to("kph").magnitude if not response.is_null() else None

    def get_rpm(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.RPM
        response = self.connection.query(cmd)
        return response.value.magnitude if not response.is_null() else None

    def get_coolant_temp(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.COOLANT_TEMP
        response = self.connection.query(cmd)
        return response.value.to("celsius").magnitude if not response.is_null() else None

    def get_fuel_level(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.FUEL_LEVEL
        response = self.connection.query(cmd)
        return response.value.magnitude if not response.is_null() else None

    def get_dtc(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.GET_DTC
        response = self.connection.query(cmd)
        return response.value if not response.is_null() else None

    def get_all_data(self):
        if not self.is_connected():
            return None
        data = {
            "speed": self.get_speed(),
            "rpm": self.get_rpm(),
            "coolant_temp": self.get_coolant_temp(),
            "fuel_level": self.get_fuel_level(),
            "dtc": self.get_dtc()
        }
        return data

    def close(self):
        if self.connection: #Thêm kiểm tra connection trước khi đóng
            self.connection.close()
            print("Đã đóng kết nối OBD-II")