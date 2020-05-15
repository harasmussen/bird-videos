import cv2
import sys
import time
import json
import os


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} [in_video_file] [out_video_file]")
    sys.exit(1)


input_video_file = sys.argv[1]
output_video_path = sys.argv[2]
output_video_file = f"{output_video_path}/{os.path.basename(input_video_file)}"
if not os.path.isfile(input_video_file):
    print(f"ERROR: {input_video_file} does not exists")
    sys.exit(1)

if os.path.isfile(output_video_file):
    print(f"ERROR: {output_video_file} does exists")
    sys.exit(1)

cap = cv2.VideoCapture(input_video_file)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

output_size= (864, 486)
out = cv2.VideoWriter(output_video_file, cv2.VideoWriter_fourcc('H','2','6','4'), frame_rate, output_size)

print(frame_count)
frame_i = 0
bad_frames = 0
while(frame_i < frame_count):
    if frame_i % 100 == 0:
        print(f"{frame_i/frame_count*100:f.2}%")
    good_frame, frame = cap.read()
    if not good_frame:
        frame = last_frame
        bad_frames += 1
    frame_scaled = cv2.resize(frame, output_size)
    out.write(frame_scaled)

    last_frame = frame

    frame_i += 1

print(frame_i, bad_frames)
cap.release()
out.release()