#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################


import cv2
import argparse
import numpy as np
import os
import json
import time

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True,
                help = 'path to input image')
ap.add_argument('-c', '--config', required=True,
                help = 'path to yolo config file')
ap.add_argument('-w', '--weights', required=True,
                help = 'path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True,
                help = 'path to text file containing class names')
args = ap.parse_args()



def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_prediction(img, class_label, confidence, x, y, x_plus_w, y_plus_h):
    color = COLORS[class_label]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, class_label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


classes = None

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

np.random.seed(7654)
colors_list = np.random.uniform(0, 255, size=(len(classes), 3))
COLORS = dict(zip(classes, colors_list))

net = cv2.dnn.readNet(args.weights, args.config)


def classify(net, image):
    scale = 0.00392

    Width = image.shape[1]
    Height = image.shape[0]
    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.2
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    selected_indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    return [(classes[class_ids[i[0]]], boxes[i[0]], confidences[i[0]]) for i in selected_indices]

def draw_detections(image, detections):
    for class_label, box, confidence in detections:
        x,y,w,h = box
        draw_prediction(image, class_label, confidence, round(x), round(y), round(x+w), round(y+h))

def filter_detections(detections):
    black_listed = ["bench"]
    return [d for d in  detections if d[1] not in black_listed]

cap = cv2.VideoCapture(args.video)
# image = cv2.imread(args.video)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
output_size = (864, 486)

input_video_filebase = os.path.basename(args.video).split(".")[0]

# images = []
# n_frames = 10
# frame_step = int(frame_count / n_frames)
# print(f"Loading {n_frames} frames")
# for i in range(0, frame_count, frame_step):
#     cap.set(cv2.CAP_PROP_POS_FRAMES, i)
#     good_frame, image = cap.read()
#     if not good_frame:
#         continue
#     image_scaled = cv2.resize(image, output_size)
#     images.append(image_scaled)

annotations = [[] for _ in range(frame_count)]
print("Start classifing")
try:
    for i in range(frame_count):
        start = time.time()
        good_frame, image = cap.read()
        if not good_frame:
            continue

        # image = cv2.resize(image, output_size)
        detections = classify(net, image)
        annotations[i] = detections
        #detections = filter_detections(detections)
        # draw_detections(image, detections)
        for d in detections:
            print(i, d[:2])
        # cv2.imshow("object detection", image)
        # cv2.waitKey(2)
        print("time_spent", time.time()-start)
finally:
    output_filename = f"{input_video_filebase}_net_annotations.json"
    print(f"Saving to {output_filename}")
    with open(output_filename, "w") as fp:
        json.dump(annotations, fp)



#cv2.imwrite("object-detection.jpg", image)
cv2.destroyAllWindows()