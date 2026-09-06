# PennAir Technical Challenge

This project uses OpenCV to detect shapes, draw their contours and centers, and estimate their 3D positions.

## Setup

Python 3.10 or newer is recommended.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run all commands from the project root so the scripts can find the input files.

## Run each part
#### WARNING: THE CODE WON'T RUN WITHOUT UPLOADING PART 2-4 VIDEOS BECAUSE GITHUB WON'T LET ME PUSH FILES THAT LARGE.

### Part 1

Detects the shapes in `part_1_image.png`, draws their contours and centers, and saves the result.

```bash
python3 part_1.py
```

Output: `contoured_pt_1.png`

### Part 2

Processes `part_2.mp4` frame by frame using the shape detection from Part 1.

```bash
python3 part_2.py
```

Output: `contoured_part_2.mp4`

### Part 3

Builds a background image from sampled frames of `part_3.mp4`, then detects and marks the moving shapes.

```bash
python3 part_3.py
```

Output: `contoured_part_3.mp4`

### Part 4

Processes `part_3.mp4` and labels each detected shape with estimated X, Y, and Z coordinates in inches.

```bash
python3 part_4.py
```

Output: `contoured_part_4.mp4`

Each run overwrites the existing output file for that part.

## Videos
Part 1:
<br>
<img width="360" height="180" alt="contoured_pt_1" src="https://github.com/user-attachments/assets/bd8e30e7-0e7a-4fe4-95af-dbb3d2c0cde0" />

Part 2: (click on the image to watch the video)
<br><a href="http://www.youtube.com/watch?feature=player_embedded&v=Kc75BvfTFmw" target="_blank">
 <img src="http://img.youtube.com/vi/Kc75BvfTFmw/mqdefault.jpg" alt="Watch the video" width="360" height="180" border="10" />
</a>

Part 3: 
<br><a href="http://www.youtube.com/watch?feature=player_embedded&v=WJv-GCt1QYg" target="_blank">
 <img src="http://img.youtube.com/vi/WJv-GCt1QYg/mqdefault.jpg" alt="Watch the video" width="360" height="180" border="10" />
</a>

Part 4: 
<br><a href="http://www.youtube.com/watch?feature=player_embedded&v=CBpOrDrj4SU" target="_blank">
 <img src="http://img.youtube.com/vi/CBpOrDrj4SU/mqdefault.jpg" alt="Watch the video" width="360" height="180" border="10" />
</a>

## Bugs I Ran Into
Part 1-4)
I wasn't able to keep the outlines of the shapes separate. When shapes would collide, the program would process it as one large polygon. I debated using the corners to detect the shape and to treat the circle as a dodecahedron or some shape with a large number of sides, but I wouldn't be able to identify which corner I was looking at and draw the whole outline accordingly.
I also had trouble with tracking the centers of the objects. When the object would go off screen, the center would jump to whatever part of the shape remained in frame rather than following the true center, since the algorithm works by averaging out every point inside the contour and getting the centroid from that rather than following the true shape at all times.

Part 4)
When the circle collides with other shapes, the program is unable to detect the circle, meaning that it can't calculate the depth and thus the measurements disappear for a little. However, I wasn't able to fix it without overhauling the algorithm from Part 1-4 entirely.

Part 5)
My MacBook was really struggling to run ROS, so for time constraints, I decided to make do with Parts 1-4.
