import cv2
import numpy as np
import time
from oblasty_yolo_4 import oblasty_yolo_4
import pandas as pd
def yolo_4(put):
    start_time = time.time()
    # Load Yolo
    net = cv2.dnn.readNet("yolov4-obj_last_old.weights", "yolov4-obj.cfg")
    with open ("passport.names","r") as f:
        classes =  [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    # Loading image
    img = cv2.imread(put)
    height, width, channels = img.shape

    # Detecting objects#
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    d = []
    z=[]
    for i in indexes:

        box = boxes[i]
        d.append(classes[class_ids[i]])
        d.append(box)
        d.append(confidences[i])

        flattenlist = lambda d:[item for element in d for item in flattenlist(element)] if type(d) is list else [d]

        z.append(flattenlist(d))
        d=[]
    print("--- %s seconds ---" % (time.time() - start_time))
    oblasty_yolo_4(put,img,z)

