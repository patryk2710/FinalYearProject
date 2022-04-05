import numpy as np
import cv2
import os
import time

net = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

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
        # rotating counter-clockwise increases accuracy
        CClockwiseImage = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # adding filtering increases accuracy
        # filtered = cv2.GaussianBlur(CClockwiseImage, (5, 5), 0) # gaussian
        # filtered = cv2.medianBlur(CClockwiseImage, 5)  # median
        # filtered = cv2.filter2D(src=CClockwiseImage, ddepth=-1, kernel=kernel) # averaging

        blob = cv2.dnn.blobFromImage(CClockwiseImage, size=(300, 300), swapRB=True, crop=False)
        net.setInput(blob)

        outputs = net.forward()

        # index 1 is class number, index 2 is confidence score
        for output in outputs[0, 0, :, :]:
            score = float(output[2])
            if score > 0.25:
                if output[1] == 44:
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

print("Single Shot Detector Completed 10 runs on " + str(len(images)) + " images in: " +
      "{:.5f}".format(totalTimeEnd - totalTime) + "s")
print("Averages per run:")
print("     Run time: " + "{:.5f}".format(averageTime) + "s")
print("     Accuracy: " + "{:.0f}".format(averageCorrect) + "/92 (" + "{:.3f}".format(averagePercCorrect) + "%)")
print("     Non bottle corrrectly ignored: " + "{:.0f}".format(averageFakeCorrect) + "/10")
