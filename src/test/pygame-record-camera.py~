#!/usr/bin/env python
import numpy
import cv2

# Encoder
cap = cv2.VideoCapture(0)
fourcc = cv2.cv.CV_FOURCC('D','I','V','X')
movie = cv2.VideoWriter('camera.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        movie.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(10) == 27:
            break
    else:
        break

cap.release()
movie.release()
cv2.destroyAllWindows()
