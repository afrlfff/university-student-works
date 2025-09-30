import cv2 as cv
import numpy as np

# ===== Основные функции ===== #

def log_transform(image, c=1.0):
    return c * np.log(1 + image)

def gamma_correction(image_norm, gamma=1.0, c=1.0):
    return c * np.power(image_norm, gamma)

def piecewise_linear(image, r1, s1, r2, s2):
    result = np.zeros_like(image)
    mask1 = image < r1
    mask2 = (image >= r1) & (image <= r2)
    mask3 = image > r2

    result[mask1] = (s1 / r1) * image[mask1]
    result[mask2] = s1 + ((s2 - s1) / (r2 - r1)) * (image[mask2] - r1)
    result[mask3] = s2 + ((255 - s2) / (255 - r2)) * (image[mask3] - r2)
    return result

# ============================ #

# ===== Задание №1. Градационные преобразования ===== #

# Чтение изображения
image = cv.imread('input_imgs/moscow.jpg', cv.IMREAD_GRAYSCALE).astype(np.float32)

# 1.1. Логарифмическое преобразование
с = 255 / np.log(1 + np.max(image))
log_result = log_transform(image, c=с)

# 1.2. Степенное преобразование
image_norm = image / 255.0
gammas = [0.1, 0.5, 1.2, 2.2]
gamma_results = []
for gamma in gammas:
    gamma_result = gamma_correction(image_norm, gamma=gamma, c=1.0)
    gamma_results.append(gamma_result * 255)

# 1.3. Кусочно-линейное преобразование
piecewise_result = piecewise_linear(image, r1=70, s1=0, r2=140, s2=255)

# Преобразуем к uint8
log_result = np.array( log_result, dtype=np.uint8 )
gamma_results = [ np.array( gamma_result, dtype=np.uint8 ) for gamma_result in gamma_results ]
piecewise_result = np.array( piecewise_result, dtype=np.uint8 )

# Показ результатов
cv.imshow("1. Source image", np.array(image, dtype=np.uint8))
cv.waitKey(0)
cv.imshow("1.1 Logarithmic transformation", log_result)
cv.waitKey(0)
for gamma_result in gamma_results:
    cv.imshow("1.2. Gamma transformation", gamma_result)
    cv.waitKey(0)
cv.imshow("1.3. Piecewise-linear transformation", piecewise_result)
cv.waitKey(0)

# =================================================== #

cv.destroyAllWindows()

# =================================================== #

# ===== Задание №2. Логические операции ===== #

# Создание тестовых изображений
img1 = np.zeros((200, 400, 1), dtype=np.uint8)
cv.fillPoly(img1, [np.array([(0, 0), (0, 200), (200, 200), (200, 0)])], (255, 255, 255))
img2 = np.zeros((200, 400, 1), dtype=np.uint8)
cv.fillPoly(img2, [np.array([(150, 100), (300, 100), (300, 150), (150, 150)])], (255, 255, 255))

# Сохранение изображений
cv.imwrite('output_imgs/drawing1.jpg', img1)
cv.imwrite('output_imgs/drawing2.jpg', img2)

# Вычисление битовых операций
bitwise_not = [cv.bitwise_not(img1), cv.bitwise_not(img2)]
bitwise_and = cv.bitwise_and(img1, img2)
bitwise_or = cv.bitwise_or(img1, img2)
bitwise_xor = cv.bitwise_xor(img1, img2)

# Показ результатов
cv.imshow("2. Source image #1", img1)
cv.waitKey(0)
cv.imshow("2. Source image #2", img2)
cv.waitKey(0)
cv.imshow("2.1. Bitwise not #1", bitwise_not[0])
cv.waitKey(0)
cv.imshow("2.1. Bitwise not #2", bitwise_not[1])
cv.waitKey(0)
cv.imshow("2.2. Bitwise and", bitwise_and)
cv.waitKey(0)
cv.imshow("2.3. Bitwise or", bitwise_or)
cv.waitKey(0)
cv.imshow("2.4. Bitwise xor", bitwise_xor)
cv.waitKey(0)

# =========================================== #
