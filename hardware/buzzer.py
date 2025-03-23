"""Quản lý Buzzer."""
import sys

#Kiểm tra xem có chạy trên Raspberry Pi không
if 'arm' not in sys.platform:
    print("[buzzer.py] Không chạy trên Raspberry Pi, sử dụng thư viện ảo.")
    import mocks.mock_rpi_gpio as GPIO
else:
    import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin):
        """
        Khởi tạo Buzzer.

        Args:
            pin (int): Số GPIO pin kết nối với buzzer.
        """
        self.pin = pin

        # Thiết lập chế độ đánh số chân GPIO (BCM)
        GPIO.setmode(GPIO.BCM)

        # Thiết lập chân làm đầu ra
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)  # Tắt buzzer khi khởi tạo

    def beep(self, duration):
        """
        Phát tiếng bíp trong khoảng thời gian nhất định.

        Args:
            duration (float): Thời gian phát tiếng bíp (giây).
        """
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        """Dọn dẹp GPIO khi kết thúc."""
        GPIO.cleanup()