import cv2 as cv
import numpy as np

# ================================ Task #1. Affine transformations ================================= #

image = cv.imread("input_imgs/cat.jpg")
h, w, ch = image.shape
center = (w/2, h/2)

cv.imshow("1. Source image", image)
cv.waitKey()

# =============== 1.1. Rotation
M = cv.getRotationMatrix2D(center, 45, 1)
transformed = cv.warpAffine(image, M, dsize=(w*2, h*2))

cv.imshow("1.1. Rotation", transformed)
cv.waitKey()

# =============== 1.2. Scale
transformed = cv.resize(image, (int(w/2), h))
cv.imshow("1.2. Downscale (using resize)", transformed)
cv.waitKey()

M = np.array([
    [0.5, 0, 0],
    [0, 1, 0]
], dtype=np.float64)

transformed = cv.warpAffine(image, M, dsize=(w, h))
cv.imshow("1.2. Downscale (using custom matrix)", transformed)
cv.waitKey()

# =============== 1.3. Move
M = np.array([
    [1, 0, 50],
    [0, 1, 50]
], dtype=np.float64)
transformed = cv.warpAffine(image, M, dsize=(w*2, h*2))

cv.imshow("1.3. Move on (50, 50)", transformed)
cv.waitKey()

# =============== 1.4. Reflection
M = np.array([
    [-1, 0, w - 1],
    [0, -1, h - 1]
], dtype=np.float64)
transformed = cv.warpAffine(image, M, dsize=(w, h))
cv.imshow("1.4. Reflection (X and Y)", transformed)
cv.waitKey()

# =============== 1.5. Scew
M = np.array([
    [1, 0.2, 0],
    [0.2, 1, 0]
], dtype=np.float64)
transformed = cv.warpAffine(image, M, dsize=(w*2, h*2))
cv.imshow("1.4. Scew (k=0.2)", transformed)
cv.waitKey()

# ================================================================================================== #

cv.destroyAllWindows()

# =============================== Task #2. Homography transformations ============================== #

image1 = cv.imread("input_imgs/book1.jpg")
image2 = cv.imread("input_imgs/book2.jpg")
image3 = cv.imread("input_imgs/times-square.jpg")
image4 = cv.imread("input_imgs/first-image.jpg")
h1, w1, _ = image1.shape
h2, w2, _ = image2.shape
h3, w3, _ = image3.shape
h4, w4, _ = image4.shape

book1_corners = np.int32([[323, 259], [534, 375], [316, 671], [73, 477]])
book2_corners = np.int32([[156, 136], [480, 165], [494, 632], [80, 605]])
times_square_board_corners = np.int32([
    [116, 215], [284, 362], [249, 448], [34, 335]
])

#cv.fillPoly(image1, [book1_corners], (255, 0, 0))
#cv.fillPoly(image2, [book2_corners], (255, 0, 0))

cv.imshow("2. Source image (book1.jpg)", image1)
cv.waitKey()

cv.imshow("2. Source image (book2.jpg)", image2)
cv.waitKey()

# =============== 2.1. align book2 to book1
H, mask = cv.findHomography(
    np.float64(book2_corners),
    np.float64(book1_corners)
)

transformed = cv.warpPerspective(image2, H, dsize=(w1, h1))
cv.imshow("2.1. Align book2 to book1", transformed)
cv.waitKey()


# =============== 2.2. Get book1 cover
H, mask = cv.findHomography(
    np.float64(book1_corners),
    np.float64([[0, 0], [w1, 0], [w1, h1], [0, h1]])
)

transformed = cv.warpPerspective(image1, H, dsize=(w1, h1))
cv.imshow("2.1. Book1's cover", transformed)
cv.waitKey()

# =============== 2.3. Set new advertisment in Times Square
cv.imshow("2.3. Source image (timer-square.jpg)", image3)
cv.waitKey()

cv.imshow("2.3. Source image (first-image.jpg)", image4)
cv.waitKey()

H, mask = cv.findHomography(
    np.float64([[0, 0], [w4, 0], [w4, h4], [0, h4]]),
    np.float64(times_square_board_corners)
)

transformed = cv.warpPerspective(image4, H, dsize=(w3, h3))
cv.imshow("2.3. Transformed advertisment", transformed)
cv.waitKey()

overlay = image3.copy()
cv.fillConvexPoly(overlay, times_square_board_corners, (0, 0, 0))
overlay += transformed
cv.imshow("2.3. Times Square new advertisment", overlay)
cv.waitKey()

# ================================================================================================== #

cv.destroyAllWindows()

# ================================================================================================== #
