import cv2
import numpy as np

K = np.array([
    [2564.3186869, 0, 0],
    [0, 2569.70273111, 0],
    [0, 0, 1]
])
Kinv = np.linalg.inv(K)
RADIUS_OF_CIRCLE = 10

# modify algo from part 1 -> mark depth and x, y as well
def contour_shapes_for_video(img, first_frame):
    # subtract every frame against the initial frame
    diff = cv2.absdiff(img, first_frame).max(axis=2)
    edges = cv2.Canny(diff, 30, 90) # find steep differences in the diff mask
    edges = cv2.dilate(edges, np.ones((7, 7), np.uint8), iterations=2)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # turn the contours into solid objects so any gaps (what i call 'fjords' that aren't accounted for) can be filled
    solid = np.zeros(edges.shape, np.uint8)
    cv2.drawContours(solid, contours, -1, 255, -1)
    solid = cv2.morphologyEx(solid, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    solid = cv2.erode(solid, np.ones((4, 4), np.uint8), iterations=3)

    all_shapes = []
    Z = None
    contours, _ = cv2.findContours(solid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 500:
            continue

        # straighten out the outline if it's jagged
        peri = cv2.arcLength(c, True)
        c = cv2.approxPolyDP(c, 0.002 * peri, True)

        # fill each shape and get every pixel inside to find the best centroid
        M = cv2.moments(c)
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        all_shapes.append((c, cx, cy))

        # first find the circle so we can calculate the depth of every shape using circularity formula
        circularity = 4 * np.pi * cv2.contourArea(c) / (peri ** 2)
        if circularity > 0.85:
            (_, _), r_px = cv2.minEnclosingCircle(c)
            Z = K[0, 0] * RADIUS_OF_CIRCLE / r_px

    for c, cx, cy in all_shapes:
        cv2.drawContours(img, [c], -1, (0, 0, 0), 3)
        cv2.drawMarker(img, (cx, cy), (0, 0, 0), cv2.MARKER_CROSS, 25, 3)

        if Z is not None:
            X, Y, _ = Z * (Kinv @ np.array([cx, cy, 1.0])) # Kinv * [x, y, 1]T = real position
            cv2.putText(img, f"X={X:.1f} Y={Y:.1f} Z={Z:.1f} in", (cx + 15, cy - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return img


# copy script from pt 3
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

out = cv2.VideoWriter("contoured_part_4.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
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

