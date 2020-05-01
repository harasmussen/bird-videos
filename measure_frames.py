import numpy as np
from skimage.metrics import structural_similarity
import cv2
import sys
import time
import json
import math

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [video_file]")
    sys.exit(1)

frame_i = 2650


input_video_path = sys.argv[1]
input_video_filename = input_video_path.split("/")[-1]
input_video_filename = input_video_filename.split(".")[0]
cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# cap.set(cv2.CAP_PROP_POS_FRAMES, frame_i)
print(input_video_filename, fps, frame_count)
bad_frames = 0
last_frame = None
last_frame_gray = None
last_time = time.time()
frame_i -= 1 # Make sure

measurements = []
frame_i = 0
try:
    while(frame_i < frame_count):
        print()
        # if frame_i > 10:
        #     break
        good_frame, frame = cap.read()
        if not good_frame:
            frame = last_frame
            bad_frames += 1
        frame_height, frame_width = frame.shape[:2]
        pixels = frame_height * frame_width

        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if last_frame is None:
            last_frame_gray = frame_grey
            last_frame = frame

        ssim_score, _diff = structural_similarity(last_frame_gray, frame_grey, full=True)
        diff = cv2.absdiff(last_frame, frame)
        red_diff = int(diff[:,:,0].sum().sum())
        green_diff = int(diff[:,:,1].sum().sum())
        blue_diff = int(diff[:,:,2].sum().sum())
        mean_diff = (red_diff + green_diff + blue_diff)/3
        measurements.append({
            "index": frame_i,
            "ssim_score": ssim_score,
            "red_diff": red_diff/pixels,
            "green_diff": green_diff/pixels,
            "blue_diff": blue_diff/pixels,
            "mean_diff": mean_diff/pixels,
        })
        print(f"{frame_i/frame_count*100:.2f}%: ssim_score {ssim_score:.2f} mean_diff {mean_diff/pixels:.2f}")
        last_frame_gray = frame_grey
        last_frame = frame

        new_time = time.time()
        print("frame period", new_time - last_time)
        last_time = new_time
        frame_i += 1
except KeyboardInterrupt:
    pass
with open(f"output/{input_video_filename}_measurements.json", "w") as fp:
    json.dump(measurements, fp)
print("empty_frames", bad_frames)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()