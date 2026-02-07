import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# ================================================================================

def set_image(img, title):
    plt.title(title)
    plt.axis('off')

    if len(img.shape) == 3 and img.shape[2] == 3:
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap='gray')

# ================================================================================

# ========================= Task #1 Canny Edge Detector ======================== #

img = cv.imread("input_imgs/cat.jpg")

edges_canny = cv.Canny(img, threshold1=50, threshold2=200)

plt.suptitle("Task #1")
plt.subplot(1, 2, 1)
set_image(img, "Source image")
plt.subplot(1, 2, 2)
set_image(edges_canny, "Canny edges (50, 200)")
plt.show()

# ====================== Task #2 Smoothing before Gradient ===================== #


def apply_gradient_transformations(img, title):
    sobel_x = cv.Sobel(img, -1, 1, 0, ksize=3)
    sobel_y = cv.Sobel(img, -1, 0, 1, ksize=3)
    sobel_abs_x = cv.convertScaleAbs(sobel_x)
    sobel_abs_y = cv.convertScaleAbs(sobel_y)
    sobel_combined = cv.addWeighted(sobel_abs_x, 0.5, sobel_abs_y, 0.5, 0)
    scharr_x = cv.Scharr(img, -1, 1, 0)
    scharr_y = cv.Scharr(img, -1, 0, 1)
    scharr_abs_x = cv.convertScaleAbs(scharr_x)
    scharr_abs_y = cv.convertScaleAbs(scharr_y)
    scharr_combined = cv.addWeighted(scharr_abs_x, 0.5, scharr_abs_y, 0.5, 0)
    laplacian = cv.Laplacian(img, -1)
    laplacian_abs = cv.convertScaleAbs(laplacian)
    canny_edges = cv.Canny(img, 50, 200)

    plt.figure(figsize=(10, 4))
    plt.suptitle(title)
    plt.subplot(2, 4, 1)
    set_image(img, "Source image")
    plt.subplot(2, 4, 5)
    set_image(sobel_combined, "Sobel")
    plt.subplot(2, 4, 6)
    set_image(scharr_combined, "Scharr")
    plt.subplot(2, 4, 7)
    set_image(laplacian_abs, "Laplasian")
    plt.subplot(2, 4, 8)
    set_image(canny_edges, "Canny")
    plt.show()

img1 = cv.imread("input_imgs/cat.jpg")
img2 = cv.imread("input_imgs/cat_gauss_noise.jpg")

img2_gauss_filtered = cv.GaussianBlur(img2, (5, 5), 0)

plt.figure(figsize=(10, 4))
plt.suptitle("Task #2. Source images")
plt.subplot(1, 3, 1)
set_image(img1, "cat.jpg")
plt.subplot(1, 3, 2)
set_image(img2, "cat_gauss_noise.jpg")
plt.subplot(1, 3, 3)
set_image(img2_gauss_filtered, "Filtered cat_gauss_noise.jpg")
plt.tight_layout()
plt.show()

img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2_gray = cv.cvtColor(img2_gauss_filtered, cv.COLOR_BGR2GRAY)

apply_gradient_transformations(img1_gray, "Task #2. Result images for cat.jpg")

apply_gradient_transformations(img2_gray, "Task #2. Result images for cat_gauss_noise.jpg")


# ==================== Task #3 Contour Detection and Analysis ================== #
img = cv.imread("input_imgs/max_area_contour.jpg")
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_test = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

_, thresh = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

areas = [cv.contourArea(c) for c in contours]
perimeters = [cv.arcLength(c, closed=True) for c in contours]

set_image(img, "Task #3. Source image (max_area_contour.jpg)")
plt.show()

plt.suptitle("Task #3. Found contours")
for i, contour in enumerate(contours):
    img_test[:] = (225, 225, 225)
    plt.subplot(2, 3, i + 1)
    cv.drawContours(img_test, contours, i, (255, 0, 0), thickness=3)
    set_image(img_test, f"S={areas[i]:.2f}\nP={perimeters[i]:.2f}")

plt.tight_layout()
plt.show()

# ===== 3.1.
max_area_idx = np.argmax(areas[:-1])
max_area_val = areas[max_area_idx]

img_test[:] = (225, 225, 225)
cv.drawContours(img_test, contours, max_area_idx, (255, 0, 0), thickness=3)
set_image(img_test, "Task #3. Maximum area")
plt.show()

# ===== 3.2.
max_perimeter_idx = np.argmax(perimeters[:-1])
max_perimeter_val = perimeters[max_perimeter_idx]

img_test[:] = (225, 225, 225)
cv.drawContours(img_test, contours, max_perimeter_idx, (255, 0, 0), thickness=3)
set_image(img_test, "Task #3. Maximum perimeter")
plt.show()

# ===== 3.3.
epsilon = 0.01 * max_perimeter_val
approx = cv.approxPolyDP(contours[max_perimeter_idx], epsilon, closed=True)

img_test[:] = (225, 225, 225)
cv.drawContours(img_test, [approx], -1, (255, 0, 0), thickness=3)
set_image(img_test, f"Task #3. Maximum perimeter approximation\neps={epsilon:.3f}")
plt.show()

# ===== 3.4.
img = cv.imread("input_imgs/goal_contour_star.jpg")
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_test = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

_, thresh = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
target_contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
target_contour = target_contours[0] # star contour

match_coeffs = []
for i, contour in enumerate(contours):
    match_coeff = cv.matchShapes(contour, target_contour, 1, 0.0)
    match_coeffs.append(match_coeff)
match_coeffs = np.array(match_coeffs)

best_match_idx = np.argmin(match_coeffs)
best_match_coeff = match_coeffs[best_match_idx]
best_match_contour = contours[best_match_idx]

set_image(img, "Task #3. Source image (goal_contour_star.jpg)")
plt.show()

img_test[:] = (225, 225, 225)
cv.drawContours(img_test, [target_contour], -1, (0, 0, 255), thickness=3)
set_image(img_test, "Task #3. Found contour (goal_contour_star.jpg)")
plt.show()

plt.suptitle("Mathces")
for i, contour in enumerate(contours):
    plt.subplot(2, 3, i + 1)
    img_test[:] = (225, 225, 225)
    cv.drawContours(img_test, [target_contour], -1, (0, 0, 255), thickness=3)
    cv.drawContours(img_test, [contour], -1, (255, 0, 0), thickness=3)
    set_image(img_test, f"coeff={match_coeffs[i]:.6f}")
plt.show()

plt.suptitle(f"Best match (k = {best_match_coeff})")
plt.subplot(1, 2, 1)
img_test[:] = (225, 225, 225)
cv.drawContours(img_test, [best_match_contour], 0, (255, 0, 0), thickness=3)
set_image(img_test, "max_area_contour.jpg")
plt.subplot(1, 2, 2)
img_test[:] = (225, 225, 225)
cv.drawContours(img_test, [target_contour], 0, (0, 0, 255), thickness=3)
set_image(img_test, "goal_contour_star.jpg")
plt.show()

# ==================== Task #4. Hough Line ================== #
img = cv.imread("input_imgs/image0.jpg")
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

edges = cv.Canny(img_gray, 50, 200)

set_image(img, "Task #4. Source image")
plt.show()

# ===== 4.1. Standard Hough
lines = cv.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=100)

img_hough = img.copy()
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv.line(img_hough, (x1, y1), (x2, y2), (0, 0, 255), 2)

set_image(img_hough, "Standard Hough")
plt.show()

# ===== 4.2. Probabilistic Hough
lines = cv.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=10, minLineLength=50, maxLineGap=10)

img_hough = img.copy()
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img_hough, (x1, y1), (x2, y2), (0, 255, 0), 2)

set_image(img_hough, "Probabilistic Hough")
plt.show()

# ===================================================================== #