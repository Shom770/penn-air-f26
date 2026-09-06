import cv2
import numpy as np

base_image = cv2.imread("part_1_image.png")

def contour_shapes(img, bg_lower=(40, 30, 30), bg_upper=(75, 255, 145)):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # determined experimentally
    grass = cv2.inRange(hsv, bg_lower, bg_upper)
    shapes = cv2.bitwise_not(grass)

    # used to remove the small specks here and there
    shapes = cv2.morphologyEx(shapes, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    contours, _ = cv2.findContours(shapes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 500:  # not a shape
            continue

        cv2.drawContours(img, [c], -1, (0, 0, 0), 4)

        # get center by computing the centroid using all of the inner pixels instead of j the boundary
        M = cv2.moments(c)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        cv2.drawMarker(img, (cx, cy), (0, 0, 0), cv2.MARKER_CROSS, 15, 3)

    return img


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

    contours, _ = cv2.findContours(solid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 500:
            continue

        # straighten out the outline if it's jagged
        peri = cv2.arcLength(c, True)
        c = cv2.approxPolyDP(c, 0.002 * peri, True)

        cv2.drawContours(img, [c], -1, (0, 0, 0), 3)

        # fill each shape and get every pixel inside to find the best centroid
        M = cv2.moments(c)
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        cv2.drawMarker(img, (cx, cy), (0, 0, 0), cv2.MARKER_CROSS, 25, 3)

    return img

cv2.imwrite("contoured_pt_1.png", contour_shapes(base_image))