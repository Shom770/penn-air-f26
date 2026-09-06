import cv2
import numpy as np
from part_1 import contour_shapes_for_video

video = cv2.VideoCapture("part_3.mp4")

# grab video properties so output matches
fps = video.get(cv2.CAP_PROP_FPS)
total = video.get(cv2.CAP_PROP_FRAME_COUNT)

# Grab background by sampling 25 frames and grabbing the median of every frame at every point to get an empty background
indices = np.linspace(0, total - 1, 25).astype(int)
samples = []

for idx in indices:
    video.set(cv2.CAP_PROP_POS_FRAMES, idx) # jump around the frames
    ret, frame = video.read()
    if ret:
        samples.append(frame)

bg = np.median(np.stack(samples), axis=0).astype(np.uint8)
video.set(cv2.CAP_PROP_POS_FRAMES, 0)

w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter("contoured_part_3.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
ct = 0

while True:
    ret, frame = video.read()
    ct += 1

    if not ret:
        break

    out.write(contour_shapes_for_video(frame, bg))

    if ct % 30 == 0:
        print(f"{ct // 30}s processed of video")  # just so i can know how fast the script is running

video.release()
out.release()


