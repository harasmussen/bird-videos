import numpy as np
import cv2
import sys

confidence_thr = 0.0001


CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")

mobile_net_dir = 'MobileNet-SSD/'
net = cv2.dnn.readNetFromCaffe(mobile_net_dir+  'deploy.prototxt' , mobile_net_dir + 'mobilenet_iter_73000.caffemodel')

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
# (note: normalization is done via the authors of the MobileNet SSD
# implementation)
blob=None
def applySSD(image):

    global blob
    #blob = cv2.dnn.blobFromImage(cv2.resize(image, (600, 300)), 0.007843, (600, 300), 127.5)
    blob = cv2.dnn.blobFromImage(image, 0.007843, image.shape[:2], 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
#     print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    print(len(detections))
    print(detections.shape)
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]
        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > confidence_thr:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            print(startX, startY, endX, endY)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    return image



if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [video_file]")
    sys.exit(1)


# create input blob
cv2.namedWindow("preview")
vc = cv2.VideoCapture(sys.argv[1])
vc.set(cv2.CAP_PROP_POS_FRAMES, 100)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
    (h, w) = frame.shape[0] , frame.shape[1]
else:
    rval = False

while vc.isOpened():
    rval, frame = vc.read()
    if rval is False:
        continue
    frame = applySSD(frame)
    cv2.imshow("preview", frame)
    key = cv2.waitKey(200) & 0xFF
    if key == ord('q'): # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")