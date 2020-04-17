import numpy as np
from skimage.measure import compare_ssim
import cv2
import sys
import time

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [video_file]")
    sys.exit(1)

frame_i = 2550

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_i)

empty_frames = 0
last_frame = None
last_time = time.time()
frame_i -= 1 # Make sure

mean_images = []
for i in range(100):
    good_frame, frame = cap.read()
    if not good_frame:
        empty_frames += 1
        continue
    mean_images.append(frame)

np.mean()
while(cap.isOpened()):
    frame_i += 1
    print("frame_i", frame_i)
    good_frame, frame = cap.read()
    if not good_frame:
        empty_frames += 1
        continue

    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if last_frame is None:
        last_frame = frame_grey


    (score, diff) = compare_ssim(frame_grey, last_frame, full=True)
    print(score)
    last_frame = frame_grey

    cv2.putText(frame, f"{frame_i} Score: {score:.2f}", (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0))

    cv2.imshow('frame', diff)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    new_time = time.time()
    print("frame period", new_time - last_time)
    last_time = new_time

print("empty_frames", empty_frames)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()