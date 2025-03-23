"""GPS Reader."""
import sys

#Kiểm tra xem có chạy trên Raspberry Pi không
if 'arm' not in sys.platform:
    print("[gps_reader.py] Không chạy trên Raspberry Pi, sử dụng thư viện ảo.")
    import mocks.mock_serial as serial
    #import mocks.mock_pynmea2 as pynmea2  #Không cần thiết ở đây
else:
    import serial
    #import pynmea2 #Không cần thiết ở đây
class GPSReader:
    def __init__(self, port, baudrate):
        """
        Khởi tạo GPS Reader.

        Args:
            port (str): Cổng serial kết nối với GPS module. Thay đổi nếu cần.
            baudrate (int): Tốc độ baudrate của GPS module.
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None  # Khởi tạo self.ser

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1) #Thêm timeout
            print(f"Kết nối GPS thành công tại cổng {self.port}") #In thông báo kết nối
        except serial.SerialException as e:
            print(f"Lỗi kết nối GPS tại cổng {self.port}: {e}")
            self.ser = None  # Đặt self.ser thành None nếu kết nối thất bại


    def get_location(self):
        if self.ser is None:
            print("Không có kết nối GPS.")
            return None, None

        try:
            while True:
                line = self.ser.readline().decode('utf-8', errors='ignore')
                if line.startswith('$GPGGA'):
                    import pynmea2
                    msg = pynmea2.parse(line)
                    latitude = msg.latitude
                    longitude = msg.longitude
                    return latitude, longitude
        except Exception as e:
            print(f"Lỗi đọc GPS: {e}")
            return None, None

    def close(self):
        if self.ser and self.ser.is_open: #Thêm kiểm tra xem serial đã mở chưa trước khi đóng
            self.ser.close()
            print("Đã đóng kết nối GPS")