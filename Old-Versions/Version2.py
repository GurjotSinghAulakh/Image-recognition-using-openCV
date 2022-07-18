# TODO: Final Versjon - men må gjøres endel endringer.
# TODO: Mangler kommentarer og en del tester

import cv2
import numpy as np

# Image
img = cv2.imread("images/ny.jpg")

# Threshold to detect object
thres = 0.45

classNames = []
classFile = './models/coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

np.random.seed(98750)
colors = np.random.uniform(0, 255, size=(len(classNames), 3))

configPath = './models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = './models/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

try:
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    print(classIds, bbox)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            predicition_text = f"{classNames[classId-1]}: {confidence:.2f}%"

            print(predicition_text)

            cv2.rectangle(img, box, colors[classId], thickness=2)
            cv2.putText(img, predicition_text, (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[classId], 2)

    cv2.imshow("Result", img)
    cv2.waitKey(0)

except Exception as e:
    print(str(e))
