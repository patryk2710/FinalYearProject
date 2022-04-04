import cv2
import numpy as np
import argparse
import os
import time

net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

classes = open('coco.names').read().strip().split('\n') # LABELS

# read in whole directory
images = []
imageName = []
results = []

for file in os.listdir('assets/'):
    image = cv2.imread(os.path.join('assets/', file))
    if image is not None:
        images.append(image)
        imageName.append(file)

kernel = np.ones((5,5),np.float32)/25
i = 0
startTime = time.time()
for image in images:
    found = False
    CClockwiseImage = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # adding filtering increases accuracy, (gaussian blur goes up to 76, averaging goes up to 78, median to 74)
    # filtered = cv2.GaussianBlur(CClockwiseImage, (5, 5), 0) # gaussian
    # filtered = cv2.medianBlur(CClockwiseImage, 5) # median
    filtered = cv2.filter2D(src=CClockwiseImage, ddepth=-1, kernel=kernel) # averaging

    blob = cv2.dnn.blobFromImage(filtered, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    classIDs = []
    confidences = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > 0.70:
                if classID == 39:
                    found = True

    if found:
        if "fake" in imageName[i]:
            results.append('Wrong')
        else:
            results.append('Correct')
    else:
        if "fake" in imageName[i]:
            results.append('Correct')
            results.append('FCorrect')
        else:
            results.append('Wrong')
    i += 1
endTime = time.time()

# here analyse results
percentCorrect = (results.count('Correct')/len(images)) * 100
print("Correct: " + str(results.count('Correct')) + " out of " + str(len(images)) + " (" + "{:.3f}".format(percentCorrect) + "%)")
print("Non bottle object correctly ignored: " + str(results.count('FCorrect')))
print("You Only Look Once Detector took {:.6f} seconds to run ".format(endTime - startTime) + str(len(images)) + " images.")