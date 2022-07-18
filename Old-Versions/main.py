import numpy as np
from cv2 import cv2

image_path = 'images/person.jpg'
prototxt_path = 'models/MobileNetSSD_deploy.prototxt'
model_path = 'models/MobileNetSSD_deploy.caffemodel'
min_confidence = 0.2

classes = ["sofa", "chair", "bird", "persom", "bottle", "glass", "glasses", "table", "chain", "mobile", "car", "dog",
           "train", "motorbike", "bus", "chair", "test2", "test"]

np.random.seed(54321)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# cap = cv2.VideoCapture(0)

# while True:

   # _, image = cap.read()

net = cv2.dnn_DetectionModel(prototxt_path, model_path)

image = cv2.imread(image_path)
height, width = image.shape[0], image.shape[1]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

net.setInput(blob)
detected_objects = net.forward()

# TODO: Helt til hit så funker alt

for i in range(detected_objects.shape[0]):

    confidence = detected_objects[0][0][i][2]
    print(f"confidence er : {confidence}")

    if confidence > min_confidence:

        class_index = int(detected_objects[0][0][i][1])

        print(f"index er :  {class_index}")

        upper_left_x = int(detected_objects[0, 0, i, 3] * width)
        upper_left_y = int(detected_objects[0, 0, i, 4] * height)
        lower_right_x = int(detected_objects[0, 0, i, 5] * width)
        lower_right_y = int(detected_objects[0, 0, i, 6] * height)

        predicition_text = f"{classes[class_index]}: {confidence:.2f}%"

       # print(predicition_text)

        cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 2)
        cv2.putText(image, predicition_text, (upper_left_x, upper_left_y - 15 if upper_left_y > 30
        else upper_left_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)

cv2.imshow("Detected Objects", image)
cv2.waitKey(2)
cv2.destroyAllWindows()
# cap.release()
