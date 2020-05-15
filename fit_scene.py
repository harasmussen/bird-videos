import cv2
import sys
import time
import json
import os
from sklearn.decomposition import PCA
import numpy as np
import pickle

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [in_video_file] [model]")
    sys.exit(1)


input_video_file = sys.argv[1]
# model_path = sys.argv[2]
model_path = f"output/{os.path.basename(input_video_file)}_model.npz"

if not os.path.isfile(input_video_file):
    print(f"ERROR: {input_video_file} does not exists")
    sys.exit(1)

if os.path.isfile(model_path):
    print(f"ERROR: {model_path} does exists")
    sys.exit(1)

cap = cv2.VideoCapture(input_video_file)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_rate = cap.get(cv2.CAP_PROP_FPS)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

end_frame = 6000

all_frames = []
print(frame_count)
frame_i = 0
bad_frames = 0
while(frame_i < frame_count):
    if frame_i % 100 == 0:
        print(f"{frame_i/frame_count*100:.2f}%")

    good_frame, frame = cap.read()
    if not good_frame:
        frame = last_frame
        bad_frames += 1


    if frame_i > 244 and frame_i % 50 == 0:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        all_frames.append(frame_gray.flatten())

    if frame_i == end_frame:
        break

    last_frame = frame

    frame_i += 1

all_frames_matrix = np.vstack(all_frames)
print(all_frames_matrix.shape)

scene_pca = PCA(n_components=0.8)
scene_pca.fit(all_frames_matrix)
scene_pca_obj = {
    "components_": scene_pca.components_,
    "explained_variance_": scene_pca.explained_variance_,
    "explained_variance_ratio_": scene_pca.explained_variance_ratio_,
    "singular_values_": scene_pca.singular_values_,
    "mean_": scene_pca.mean_,
    "n_components_": scene_pca.n_components_,
    "n_features_": scene_pca.n_features_,
    "n_samples_": scene_pca.n_samples_,
    "noise_variance_": scene_pca.noise_variance_,
}
print("components", scene_pca.n_components_)
print("explained_variance_ratio", scene_pca.explained_variance_ratio_)

np.savez(model_path, **scene_pca_obj)

print(frame_i, bad_frames)
cap.release()


# cv2.imwrite(f"output/mean.png", scene_pca.mean_.reshape(frame_height, frame_width))
# for i, comp in enumerate(scene_pca.components_):
#     com_norm = (255*(comp - np.min(comp))/np.ptp(comp)).astype(int)
#     cv2.imwrite(f"output/comp{i}.png", com_norm.reshape(frame_height, frame_width))
