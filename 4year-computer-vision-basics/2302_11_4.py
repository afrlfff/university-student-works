import cv2 as cv
import numpy as np

# ===== Задание №1. Линейный фильтр ===== #
kernel = np.array([
    -0.1, 0.2, -0.1, \
    0.2, 3.0, 0.2, \
    -0.1, 0.2, -0.1
])

image = cv.imread('input_imgs/image0.jpg')
cv.imshow("1. Source image", image)
cv.waitKey()

image_filtered = cv.filter2D(image, -1, kernel)
cv.imshow("1.1. Filtered image", image_filtered)
cv.waitKey()

# ======================================= #

cv.destroyAllWindows()

# ===== Задание №2. Линейный арифметический взвешенный усредняющий фильтр (ФНЧ) ===== #

max_dist = np.sqrt(8)
kernel = np.zeros((5, 5), dtype=np.float32)
cetner = 2

for i in range(5):
    for j in range(5):
        dist = np.sqrt((i - cetner)**2 + (j - cetner)**2)
        kernel[i, j] = (max_dist - dist) / max_dist

kernel /= sum(kernel) # нормировка

image = cv.imread('input_imgs/image0.jpg')
cv.imshow("2. Source image", image)
cv.waitKey()

image_filtered = cv.filter2D(image, -1, kernel)
cv.imshow("2.1. Filtered image", image_filtered)
cv.waitKey()

# =================================================================================== #

cv.destroyAllWindows()

# ===== Задание №3. Линейный арифметический однородный усредняющий фильтр + фильтр Гаусса ===== #

image = cv.imread('input_imgs/image0.jpg')
cv.imshow("3. Source image", image)
cv.waitKey()

image_box_filtered = cv.boxFilter(image, -1, (5, 5), normalize=False)
cv.imshow("3.1. Box-filtered image (without normalization)", image_box_filtered)
cv.waitKey()

image_box_filtered = cv.boxFilter(image, -1, (5, 5), normalize=True)
cv.imshow("3.2. Box-filtered image (with normalization)", image_box_filtered)
cv.waitKey()

image_gauss_filtered = cv.GaussianBlur(image, (5, 5), 0)
cv.imshow("3.3. Gaussian-blured image", image_gauss_filtered)
cv.waitKey()

# ============================================================================================= #

cv.destroyAllWindows()

# ===== Задание №4. Нелинейный медианный и двунаправленный фильтр ===== #

image = cv.imread('input_imgs/image0.jpg')
cv.imshow("4. Source image", image)
cv.waitKey()

image_median_filtered = cv.medianBlur(image, 5)
cv.imshow("4.1. Median-filtered image", image_median_filtered)
cv.waitKey()

image_bilateral_filtered = cv.bilateralFilter(image, -1, 10, 5)
cv.imshow("4.2. Bilateral-filtered image", image_bilateral_filtered)
cv.waitKey()

# ===================================================================== #

cv.destroyAllWindows()

# ===== Задание №5. Фильтр повышения резкости ===== #

prewitt_x = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
], dtype=np.float32)

prewitt_y = np.array([
    [-1, -1, -1],
    [ 0,  0,  0],
    [ 1,  1,  1]
], dtype=np.float32)

laplassian_mod = np.array([
    0, -1, 0,
    -1, 5, -1,
    0, -1, 0
])

image = cv.imread('input_imgs/cat.jpg')
cv.imshow("5. Source image", image)
cv.waitKey()

image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("5.1 Gray image", image_gray)
cv.waitKey()

image_prewitt_x = cv.filter2D(image_gray, -1, prewitt_x)
cv.imshow("5.2. Prewitt-x", image_prewitt_x)
cv.waitKey()

image_prewitt_y = cv.filter2D(image_gray, -1, prewitt_y)
cv.imshow("5.3. Prewitt-y", image_prewitt_y)
cv.waitKey()

image_sobel_x = cv.Sobel(image_gray, -1, 1, 0, ksize=3)
cv.imshow("5.4. Sobel-x", image_sobel_x)
cv.waitKey()

image_sobel_y = cv.Sobel(image_gray, -1, 0, 1, ksize=3)
cv.imshow("5.5. Sobel-y", image_sobel_y)
cv.waitKey()

image_scharr_x = cv.Scharr(image_gray, -1, 1, 0)
cv.imshow("5.6. Scharr-x", image_scharr_x)
cv.waitKey()

image_scharr_y = cv.Scharr(image_gray, -1, 0, 1)
cv.imshow("5.7. Scharr-y", image_scharr_y)
cv.waitKey()

image_laplassian = cv.Laplacian(image_gray, -1, ksize=3)
cv.imshow("5.8. Laplassian", image_laplassian)
cv.waitKey()

image_laplassian_mod = cv.filter2D(image_gray, -1, laplassian_mod)
cv.imshow("5.8. Laplassian modified", image_laplassian_mod)
cv.waitKey()


# ================================================= #