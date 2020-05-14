import cv2 as cv

cap = cv.VideoCapture("IMG_1800.mov")

while (True):
    ret, frame = cap.read()
    cv.imshow("Frame", frame)
    Framec = frame.copy()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv, (5, 5))
    mask = cv.inRange(hsv, (89, 124, 73), (255, 255, 255))
    cv.imshow("Mask", mask)

    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=4)
    cv.imshow("Mask2", mask)

    cont = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[0]
    if cont:
        cont = sorted(cont, key=cv.contourArea, reverse=True)
        cv.drawContours(frame, cont, 0, (255, 0, 255), 3)

        (x, y, w, h) = cv.boundingRect(cont[0])
        cv.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        cv.imshow("Cont", frame)

        roImg = Framec[y:y + h,x:x + w]
        roImg = cv.resize(roImg, (64, 64))
        roImg = cv.inRange(roImg, (89, 91, 149), (255, 255, 255))
        cv.imshow("Cut", roImg)
    else:
        cv.imshow("Cont", frame)
        cv.imshow("Cut", frame)


    if cv.waitKey(1) == ord("q"):
        break