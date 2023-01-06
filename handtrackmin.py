import cv2
import mediapipe as mp
import time

ccamera=0
cap = cv2.VideoCapture(ccamera, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1050)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while cap.isOpened():
    success, image = cap.read()
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id , lm in enumerate(handLms.landmark):
                print(id, lm)
                h,w,c = image.shape
                cx ,cy = int(lm.x*w ) , int(lm.y*h)
                print(id, cx, cy)
                if id == 4 :
                    cv2.circle(image,(cx,cy),25,(255,0,255),cv2.FILLED)
            mpDraw.draw_landmarks(image, handLms , mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(image,str(int(fps)), (10,70) , cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    cv2.imshow('Image', image)
    if cv2.waitKey(5) & 0xFF == ord("q"):
      break
cap.release()


