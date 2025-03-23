import sys
import time
import random
import base64
import io
from PIL import Image

#Kiểm tra xem có chạy trên Raspberry Pi không
if 'arm' not in sys.platform:
    print("Không chạy trên Raspberry Pi, sử dụng thư viện ảo.")
    sys.path = ['mocks'] + sys.path  # Thêm 'mocks' vào đầu sys.path

    # Import các mock cần thiết
    from mocks import mock_obd as obd
    from mocks import mock_serial as serial
    import mocks.mock_rpi_gpio as GPIO

    # Loại bỏ 'mocks' khỏi sys.path để sử dụng cv2 thật
    if 'mocks' in sys.path:
        sys.path.remove('mocks')
else:
    import obd
    import serial
    import RPi.GPIO as GPIO

import cv2
import base64
import os
import datetime
import threading

from flask import Flask, render_template, jsonify, send_file, request
from flask_socketio import SocketIO
from hardware.camera_stream import CameraStream
from services.alert_service import AlertService
from services.data_logger import DataLogger
from hardware.led_indicator import LEDIndicator
from hardware.buzzer import Buzzer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #Khóa bảo mật
socketio = SocketIO(app, cors_allowed_origins='*')

#Check if YOLO is available
try:
    import torch
    print("PyTorch found. YOLO will be imported")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', force_reload=True)
    print("YOLO model loaded successfully!")
except ImportError:
    print("PyTorch not found, so YOLO can not be imported. Running in Safe Mode")
    model = None

#Tạo hàm tùy chỉnh để kiểm tra hasattr
def has_attribute(obj, attr):
    return hasattr(obj, attr)

#Đăng ký hàm tùy chỉnh
app.jinja_env.filters['has_attribute'] = has_attribute

RED_LED_PIN = 17      # GPIO17 (Pin 11)
YELLOW_LED_PIN = 27   # GPIO27 (Pin 13)
GREEN_LED_PIN = 22    # GPIO22 (Pin 15)
BUZZER_PIN = 4        # GPIO4  (Pin 07)

CAMERA_ID = 0         # ID của camera (thường là 0 cho camera mặc định)
CAMERA_WIDTH = 640      # Độ rộng của ảnh camera
CAMERA_HEIGHT = 480     # Độ cao của ảnh camera

GPS_PORT = "/dev/ttyS0"     # Cổng serial GPS (thay đổi nếu cần)
GPS_BAUDRATE = 9600     # Baudrate GPS

OBD_PORT = None       # Cổng Bluetooth OBD-II (None để tự động tìm) -  "/dev/rfcomm0" (ví dụ)
OBD_BAUDRATE = None       # Baudrate OBD-II (thường không cần thiết lập)

#led_indicator = LEDIndicator(RED_LED_PIN, YELLOW_LED_PIN, GREEN_LED_PIN)
#buzzer = Buzzer(BUZZER_PIN)
camera_stream = CameraStream(src=CAMERA_ID, width=CAMERA_WIDTH, height=CAMERA_HEIGHT).start()
import sys
if 'arm' not in sys.platform:
    print("Không chạy trên Raspberry Pi, import mock obd/serial")
    from mocks import mock_obd as obd
    from mocks import mock_serial as serial
    import mocks.mock_rpi_gpio as GPIO
    #from mocks import mock_pynmea2 as pynmea2 #Chưa cần thiết
else:
    import obd
    import serial
    import RPi.GPIO as GPIO
    #from hardware.gps_reader import GPSReader
    #from hardware.obd_reader import OBDReader
    #Khởi tạo sau để có thể dùng được mock GPIO
if 'arm' not in sys.platform:
    print("Không chạy trên Raspberry Pi, nên không dùng led/buzzer")
else:
    led_indicator = LEDIndicator(RED_LED_PIN, YELLOW_LED_PIN, GREEN_LED_PIN)
    buzzer = Buzzer(BUZZER_PIN)
class GPSReader:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        print(f"[GPSReader] Khởi tạo GPSReader tại {self.port} với baudrate {self.baudrate}")

    def get_location(self):
        try:
            line = self.ser.readline().decode('utf-8', errors='ignore')
            import sys
            if 'arm' not in sys.platform:
                 print("[GPSReader]Không chạy trên Raspberry Pi, cần dữ liệu ảo từ Pynmea2")
                 latitude = 21.022578
                 longitude = 105.516662
                 return latitude, longitude
            else:
                 import pynmea2
                 msg = pynmea2.parse(line)
                 latitude = msg.latitude
                 longitude = msg.longitude
                 print(f"[GPSReader] Vĩ độ: {latitude}, Kinh độ: {longitude}")
                 return latitude, longitude
        except Exception as e:
            print(f"[GPSReader] Lỗi đọc GPS: {e}")
            return None, None

    def close(self):
        self.ser.close()
        print("[GPSReader] Đã đóng kết nối GPS")

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
        #Kiểm tra response từ mock_obd hoặc obd thật
        if hasattr(response, 'is_null'):
             if not response.is_null():
                return response.value.to("kph").magnitude
             else:
                return None
        else:
             return 50

    def get_rpm(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.RPM
        response = self.connection.query(cmd)
        #Kiểm tra response từ mock_obd hoặc obd thật
        if hasattr(response, 'is_null'):
             if not response.is_null():
                return response.value.magnitude
             else:
                return None
        else:
             return 1000

    def get_coolant_temp(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.COOLANT_TEMP
        response = self.connection.query(cmd)
        #Kiểm tra response từ mock_obd hoặc obd thật
        if hasattr(response, 'is_null'):
             if not response.is_null():
                return response.value.to("celsius").magnitude
             else:
                return None
        else:
             return 80

    def get_fuel_level(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.FUEL_LEVEL
        response = self.connection.query(cmd)
        #Kiểm tra response từ mock_obd hoặc obd thật
        if hasattr(response, 'is_null'):
             if not response.is_null():
                return response.value.magnitude
             else:
                return None
        else:
             return 50

    def get_dtc(self):
        if not self.is_connected():
            return None
        cmd = obd.commands.GET_DTC
        response = self.connection.query(cmd)
        #Kiểm tra response từ mock_obd hoặc obd thật
        if hasattr(response, 'is_null'):
             if not response.is_null():
                return response.value
             else:
                return None
        else:
             return "P0000"

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

alert_service = AlertService()
data_logger = DataLogger()
camera_stream = CameraStream(src=CAMERA_ID, width=CAMERA_WIDTH, height=CAMERA_HEIGHT).start()
gps_reader = GPSReader(port=GPS_PORT, baudrate=GPS_BAUDRATE)
obd_reader = OBDReader(port=OBD_PORT, baudrate=OBD_BAUDRATE)

#Sửa đổi Alert Service để điều khiển LED và Buzzer
class AlertService:
    def check_alerts(self, obd_data):
        """
        Kiểm tra các điều kiện và tạo ra cảnh báo nếu cần.
        """
        if obd_data is None:
            #Nếu là thật mới chạy
            import sys
            if 'arm' not in sys.platform:
                print("Không chạy trên Raspberry Pi, bỏ qua led")
            else:
                led_indicator.green() # Không có dữ liệu -> hoạt động bình thường
            return None

        alerts = []

        if obd_data["speed"] is not None and obd_data["speed"] > 80:  # Ví dụ: Cảnh báo tốc độ
            alerts.append("Vượt quá tốc độ cho phép (80 km/h)")
            #Nếu là thật mới chạy
            import sys
            if 'arm' not in sys.platform:
                print("Không chạy trên Raspberry Pi, bỏ qua led")
            else:
                led_indicator.red() # Bật đèn đỏ
            import sys
            if 'arm' not in sys.platform:
                 print("Không chạy trên Raspberry Pi, bỏ qua buzzer")
            else:
                 buzzer.beep(0.2) # Bíp ngắn
        elif obd_data["coolant_temp"] is not None and obd_data["coolant_temp"] > 100:  # Ví dụ: Cảnh báo quá nhiệt
            alerts.append("Nhiệt độ động cơ quá cao")
            #Nếu là thật mới chạy
            import sys
            if 'arm' not in sys.platform:
                print("Không chạy trên Raspberry Pi, bỏ qua led")
            else:
                led_indicator.yellow() # Bật đèn vàng
            import sys
            if 'arm' not in sys.platform:
                 print("Không chạy trên Raspberry Pi, bỏ qua buzzer")
            else:
                 buzzer.beep(0.5) # Bíp dài hơn
        #Kiểm tra dtc
        if obd_data["dtc"] is not None:
            try:
                if hasattr(obd_data["dtc"], 'magnitude'): #Kiểm tra xem là mock quantity
                    dtc_value = obd_data["dtc"].magnitude #lấy giá trị
                else:
                     dtc_value = obd_data["dtc"]
                if len(dtc_value) > 0:  # Ví dụ: Cảnh báo có mã lỗi
                    alerts.append(f"Có mã lỗi: {dtc_value}")
                     #Nếu là thật mới chạy
                    import sys
                    if 'arm' not in sys.platform:
                        print("Không chạy trên Raspberry Pi, bỏ qua led")
                    else:
                        led_indicator.yellow()
                    import sys
                    if 'arm' not in sys.platform:
                         print("Không chạy trên Raspberry Pi, bỏ qua buzzer")
                    else:
                         buzzer.beep(0.3)
            except TypeError:
                #Xử lý nếu len() không thể được gọi
                print("Không thể lấy len() của dtc")
        else:
            #Nếu là thật mới chạy
            import sys
            if 'arm' not in sys.platform:
                print("Không chạy trên Raspberry Pi, bỏ qua led")
            else:
                led_indicator.green() # Không có cảnh báo -> hoạt động bình thường
            import sys
            if 'arm' not in sys.platform:
                 print("Không chạy trên Raspberry Pi, bỏ qua buzzer")
            else:
                buzzer.beep(0) # Tắt Buzzer
        return alerts if len(alerts) > 0 else None

def data_logger_get_data():
    """
    Hàm này được gọi từ DataLogger để lấy dữ liệu từ các đối tượng
    OBDReader và GPSReader trong app.py.
    """
    timestamp = datetime.datetime.now().isoformat()
    speed = obd_reader.get_speed() if obd_reader.is_connected() else None
    rpm = obd_reader.get_rpm() if obd_reader.is_connected() else None
    coolant_temp = obd_reader.get_coolant_temp() if obd_reader.is_connected() else None
    fuel_level = obd_reader.get_fuel_level() if obd_reader.is_connected() else None
    latitude, longitude = gps_reader.get_location()

    return [timestamp, speed, rpm, coolant_temp, fuel_level, latitude, longitude]

data_logger_get_data = data_logger_get_data

#Create a flag to indicate if the data logger has been started
data_logger_started = False

def initial_data_logger():
    with app.app_context():
        data_logger.start()
threading.Thread(target=initial_data_logger).start()

@app.route('/')
def index():
    # Lấy dữ liệu từ OBD-II
    obd_data = obd_reader.get_all_data() if obd_reader.is_connected() else None
    # Lấy vị trí từ GPS
    latitude, longitude = gps_reader.get_location()
    # Lấy frame từ camera
    frame = camera_stream.read()

    # Tạo cảnh báo (ví dụ: nếu tốc độ vượt quá 80 km/h)
    alert = alert_service.check_alerts(obd_data) if obd_data else None

    return render_template('index.html',
                           obd_data=obd_data,
                           latitude=latitude,
                           longitude=longitude,
                           frame=frame,
                           alert=alert)

@app.route('/data')
def data():
    #Update data ở đây để không cần restart
    if 'arm' not in sys.platform:
        try:
            from mocks import mock_obd as obd
            #Cứ mỗi giây update thông số 1 lần
            obd.MockData.update_data()
        except Exception as e:
            print(f"Lỗi update MockData {e}")
    # Lấy dữ liệu từ OBD-II
    obd_data = obd_reader.get_all_data()
    #Chắc chắn là nó là số
    if obd_data:
        for key, value in obd_data.items():
            if hasattr(value, 'magnitude'):
                obd_data[key] = value.magnitude
    if obd_data is None:
        obd_data[key] = 0
    # Lấy vị trí từ GPS
    latitude, longitude = gps_reader.get_location()

    # Tạo cảnh báo (ví dụ: nếu tốc độ vượt quá 80 km/h)
    alert = alert_service.check_alerts(obd_data) if obd_data else None

    data = {
        "obd": obd_data,
        "latitude": latitude,
        "longitude": longitude,
        "alert": alert
    }
    return jsonify(data)

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    frame_data = data['frame']  # Frame ở định dạng base64
    camera_stream.update(frame_data)
    frame = camera_stream.read() #Đọc frame
    try:
        if frame is not None:
            cv2.imwrite('static/frame.jpg', frame) # Lưu frame
            print("Frame lưu thành công")
        else:
            print("Không có frame để lưu")
    except Exception as e:
        print(f"Lỗi lưu frame: {e}")
    return jsonify({'message': 'Frame đã nhận và xử lý'})

@app.route('/camera_feed')
def camera_feed():
    frame = camera_stream.read()
    if frame is None:
        return jsonify({'error': 'Không có frame nào'})
    else:
        try:
            # Lưu frame trước khi detect
            cv2.imwrite('static/input_frame.jpg', frame)
            print("Input frame saved to static/input_frame.jpg")

            if model is not None:
                print("Model is available, performing detection...")
                with torch.no_grad():  # Chế độ không tính đạo hàm
                    # Resize frame
                    frame = cv2.resize(frame, (640, 480))  # Thay đổi kích thước nếu cần
                    print("Frame shape:", frame.shape)  # In ra kích thước ảnh
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi BGR sang RGB
                    results = model(frame)  # Loại bỏ tham số conf
                    print("Results:", results)
                    detections = results.pandas().xyxy[0]
                    print("Number of detections:", len(detections))
                    print("Detections:", detections)
                    frame = results.render()[0]  # Lấy frame đã vẽ bounding box
            else:
                print("Model is None, skipping detection.")

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            #Kiểm tra xem buffer có phải bytes hay không
            if isinstance(buffer, str):
                buffer = buffer.encode('utf-8')
            frame_bytes = base64.b64encode(buffer)
            frame_string = frame_bytes.decode('utf-8')
            return jsonify({'frame': frame_string})
        except Exception as e:
            print(f"Lỗi mã hóa ảnh: {e}")
            return jsonify({'error': str(e)})

@app.route('/download_log')
def download_log():
    log_file = data_logger.log_file
    #Kiểm tra file có tồn tại không
    if not os.path.exists(log_file):
        return "File log không tồn tại", 404
    try:
        return send_file(log_file, as_attachment=True, download_name="data_log.csv") # Đặt tên file khi tải xuống
    except Exception as e:
        return str(e), 500

@app.route('/view_log')
def view_log():
    log_file = data_logger.log_file
    #Kiểm tra file có tồn tại không
    if not os.path.exists(log_file):
        return "File log không tồn tại", 404

    try:
        with open(log_file, 'r') as f:
            log_content = f.read()
        return render_template('view_log.html', log_content=log_content)
    except Exception as e:
        return str(e), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Tắt ứng dụng")
    #led_indicator.cleanup()   # Dọn dẹp LED
    #buzzer.cleanup()         # Dọn dẹp Buzzer
    #gps_reader.close()
    #camera_stream.stop()
    #obd_reader.close()
    #data_logger.stop()

if __name__ == '__main__':
    #Start the data_logger on a separate thread to avoid blocking the main thread
    threading.Thread(target=initial_data_logger).start()
    app.run(host="0.0.0.0", port=5001, debug=True)