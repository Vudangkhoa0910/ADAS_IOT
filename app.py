from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Biến lưu trữ mức xăng, bắt đầu ở mức 100%
fuel = 100.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    global fuel

    # Giảm mức xăng từ từ
    fuel -= 0.001  # Giảm xăng mỗi lần gọi API

    # Đảm bảo xăng không giảm quá 0
    if fuel < 0:
        fuel = 0.0

    # Giới hạn khu vực Hà Đông, Hà Nội (latitude: 20.9600 - 21.0300, longitude: 105.7700 - 105.8600)
    lat = random.uniform(20.9840, 20.9890)  # Chọn lat trong khu vực Hà Đông
    lon = random.uniform(105.8060, 105.8130)  # Chọn lon trong khu vực Hà Đông

    # Giả lập tốc độ
    speed = random.randint(0, 120)

    # Giả lập thông tin GPS
    gps_location = {"lat": lat, "lon": lon}

    # Trả về các thông số dưới dạng JSON
    return jsonify(speed=speed, fuel=fuel, gps=gps_location)

if __name__ == "__main__":
    # Chạy Flask trên Vercel, cổng 8080 và host '0.0.0.0'
    app.run(debug=False, host='0.0.0.0', port=8080)
