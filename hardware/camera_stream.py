# hardware/camera_stream.py
import cv2
import threading
import base64
import numpy as np

class CameraStream:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.width = width
        self.height = height
        self.frame = None #Khởi tạo để không bị lỗi
        self.stopped = True

    def start(self):
        self.stopped = False
        return self

    def update(self, frame_data):
         # Giải mã frame từ dữ liệu base64
        try:
            frame_bytes = base64.b64decode(frame_data)
            frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
            self.frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            if self.frame is None:
                print("Không thể giải mã frame")
        except Exception as e:
            print(f"Lỗi giải mã và xử lý frame: {e}")
            self.frame = None

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True