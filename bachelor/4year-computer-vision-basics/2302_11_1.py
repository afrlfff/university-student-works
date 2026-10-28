import cv2 as cv
import numpy as np

# make background square
image = np.zeros((400, 400, 3), dtype=np.uint8)

# draw line
cv.line(image, (15, 20), (70, 50), (0, 255, 0), thickness=2)

# draw circle
cv.circle(image, (200, 200), 32, (255, 0, 0), thickness=2)

# draw ellipse
cv.ellipse(image, (200, 200), (100, 160), 45, 0, 360, (0, 0, 255), thickness=2)

# draw rectangle
cv.rectangle(image, (15, 20), (70, 50), (0, 255, 255), thickness=2)

# initialize polygon points
poly_points = np.array([
    [0, 70], [8, 70], [18, 25], [0, 25], [0, 0],
    [12, 0], [12, 13], [24, 13], [24, 0], [36, 0], 
    [36, 13], [48, 13], [48, 0], [60, 0], [60, 25], 
    [42, 25], [52, 70], [60, 70], [60, 75], [0, 75]
], dtype=np.int32)

# draw polygons
cv.fillPoly(image,  [np.array([55*1 + 60*0, 320]) + poly_points], (255, 255, 255))
cv.polylines(image, [np.array([55*2 + 60*1, 320]) + poly_points], True, (255, 255, 255))
cv.polylines(image, [np.array([55*3 + 60*2, 320]) + poly_points], False, (255, 255, 255))

# draw text
cv.putText(image, 
           text="Hello, world!", 
           org=(20, 375),
           fontFace=cv.FONT_ITALIC, 
           fontScale=0.8, 
           color=(128, 0, 128), 
           thickness=2
           )

cv.putText(image, 
           text="Hello, world!", 
           org=(80, 50),
           fontFace=cv.FONT_HERSHEY_SCRIPT_COMPLEX, 
           fontScale=1.0, 
           color=(255, 255, 0), 
           thickness=2
           )

# show result
cv.imshow("Work 1", image)
cv.waitKey(0)

# save result
cv.imwrite('result.jpg', image)