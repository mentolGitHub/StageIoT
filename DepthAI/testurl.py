
 
import cv2
cap = cv2.VideoCapture('http://localhost:4748/video')
cap2 = cv2.VideoCapture('http://localhost:4747/video')
while True:
  ret, frame = cap.read()
  ret2, frame2 = cap2.read()
  cv2.imshow('Video', frame)
  cv2.imshow('Video2', frame2)
  if cv2.waitKey(1) == 27:
    exit(0)