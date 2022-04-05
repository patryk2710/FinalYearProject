import cv2
import numpy as np
import argparse
import os
import time

net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

classes = open('coco.names').read().strip().split('\n') # LABELS

# read in whole directory
images = []
imageName = []

for file in os.listdir('assets/'):
    image = cv2.imread(os.path.join('assets/', file))
    if image is not None:
        images.append(image)
        imageName.append(file)

kernel = np.ones((5,5),np.float32)/25

timeTaken = []
results = []
totalTime = time.time()
for x in range(0,10):
    i = 0
    resultsCurr = []
    startTime = time.time()
    for image in images:
        found = False
        CClockwiseImage = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # adding filtering increases accuracy
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
                resultsCurr.append('Wrong')
            else:
                resultsCurr.append('Correct')
        else:
            if "fake" in imageName[i]:
                resultsCurr.append('Correct')
                resultsCurr.append('FCorrect')
            else:
                resultsCurr.append('Wrong')
        i += 1
    # clean and store
    endTime = time.time()
    timeTaken.append(endTime - startTime)
    results.append(resultsCurr)
totalTimeEnd = time.time()

# here analyse results
percentCorrect = []
Correct = []
FakeCorrect = []
for x in results:
    Correct.append(x.count('Correct'))
    percentCorrect.append(x.count('Correct')/len(images) * 100)
    FakeCorrect.append(x.count('FCorrect'))

averageCorrect = np.mean(Correct)
averageTime = np.mean(timeTaken)
averagePercCorrect = np.mean(percentCorrect)
averageFakeCorrect = np.mean(FakeCorrect)

print("You Only Look Once Detector Completed 10 runs on " + str(len(images)) + " images in: " +
      "{:.5f}".format(totalTimeEnd - totalTime) + "s")
print("Averages per run:")
print("     Run time: " + "{:.5f}".format(averageTime) + "s")
print("     Accuracy: " + "{:.0f}".format(averageCorrect) + "/92 (" + "{:.3f}".format(averagePercCorrect) + "%)")
print("     Non bottle corrrectly ignored: " + "{:.0f}".format(averageFakeCorrect) + "/10")
