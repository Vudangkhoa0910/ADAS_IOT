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
            #Kiểm tra để biết nó có define hay không
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