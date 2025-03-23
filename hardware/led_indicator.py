"""Quản lý LED Indicator."""
import sys

#Kiểm tra xem có chạy trên Raspberry Pi không
if 'arm' not in sys.platform:
    print("[led_indicator.py] Không chạy trên Raspberry Pi, sử dụng thư viện ảo.")
    import mocks.mock_rpi_gpio as GPIO
else:
    import RPi.GPIO as GPIO

class LEDIndicator:
    def __init__(self, red_pin, yellow_pin, green_pin):
        """
        Khởi tạo LED Indicator.

        Args:
            red_pin (int): Số GPIO pin cho đèn LED đỏ.
            yellow_pin (int): Số GPIO pin cho đèn LED vàng.
            green_pin (int): Số GPIO pin cho đèn LED xanh.
        """
        self.red_pin = red_pin
        self.yellow_pin = yellow_pin
        self.green_pin = green_pin

        # Thiết lập chế độ đánh số chân GPIO (BCM)
        GPIO.setmode(GPIO.BCM)

        # Thiết lập các chân làm đầu ra
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.yellow_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)

        # Tắt tất cả các đèn LED khi khởi tạo
        self.off()

    def red(self):
        """Bật đèn LED đỏ và tắt các đèn khác."""
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.yellow_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)

    def yellow(self):
        """Bật đèn LED vàng và tắt các đèn khác."""
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.yellow_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)

    def green(self):
        """Bật đèn LED xanh và tắt các đèn khác."""
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.yellow_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)

    def off(self):
        """Tắt tất cả các đèn LED."""
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.yellow_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)

    def cleanup(self):
        """Dọn dẹp GPIO khi kết thúc."""
        GPIO.cleanup()