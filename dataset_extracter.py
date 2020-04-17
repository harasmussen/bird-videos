import numpy as np
import cv2
import sys
import time

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [video_file]")
    sys.exit(1)


frame_i = 2630

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_i)
sleep = 3000
empty_frames = 0
last_time = time.time()
buffer = []
while(cap.isOpened()):
    print("frame_i", frame_i)
    good_frame, frame = cap.read()
    if not good_frame:
        empty_frames += 1
        frame_i += 1
        continue

    ahead_frame = cv2.resize(frame, (854, 480))
    buffer.append(ahead_frame)
    if len(buffer) < 10:
        continue
    current_frame = buffer.pop(0)

    show_frame = np.concatenate((current_frame, ahead_frame), axis=1)
    cv2.imshow('frame', show_frame)
    key = cv2.waitKey(sleep) & 0xFF
    if key  == ord('q'):
        break
    if key  == ord('f'):
        sleep = 1
    if key  == ord('s'):
        sleep = 3000
    if key == ord('y'):
        print("yes")
        cv2.imwrite(f"positive/{frame_i:05}.png", current_frame)
    if key == ord('n'):
        cv2.imwrite(f"negative/{frame_i:05}.png", current_frame)
        print("no")
    frame_i += 1
    new_time = time.time()
    print(new_time - last_time)
    last_time = new_time
print("empty_frames", empty_frames)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()