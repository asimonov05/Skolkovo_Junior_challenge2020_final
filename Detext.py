import cv2 as cv
import dlib

model_detector_park = dlib.simple_object_detector("tdl1.svm")
model_detector_noDrive = dlib.simple_object_detector("noDrive.svm")

cam = cv.VideoCapture(0)

while (1):
    stat, frame = cam.read()
    rect = frame.copy()
    boxes = model_detector_park(frame)
    xb = 0
    x = 0
    b = 0
    for box in boxes:
        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        cv.rectangle(frame, (x, y), (xb, yb), (255, 75, 0), 2)
        rect = frame[y:yb, x:xb]
        if xb - x > 0 or yb - y > 0:
            print("Parking")
            b = 1
            cv.imshow("Parking", rect)

    boxes = model_detector_noDrive(frame)
    for box in boxes:
        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        cv.rectangle(frame, (x, y), (xb, yb), (0, 0, 255), 2)
        rect = frame[y:yb, x:xb]
        if xb - x > 0 or yb - y > 0 and y != 0:
            print("noDrive")
            b += 1
            cv.imshow("No Drive", rect)
    if not b:
        print("Nothing")
    cv.imshow("Frame", frame)


    if cv.waitKey(1) == ord("q"):
        break