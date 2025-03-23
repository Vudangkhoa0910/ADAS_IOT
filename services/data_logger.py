import csv
import datetime
import threading
import time

class DataLogger:
    def __init__(self, log_file="data.csv", interval=5):  # Ghi mỗi 5 giây
        self.log_file = log_file
        self.interval = interval
        self.running = False
        self.thread = None
        self.header = ["timestamp", "speed", "rpm", "coolant_temp", "fuel_level", "latitude", "longitude"]  # Header CSV

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.log_data)
        self.thread.daemon = True  # Kết thúc khi chương trình chính kết thúc
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()  # Chờ thread kết thúc

    def log_data(self):
        while self.running:
            # Lấy dữ liệu từ các hàm get trong app.py (cần truyền vào)
            data = self.get_data_from_app() #Cần phải sửa đổi hàm này

            if data:
                self.write_to_csv(data)
            time.sleep(self.interval)

    def write_to_csv(self, data):
        try:
            #Kiểm tra xem file có tồn tại hay không
            file_exists = True
            try:
                with open(self.log_file, 'r') as f:
                    pass
            except FileNotFoundError:
                file_exists = False
            with open(self.log_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Nếu file chưa tồn tại thì ghi header
                if not file_exists:
                    writer.writerow(self.header)
                writer.writerow(data)

        except Exception as e:
            print(f"Lỗi ghi log: {e}")

    def get_data_from_app(self):
        """
        Hàm này phải được sửa đổi để lấy dữ liệu từ các đối tượng
        OBDReader và GPSReader trong app.py.
        """
        # Ví dụ: Trả về dữ liệu giả định. CẦN THAY ĐỔI.
        timestamp = datetime.datetime.now().isoformat()
        speed = None  # Thay bằng obd_reader.get_speed()
        rpm = None    # Thay bằng obd_reader.get_rpm()
        coolant_temp = None # Thay bằng obd_reader.get_coolant_temp()
        fuel_level = None   # Thay bằng obd_reader.get_fuel_level()
        latitude = None  # Thay bằng gps_reader.get_latitude()
        longitude = None # Thay bằng gps_reader.get_longitude()

        return [timestamp, speed, rpm, coolant_temp, fuel_level, latitude, longitude]