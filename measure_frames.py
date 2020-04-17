import numpy as np
from skimage.measure import compare_ssim
import cv2
import sys
import time

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [video_file]")
    sys.exit(1)

frame_i = 2650


input_video_path = sys.argv[1]
input_video_filename = input_video_path.split("/")[-1]
cap = cv2.VideoCapture(input_video_path)
# cap.set(cv2.CAP_PROP_POS_FRAMES, frame_i)

empty_frames = 0
last_frame = None
last_frame_gray = None
last_time = time.time()
frame_i -= 1 # Make sure

mean_images = []
for i in range(100):
    good_frame, frame = cap.read()
    if not good_frame:
        empty_frames += 1
        continue
    mean_images.append(frame)

measurements = []
frame_i = 0
while(cap.isOpened()):
    print("frame_i", frame_i)
    good_frame, frame = cap.read()
    if not good_frame:
        bad_frames += 1
        frame_i += 1
        continue

    print(good_frame.shape)
    print(good_frame[0].shape)
    break
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if last_frame is None:
        last_frame_gray = frame_grey
        last_frame = frame

    ssim_score, _diff = compare_ssim(frame_grey, last_frame_gray, full=True)
    diff = cv2.absdiff(img1, img2)
    red_diff = diff[:,:,0].sum().sum()
    green_diff = diff[:,:,1).sum().sum()
    blue_diff = diff[:,:,2].sum().sum()
    dist = math.sqrt(red_diff**2 + green_diff**2 + blue_diff**2)
    measurements.append({
        "ssim_score": ssim_score,
        "red_diff": red_diff,
        "green_diff": green_diff,
        "blue_diff": blue_diff,
        "dist": dist,
    })
    last_frame_gray = frame_grey
    last_frame = frame

    key = cv2.waitKey(sleep) & 0xFF
    if key  == ord('q'):
        break

    new_time = time.time()
    print("frame period", new_time - last_time)
    last_time = new_time
    frame_i += 1

with open(f"output/{input_video_filename}.json", "w"):
    json.dump(measurements, fp)
print("empty_frames", empty_frames)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()