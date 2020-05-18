import cv2 as cv
import dlib
import os
import xml.etree.ElementTree as pars

dir = r"/Users/asimonov/PycharmProjects/Skolkovo_Junior_challenge2020_final/detect"

ImgNameL = os.listdir(dir + r"/images/noDrive/")

images = []
annots = []

for FileName in ImgNameL:
    Img = cv.imread(dir + r"/images/noDrive/" + FileName)
    Img = cv.cvtColor(Img, cv.COLOR_BGR2RGB)

    FName = FileName.split(".")[0]
    e = pars.parse(dir+r"/annotations/noDrive_save/" + FName + ".xml")
    root = e.getroot()

    object = root.find("object")
    object = object.find("bndbox")
    x = int(object.find("xmin").text)
    y = int(object.find("ymin").text)
    x1 = int(object.find("xmax").text)
    y1 = int(object.find("ymax").text)

    images.append(Img)
    annots.append([dlib.rectangle(left=x, top=y, right=x1, bottom=y1)])

options = dlib.simple_object_detector_training_options()

detector = dlib.train_simple_object_detector(images, annots, options)

detector.save("noDrive.svm")
print("Succsesfule")