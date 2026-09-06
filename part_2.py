import cv2
from part_1 import contour_shapes

video = cv2.VideoCapture("part_2.mp4")

# grab video properties so output matches
fps = video.get(cv2.CAP_PROP_FPS)
w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter("contoured_part_2.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
ct = 0

while True:
    ret, frame = video.read()
    ct += 1

    if not ret:
        break

    out.write(contour_shapes(frame))

    if ct % 30 == 0:
        print(f"{ct // 30}s processed of video")  # just so i can know how fast the script is running

video.release()
out.release()


