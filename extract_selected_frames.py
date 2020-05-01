import cv2
import os
import sys
import time
import json
import numpy as np


if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} [InVideoFile] [Annontations] [OutVideoFile] ")
    sys.exit(1)


input_video_path = sys.argv[1]
annontation_path = sys.argv[2]
output_video_path = sys.argv[3]

if not os.path.isfile(input_video_path):
    print(f"ERROR: {input_video_path} does not exists")
    sys.exit(1)

if os.path.isfile(output_video_path):
    print(f"ERROR: {output_video_path} does exists")
    sys.exit(1)

with open(annontation_path) as fp:
    annotations = json.load(fp)


cap = cv2.VideoCapture(input_video_path)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


if len(annotations) != frame_count:
    print(f"len(annotations) {len(annotations)} != frame_count {frame_count}")
    sys.exit(1)

out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc('H','2','6','4'), frame_rate, (frame_width, frame_height))


print(frame_count)
frame_i = 0
bad_frames = 0
last_frame = np.array([1])
try:
    while(frame_i < frame_count):
        if frame_i % 100 == 0:
            print(f"{frame_i/frame_count*100}")
        good_frame, frame = cap.read()
        if not good_frame:
            frame = last_frame
            bad_frames += 1
        if annotations[frame_i] == 1:
            out.write(frame)
        last_frame = frame

        frame_i += 1
except KeyboardInterrupt:
    pass
print(frame_i, bad_frames)
cap.release()
out.release()
