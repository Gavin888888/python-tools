import cv2

cap = cv2.VideoCapture('1.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    # 调整窗口大小
    cv2.namedWindow("frame", 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口名一直
    cv2.resizeWindow("frame", 1920, 1080)  # 设置长和宽
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()