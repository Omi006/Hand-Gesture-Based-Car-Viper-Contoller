from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject
import cv2
import numpy as np
from time import sleep

# Parameters
width, height = 1280, 720
gestureThreshold = 300

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
arduino = SerialObject()
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)
delay = 30
buttonPressed = False
counter = 0


while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)


    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:  # If hand is detected

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                #print("Left")
                buttonPressed = True
                arduino.sendData([1])

            if fingers == [0, 0, 0, 0, 1]:
                #print("Right")
                buttonPressed = True
                arduino.sendData([0])

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False


    cv2.imshow("Image", img)



    key = cv2.waitKey(1)
    if key == ord('q'):
        break