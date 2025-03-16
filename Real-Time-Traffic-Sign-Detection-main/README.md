# Phát Hiện Biển Báo Giao Thông Thời Gian Thực

## Tóm tắt

Dự án này tập trung vào việc phát hiện và phân loại biển báo giao thông trong thời gian thực. Vùng quan tâm (ROI) được bao quanh bởi một khung chữ nhật và nhãn tương ứng được hiển thị trên đó. Thuật toán Yolov5-small được sử dụng để phát hiện vật thể. Mô hình được huấn luyện trong 800 epochs trên 3000 hình ảnh được gán nhãn thủ công cho 61 lớp khác nhau. Đạt được độ chính xác trung bình (mAP@0.5) là 91.75% và tốc độ thời gian thực là 45 fps trên card đồ họa GeForce MX 250.

## Hướng dẫn chạy mã

1. Giải nén toàn bộ kho lưu trữ và đặt nó làm thư mục hiện tại của bạn.
2. Tìm tệp *Models.zip* trong thư mục hiện tại và giải nén nó.
3. Cài đặt tất cả các phụ thuộc cần thiết bằng cách sử dụng tệp `requirements.txt`.
    * Nếu bạn đang sử dụng máy tính Windows:
    * **Gõ lệnh** - `pip install -r requirements.txt`
    * Hoặc nếu bạn đang sử dụng Anaconda Prompt:
    * **Gõ lệnh** - `conda install --file requirements.txt`
4. Điều hướng đến thư mục có tên *Codes* bằng cách sử dụng lệnh `cd Codes`.
5. Trước khi chạy lệnh tiếp theo, hãy đặt tệp hình ảnh/video mà bạn muốn phát hiện biển báo giao thông vào thư mục có tên *Test*.
    * **Gõ lệnh** - `python detect.py --source ../Test/{tên tệp của bạn}`
    * Ví dụ, nếu tên hình ảnh là `test.jpg`, hãy gõ `python detect.py --source ../Test/test.jpg`.
6. Để chạy trên luồng camera trực tiếp:
    * **Gõ lệnh** - `python detect.py --source 0`
7. Kết quả sẽ được lưu trong thư mục *Results*.

## Cấu trúc thư mục

**Real-Time-Traffic-Sign-Detection-main**\
├───Codes\
│ ├───models\
│ │ ├───hub\
│ │ └───__pycache__\
│ └───utils\
│ ├───google_app_engine\
│ └───__pycache__\
├───Model\
│ └───weights\
├───Results\
├───Sample Dataset\
└───Test


## Tài liệu tham khảo

1. Liên kết Github đến kho lưu trữ Ultralytics - https://github.com/ultralytics/yolov5
2. Liên kết Kaggle cho một số hình ảnh của tập dữ liệu - https://www.kaggle.com/andrewmvd/road-sign-detection
3. Bài báo gốc của YOLO được phát hành vào tháng 5 năm 2016 - https://arxiv.org/pdf/1506.02640.pdf
4. Liên kết Github đến kho lưu trữ LabelImg - https://github.com/tzutalin/labelImg