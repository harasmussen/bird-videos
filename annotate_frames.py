import cv2
import sys
import time
import json
import numpy as np

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} [VideoFile] [Annontations]")
    sys.exit(1)


input_video_path = sys.argv[1]
annontation_path = sys.argv[2]

try:
    with open(annontation_path) as fp:
        annontations = json.load(fp)
except IOError:
    annontations = []


def load_frames(input_video_path, start_frame):
# frame_i = 2630

    cap = cv2.VideoCapture(input_video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(fps, frame_count)
    all_frames = [None for _ in range(frame_count)]
    stop_loading = min(start_frame + 100, frame_count)
    frame_i = start_frame
    bad_frames = 0
    last_frame = np.array([1])
    while(frame_i < stop_loading):

        good_frame, frame = cap.read()
        if not good_frame:
            frame = last_frame
            bad_frames += 1

        all_frames[frame_i] = frame
        last_frame = frame
        frame_i += 1

    return all_frames

all_frames = load_frames(input_video_path, start_frame=0)
if len(annontations) == 0:
    annontations = [0 for _ in all_frames]

if len(annontations) != len(all_frames):
    print("Loaded annotation and frames are not the same length. Did you load a wrong file?")
    sys.exit(1)

frame_i = 0
cut_start = None
try:
    while True:
        if all_frames[frame_i] is None:
            start_frame = frame_i - 10 if reversing else frame_i
            all_frames = load_frames(input_video_path, start_frame=start_frame)
        reversing = False


        current_frame = all_frames[frame_i].copy()
        cv2.putText(current_frame, f"{frame_i} {annontations[frame_i]} ", (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255),3)
        cv2.putText(current_frame, f"{cut_start}", (0,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)
        cv2.imshow('frame', current_frame)
        pressed_key = cv2.waitKey(10) & 0xFF

        if pressed_key == ord('q'):
            break

        if pressed_key == ord('a'):
            if frame_i > 0:
                frame_i -= 1
                reversing = True

        if pressed_key == ord('d'):
            if frame_i < len(all_frames)-1:
                frame_i += 1

        if pressed_key == ord('j'):
            cut_start = frame_i

        if pressed_key == ord('l'):
            if cut_start is not None:
                for i in range(cut_start, frame_i+1):
                    annontations[i] = 1
            cut_start = None

        if pressed_key == ord('k'):
            annontations[frame_i] = 0

        if pressed_key == ord('s'):
            print(f"Saving annotations to {annontation_path}")
            with open(annontation_path, "w") as fp:
                json.dump(annontations, fp)
except:
    pass
print(f"Saving annotations to {annontation_path}")
with open(annontation_path, "w") as fp:
    json.dump(annontations, fp)
