import cv2 as cv
import numpy as np


# ===== Task 1: Refine object using eriosion ===== #
image = cv.imread("input_imgs/type_2G.jpg")
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
eroded = cv.erode(image, kernel, iterations=1)
cv.imshow("1. Source image", image)
cv.waitKey()
cv.imshow("1.1. Result image", eroded)
cv.waitKey()
cv.destroyAllWindows()
# ================================================ #

# ===== Task 2: Exclude little squares (<13px) using erosion ===== #
image = cv.imread("input_imgs/black_sq.jpg")
kernel = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
eroded = cv.erode(image, kernel, iterations=1)
cv.imshow("2. Source image", image)
cv.waitKey()
cv.imshow("2.1. Result image", eroded)
cv.waitKey()
cv.destroyAllWindows()
# ================================================================ #

# ===== Task 3: Thickening after dialtion ===== #
image = cv.imread("input_imgs/type_2G.jpg")
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
dilated = cv.dilate(image, kernel, iterations=1)
cv.imshow("3. Source image", image)
cv.waitKey()
cv.imshow("3.1. Result image", dilated)
cv.waitKey()
cv.destroyAllWindows()
# ============================================= #

# ===== Task 4: Little squares removing using opening (erosion + delation) ===== #
image = cv.imread("input_imgs/black_sq.jpg")
kernel = np.ones((13, 13), np.uint8)
opened = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
cv.imshow("4. Source image", image)
cv.waitKey()
cv.imshow("4.1. Result image", opened)
cv.waitKey()
cv.destroyAllWindows()
# ============================================================================== #

# ===== Task 5: Dilation with different structured objects (5x5) ===== #
image = cv.imread("input_imgs/black_sq.jpg")

square = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
cross = cv.getStructuringElement(cv.MORPH_CROSS, (5, 5))
custom = np.array([
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0]
], dtype=np.uint8)

dilated_square = cv.dilate(image, square)
dilated_cross = cv.dilate(image, cross)
dilated_custom = cv.dilate(image, custom)

cv.imshow("5. Source", image)
cv.waitKey()
cv.imshow("5.1. Dilated square", dilated_square)
cv.waitKey()
cv.imshow("5.2. Dilated cross", dilated_cross)
cv.waitKey()
cv.imshow("5.3. Dilated custom object", dilated_custom)
cv.waitKey()
cv.destroyAllWindows()
# ==================================================================== #

# ===== Task 6: Remove salt noise using opening ===== #
image = cv.imread("input_imgs/type_j_open.jpg", cv.IMREAD_GRAYSCALE)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
opened = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
cv.imshow("6. Source image", image)
cv.waitKey()
cv.imshow("6.1. Result image", opened)
cv.waitKey()
cv.destroyAllWindows()
# ================================================== #

# ===== Task 7: Remove pepper noise using closing ===== #
image = cv.imread("input_imgs/type_j_close.jpg", cv.IMREAD_GRAYSCALE)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
closed = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
cv.imshow("7. Source image", image)
cv.waitKey()
cv.imshow("7.1. Result image", closed)
cv.waitKey()
cv.destroyAllWindows()
# ==================================================== #

# ===== Task 8: Edge contour using morphological gradient ===== #
image = cv.imread("input_imgs/type_j.jpg", cv.IMREAD_GRAYSCALE)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
gradient = cv.morphologyEx(image, cv.MORPH_GRADIENT, kernel)
cv.imshow("8. Source image", image)
cv.waitKey()
cv.imshow("8.1. Result image", gradient)
cv.waitKey()
cv.destroyAllWindows()
# ============================================================ #

# ===== Task 9: TopHat — highlight bright spots and extract noise ===== #
image1 = cv.imread("input_imgs/type_j.jpg", cv.IMREAD_GRAYSCALE)
image2 = cv.imread("input_imgs/type_j_open.jpg", cv.IMREAD_GRAYSCALE)

kernel1 = cv.getStructuringElement(cv.MORPH_RECT, (6, 6))
kernel2 = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

tophat1 = cv.morphologyEx(image1, cv.MORPH_TOPHAT, kernel1)
tophat2 = cv.morphologyEx(image2, cv.MORPH_TOPHAT, kernel2)

cv.imshow(f"9.1. Source image #1", image1)
cv.waitKey()
cv.imshow(f"9.2. Result #1", tophat1)
cv.waitKey()
cv.imshow(f"9.3. Source image #2", image2)
cv.waitKey()
cv.imshow(f"9.4. Result #2", tophat2)
cv.waitKey()
cv.destroyAllWindows()
# ===================================================================== #

# ===== Task 10: BlackHat — detect darker regions ===== #
image = cv.imread("input_imgs/type_j.jpg", cv.IMREAD_GRAYSCALE)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (6, 6))
blackhat = cv.morphologyEx(image, cv.MORPH_BLACKHAT, kernel)
cv.imshow(f"10. Source image #1", image)
cv.waitKey()
cv.imshow(f"10.1. Result #1", blackhat)
cv.waitKey()
cv.destroyAllWindows()
# ====================================================== #