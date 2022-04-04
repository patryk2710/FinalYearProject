import numpy as np
import tensorflow as tf
import cv2
import os
import time

net = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

# read in whole directory
images = []
imageName = []
results = []
for file in os.listdir('assets/'):
    image = cv2.imread(os.path.join('assets/', file))
    if image is not None:
        images.append(image)
        imageName.append(file)

# kernel = np.ones((5,5),np.float32)/25

i = 0
startTime = time.time()
for image in images:
    found = False
    CClockwiseImage = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # adding filtering increases accuracy, (gaussian blur goes up to 74, averaging goes up to 76, median to 77)
    # filtered = cv2.GaussianBlur(CClockwiseImage, (5, 5), 0) # gaussian
    filtered = cv2.medianBlur(CClockwiseImage, 5)  # median
    # filtered = cv2.filter2D(src=CClockwiseImage, ddepth=-1, kernel=kernel) # averaging

    blob = cv2.dnn.blobFromImage(filtered, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)

    outputs = net.forward()

    # index 1 is class number, index 2 is confidence score
    for output in outputs[0, 0, :, :]:
        score = float(output[2])
        if score > 0.3:
            if output[1] == 44:
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
print("Correct: " + str(results.count('Correct')) + " out of " + str(len(images)) +
      " (" + "{:.3f}".format(percentCorrect) + "%)")
print("Non bottle object correctly ignored: " + str(results.count('FCorrect')))
print("Single Shot Detector took {:.6f} seconds to run ".format(endTime - startTime) + str(len(images)) + " images.")
