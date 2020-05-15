import cv2
import os
import sys
import time
import json
import numpy as np
import argparse


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True,
                help = 'Path to input video')
ap.add_argument('-o', '--output', required=True,
                help = 'Path to output video')
ap.add_argument('-a', '--annotations', required=True,
                help = 'Path to annotation file')
ap.add_argument('-n', '--nframes', required=False,
                help = 'Number of frames to  extract')
ap.add_argument('-v', '--inverse', required=False,
                help = 'Extract negative frames')
args = ap.parse_args()


input_video_path = args.input
annontation_path = args.sannotations
output_video_path = args.output

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
