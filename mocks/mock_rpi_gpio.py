"""Mô phỏng thư viện RPi.GPIO."""

#Các chế độ chân
BCM = "BCM"
BOARD = "BOARD"

#Các trạng thái chân
OUT = "OUT"
IN = "IN"
HIGH = True
LOW = False

#Các thiết lập
_mode = None
_setup = {}
_output = {}

def setmode(mode):
    """Thiết lập chế độ chân."""
    global _mode
    _mode = mode
    print(f"[MOCK RPi.GPIO] Thiết lập chế độ chân: {mode}")

def setup(pin, direction):
    """Thiết lập chân."""
    global _setup
    _setup[pin] = direction
    print(f"[MOCK RPi.GPIO] Thiết lập chân {pin} là {direction}")

def output(pin, value):
    """Thiết lập giá trị chân."""
    global _output
    _output[pin] = value
    print(f"[MOCK RPi.GPIO] Thiết lập giá trị chân {pin} là {value}")

def cleanup():
    """Dọn dẹp GPIO."""
    global _setup, _output
    _setup = {}
    _output = {}
    print("[MOCK RPi.GPIO] Dọn dẹp GPIO")

#Các hàm khác
def input(channel):
     print("[MOCK RPi.GPIO] Chân input() được gọi, trả về LOW")
     return False

def setwarnings(flag):
    print(f"[MOCK RPi.GPIO] setwarnings({flag})")

def getmode():
    print(f"[MOCK RPi.GPIO] Chế độ hiện tại: {_mode}")
    return _mode