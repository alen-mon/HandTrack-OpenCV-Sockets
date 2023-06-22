from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

cap = cv2.VideoCapture("http://192.168.0.101:8081/video")
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5051)

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    data = []

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            data = []
            for lm in lmList:
                data.extend([lm[0], h - lm[1], lm[2]])
            data.append(hand["type"])  # Append hand type to the data list
            sock.sendto(str.encode(str(data)), serverAddressPort)

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)