"""Mô phỏng thư viện cv2 (OpenCV)."""
import sys
import numpy as np
if 'arm' not in sys.platform:
    print("Không chạy trên Raspberry Pi, import mock cv2")
    CAP_PROP_FRAME_WIDTH = 3  # Các hằng số cần thiết
    CAP_PROP_FRAME_HEIGHT = 4

    class VideoCapture:
        """Mô phỏng lớp VideoCapture."""
        def __init__(self, src):
            """Khởi tạo đối tượng VideoCapture."""
            self.src = src
            self.is_opened = True
            self.video_path = "static/videos/detect.mp4"  #Đường dẫn đến video
            self.cap = None #Gán cap
            self.frame = self._load_frame()
            print(f"[MOCK cv2] Mở camera với src {src}")

        def _load_frame(self):
            """Tải một frame từ video."""
            try:
                cap = cv2.VideoCapture(self.video_path)
                if not cap.isOpened():
                    print(f"Không thể mở video {self.video_path}")
                    return None
                ret, frame = cap.read()
                cap.release()  # Giải phóng sau khi đọc
                if not ret:
                    print("Không đọc được frame nào từ video")
                    return None
                return frame
            except Exception as e:
                print(f"Lỗi đọc video: {e}")
                return None

        def set(self, property_id, value):
            """Mô phỏng thiết lập thuộc tính."""
            print(f"[MOCK cv2] Thiết lập property {property_id} với giá trị {value}")

        def read(self):
            """Trả về một frame ảnh giả lập."""
            if self.frame is not None:
                return True, self.frame
            else:
                print("Không có frame nào")
                return False, None

        def release(self):
            """Giải phóng camera."""
            self.is_opened = False
            #if self.cap: #Không cần thiết
            #    self.cap.release()
            print("[MOCK cv2] Giải phóng camera")

        def isOpened(self):
            """Kiểm tra xem camera có mở không."""
            return self.is_opened

        def __del__(self):
            print("[MOCK cv2] Đối tượng VideoCapture đã bị hủy")

    def imencode(ext, img):
        """Giả lập hàm imencode"""
        print("[MOCK cv2] Mã hóa ảnh")
        #Chuyển đổi chuỗi thành bytes
        return True, "mock_encoded_image".encode('utf-8')

    def imshow(name, image):
        """Giả lập hàm imshow"""
        print(f"[MOCK cv2] Hiển thị ảnh: {name}")

    def waitKey(delay):
        """Giả lập hàm waitKey"""
        print(f"[MOCK cv2] Chờ {delay}ms")
        return ord('q')  # Giả lập nhấn q

    def destroyAllWindows():
        """Giả lập hàm destroyAllWindows"""
        print("[MOCK cv2] Đóng tất cả các cửa sổ")