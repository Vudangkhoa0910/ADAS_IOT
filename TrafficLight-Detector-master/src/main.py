import cv2
import numpy as np

def detect(frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cimg = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Định nghĩa khoảng màu
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])
    lower_yellow = np.array([15, 150, 150])
    upper_yellow = np.array([35, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    maskr = cv2.add(mask1, mask2)

    size = frame.shape
    
    # Phát hiện hình tròn bằng HoughCircles
    r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80, param1=50, param2=10, minRadius=0, maxRadius=30)
    g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60, param1=50, param2=10, minRadius=0, maxRadius=30)
    y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=5, minRadius=0, maxRadius=30)

    # Xử lý từng màu đèn
    def process_circles(circles, mask, color_name, text_color):
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv2.putText(cimg, color_name, (i[0], i[1]), font, 1, text_color, 2, cv2.LINE_AA)
    
    process_circles(r_circles, maskr, "RED", (0, 0, 255))
    process_circles(g_circles, maskg, "GREEN", (0, 255, 0))
    process_circles(y_circles, masky, "YELLOW", (0, 255, 255))

    return cimg

if __name__ == '__main__':
    video_path = "../light/video.mp4"  # Thay bằng đường dẫn video của bạn
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result_frame = detect(frame)
        cv2.imshow("Traffic Light Detection", result_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
