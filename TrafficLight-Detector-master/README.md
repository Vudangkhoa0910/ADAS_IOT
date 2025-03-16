Dưới đây là file `README.md` chi tiết dựa trên code phát hiện đèn giao thông bằng OpenCV:

---

# **Traffic Light Detector (TLD)**

## **Giới thiệu**
Traffic Light Detector (TLD) là một ứng dụng đơn giản sử dụng OpenCV và Python để phát hiện và phân loại đèn giao thông (đỏ, xanh, vàng) trong hình ảnh hoặc video. Ứng dụng sử dụng kỹ thuật phân đoạn màu sắc (HSV) và phát hiện hình tròn (Hough Circle Transform) để xác định vị trí và màu sắc của đèn giao thông.

---

## **Cách thức hoạt động**
1. **Chuyển đổi không gian màu**: Hình ảnh được chuyển từ không gian màu BGR sang HSV để dễ dàng phân đoạn màu sắc.
2. **Phân đoạn màu sắc**: Sử dụng các ngưỡng màu (threshold) để tách biệt các màu đỏ, xanh lá cây và vàng.
3. **Phát hiện hình tròn**: Áp dụng Hough Circle Transform để phát hiện các hình tròn (đèn giao thông) trong từng vùng màu.
4. **Hiển thị kết quả**: Vẽ khung tròn và nhãn màu lên hình ảnh gốc để hiển thị kết quả phát hiện.

---

## **Cài đặt**
### **Yêu cầu hệ thống**
- Python 3.x
- Thư viện OpenCV (`opencv-python`)
- Thư viện NumPy (`numpy`)

### **Cài đặt thư viện**
Chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install opencv-python numpy
```

---

## **Hướng dẫn sử dụng**
1. **Chuẩn bị dữ liệu**:
   - Đặt video hoặc hình ảnh cần phát hiện vào thư mục `light`.
   - Ví dụ: `light/video.mp4`.

2. **Chạy chương trình**:
   - Mở terminal và chạy lệnh sau:
     ```bash
     python main.py
     ```
   - Nếu muốn sử dụng video khác, thay đổi đường dẫn trong file `main.py`:
     ```python
     video_path = "../light/video.mp4"  # Thay bằng đường dẫn video của bạn
     ```

3. **Kết quả**:
   - Kết quả sẽ được hiển thị trong cửa sổ có tên "Traffic Light Detection".
   - Nhấn phím `q` để thoát chương trình.

---

## **Cấu trúc thư mục**
```
TrafficLight-Detector/
├── light/                # Thư mục chứa video hoặc hình ảnh đầu vào
│   └── video.mp4
├── main.py               # Script chính để phát hiện đèn giao thông
├── README.md             # Hướng dẫn sử dụng
└── requirements.txt      # Danh sách các thư viện cần thiết
```

---

## **Giải thích code**
### **1. Phân đoạn màu sắc**
- Sử dụng không gian màu HSV để xác định các ngưỡng màu:
  ```python
  lower_red1 = np.array([0, 100, 100])
  upper_red1 = np.array([10, 255, 255])
  lower_red2 = np.array([160, 100, 100])
  upper_red2 = np.array([180, 255, 255])
  lower_green = np.array([40, 50, 50])
  upper_green = np.array([90, 255, 255])
  lower_yellow = np.array([15, 150, 150])
  upper_yellow = np.array([35, 255, 255])
  ```

### **2. Phát hiện hình tròn**
- Sử dụng Hough Circle Transform để phát hiện các hình tròn:
  ```python
  r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80, param1=50, param2=10, minRadius=0, maxRadius=30)
  g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60, param1=50, param2=10, minRadius=0, maxRadius=30)
  y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=5, minRadius=0, maxRadius=30)
  ```

### **3. Hiển thị kết quả**
- Vẽ khung tròn và nhãn màu lên hình ảnh gốc:
  ```python
  cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
  cv2.putText(cimg, color_name, (i[0], i[1]), font, 1, text_color, 2, cv2.LINE_AA)
  ```

---


## **Tùy chỉnh**
- Để cải thiện kết quả, bạn có thể điều chỉnh các tham số như:
  - Ngưỡng màu sắc (`lower_red1`, `upper_red1`, ...).
  - Tham số của Hough Circle Transform (`param1`, `param2`, `minRadius`, `maxRadius`).

---


## **Tài liệu tham khảo**
1. [OpenCV Documentation](https://docs.opencv.org/)
2. [Hough Circle Transform](https://docs.opencv.org/4.x/d4/d70/tutorial_hough_circle.html)
3. [Color Spaces in OpenCV](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)

---

Chúc bạn sử dụng hiệu quả! 🚦