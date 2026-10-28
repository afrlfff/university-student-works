import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# ===== Задание №1. Нормализация ===== #

image = cv.imread('input_imgs/image3.jpg')
cv.imshow("1. Source image", image)
cv.waitKey(0)

image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("1.1. Grayscale image", image_gray)
cv.waitKey(0)

hist_gray = cv.calcHist([image_gray], [0], None, [256], [0, 256])
plt.figure(); plt.plot(hist_gray)
plt.title('1.2. Histogram of gray'); plt.xlabel('Intensity'); plt.ylabel('Frequensy')
plt.show()

normalized = cv.normalize(image_gray.astype(np.float32), np.zeros_like(image_gray), alpha=63, beta=255, norm_type=cv.NORM_MINMAX)
normalized = np.clip(normalized, 0, 255).astype(np.uint8)
cv.imshow("1.3. Normalized image", normalized)
cv.waitKey(0)

hist_norm = cv.calcHist([normalized], [0], None, [256], [0, 256])
plt.figure(); plt.plot(hist_norm)
plt.title('1.4. Histogram of normlized image'); plt.xlabel('Intensity'); plt.ylabel('Frequensy')
plt.show()

# =================================== #

cv.destroyAllWindows()

# ===== Задание №2. Эквализация ===== #

image = cv.imread('input_imgs/color4.png')
cv.imshow("2. Source image", image)
cv.waitKey(0)

image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("2.1. Grayscale image", image_gray)
cv.waitKey(0)

hist_gray = cv.calcHist([image_gray], [0], None, [256], [0, 10])
plt.figure(); plt.plot(hist_gray); plt.xticks([i * 255/10 for i in range(10 + 1)], [i for i in range(10 + 1)])
plt.title('2.2. Histogram of gray'); plt.xlabel('Intensity'); plt.ylabel('Frequensy')
plt.show()

equalized = cv.equalizeHist(image_gray)
cv.imshow("2.3. Equalized image", equalized)
cv.waitKey(0)

hist_eq = cv.calcHist([equalized], [0], None, [256], [0, 256])
plt.figure(); plt.plot(hist_eq)
plt.title('2.4 Histogram of equalized'); plt.xlabel('Intensity'); plt.ylabel('Frequensy')
plt.show()

# ================================================== #

cv.destroyAllWindows()

# ===== Задание №3. Нормализация + эквализация ===== #

image = cv.imread('input_imgs/image_gray_63-192.jpg')
cv.imshow("3. Source image", image)
cv.waitKey(0)
image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("3.1. Grayscale image", image_gray)
cv.waitKey(0)

hist_gray = cv.calcHist([image_gray], [0], None, [256], [0, 256])
plt.figure(); plt.plot(hist_gray)
plt.title('3.2. Histogram of gray'); plt.xlabel('Intensity'); plt.ylabel('Frequensy')
plt.show()

normalized = cv.normalize(image_gray.astype(np.float32), np.zeros_like(image_gray), alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
normalized = np.clip(normalized, 0, 255).astype(np.uint8)
cv.imshow("3.3. Normalized image", normalized)
cv.waitKey(0)

hist_norm = cv.calcHist([normalized], [0], None, [256], [0, 256])
plt.figure(); plt.plot(hist_norm)
plt.title('3.4. Histogram of normlized image'); plt.xlabel('Intensity'); plt.ylabel('Frequensy')
plt.show()

equalized = cv.equalizeHist(image_gray)
cv.imshow("3.5. Equalized image", equalized)
cv.waitKey(0)

hist_eq = cv.calcHist([equalized], [0], None, [256], [0, 256])
plt.figure(); plt.plot(hist_eq)
plt.title('3.6 Histogram of equalized'); plt.xlabel('Intensity'); plt.ylabel('Frequensy')
plt.show()

# =================================== #