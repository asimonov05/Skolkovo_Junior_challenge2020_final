import cv2 as cv


def form_blue(frame):
    frame = cv.resize(frame, (64, 64))
    frame = cv.inRange(frame, (89, 123, 73), (255, 255, 255))
    return frame


def formate(frame):
    cv.imshow("Frame", frame)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame = cv.blur(frame, (5, 5))
    frame = cv.inRange(frame, (89, 123, 73), (255, 255, 255))
    frame = cv.erode(frame, None, iterations=2)
    frame = cv.dilate(frame, None, iterations=4)
    return frame


def detect(frame):
    cv.imshow("Frame", frame)
    noDrive = cv.imread("park.png")
    ped = cv.imread("stop.jpg")
    noDrive = form_blue(noDrive)
    ped = form_blue(ped)
    framec = frame.copy()
    mask = formate(frame)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if contours:
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        cv.drawContours(frame, contours, 0, (255, 0, 255), 3, cv.LINE_AA, hierarchy, 1)

        (x, y, w, h) = cv.boundingRect(contours[0])
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)

        roImg = framec[y:y + h, x:x + w]
        roImg = cv.resize(roImg, (64, 64))
        roImg = cv.inRange(roImg, (89, 123, 73), (255, 255, 255))

        nd = 0
        pd = 0

        for i in range(64):
            for j in range(64):
                if roImg[i][j] == noDrive[i][j]:
                    nd += 1
                if roImg[i][j] == ped[i][j]:
                    pd += 1

        if nd > 3000:
            return "Parking"
        elif pd > 3000:
            return "Stop"
    return 0

def only_sravn(roImg, b):
    if not b:
        return "Nothing"
    park = cv.imread("park.png")
    park = form_blue(park)
    roImg = cv.resize(roImg, (64, 64))
    roImg = cv.inRange(roImg, (89, 123, 73), (255, 255, 255))
    park_k = 0
    for i in range(64):
        for j in range(64):
            if roImg[i][j] == None:
                continue
            if roImg[i][j] == park[i][j]:
                park_k += 1

    if park_k > 1600:
        return "Parking "
    return "Nothing "


def main():
    cap = cv.VideoCapture("IMG_1800.mov")
    ret, frame = cap.read()
    while(ret):
        print(detect(frame))
        ret, frame = cap.read()
        if ret:
            framec = frame.copy()
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()