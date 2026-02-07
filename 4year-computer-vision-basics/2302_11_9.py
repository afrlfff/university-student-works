import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from collections import deque

# ================================================================================

def set_image(img, title):
    plt.title(title)
    plt.axis('off')

    if len(img.shape) == 3 and img.shape[2] == 3:
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap='gray')
        
# ================================================================================

# ========================= Task #1 Global binarization ======================== #

img_gray = cv.imread("input_imgs/adapt_threshold.jpg", cv.IMREAD_GRAYSCALE)

_, threshold_binary = cv.threshold(img_gray, 128, 255, type=cv.THRESH_BINARY)
_, threshold_otsu = cv.threshold(img_gray, 128, 255, type=cv.THRESH_BINARY + cv.THRESH_OTSU)

plt.suptitle("Task #1")
plt.subplot(1, 3, 1)
set_image(img_gray, "Source image")
plt.subplot(1, 3, 2)
set_image(threshold_binary, "THRESH_BINARY")
plt.subplot(1, 3, 3)
set_image(threshold_otsu, "THRESH_OTSU")
plt.tight_layout()
plt.show()

# ========================= Task #2 Adaptive binarization ======================== #

img_gray = cv.imread("input_imgs/adapt_threshold.jpg", cv.IMREAD_GRAYSCALE)

fig, ax = plt.subplots()
plt.suptitle("Task #2. Adaptive threshold test")
plt.subplots_adjust(bottom=0.3)
im = ax.imshow(img_gray, cmap='gray')
ax.axis('off')

def update_image(blockSize, C):
    thresh = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize, C)
    im.set_array(thresh)
    fig.canvas.draw_idle()

sax1 = plt.axes([0.25, 0.1, 0.5, 0.03])
slider_block = Slider(sax1, 'Block Size', 3, 383, valstep=2, valinit=11, valfmt='%d')
slider_block.valtext.set_text(f"{int(slider_block.val)}")

sax2 = plt.axes([0.25, 0.05, 0.5, 0.03])
slider_C = Slider(sax2, 'C', -20, 20, valinit=2, valstep=1, valfmt='%d')

slider_block.on_changed(lambda val: update_image(int(val), slider_C.val))
slider_C.on_changed(lambda val: update_image(int(slider_block.val), int(val)))

slider_block.set_val(3)
slider_C.set_val(2)

plt.show()

# ========================= Task #3 Region growing ======================== #

def region_growing(img, seed, T):
    h, w = img.shape
    segmented = np.zeros((h, w), dtype=np.uint8)
    visited = np.zeros((h, w), dtype=bool)
    
    y0, x0 = seed
    fC = img[y0, x0] # яркость центра кристаллизации
    
    queue = deque([seed])
    segmented[y0, x0] = 255
    visited[y0, x0] = True

    while queue:
        y, x = queue.popleft()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if (0 <= ny < h) and (0 <= nx < w) and (not visited[ny, nx]):
                    if max(img[ny, nx], fC) - min(img[ny, nx], fC) < T: # предикат Q из методички
                        visited[ny, nx] = True
                        segmented[ny, nx] = 255
                        queue.append((ny, nx))
    
    return segmented

img_gray = cv.imread("input_imgs/region_growing.jpg", cv.IMREAD_GRAYSCALE)
_, thresh = cv.threshold(img_gray, 128, 255, cv.THRESH_BINARY)

seeds_xy = [(176, 255), (229, 405), (347, 165)]
seeds_yx = [(y, x) for x, y in seeds_xy]

masks = [region_growing(img_gray, seeds_yx[i], 15) for i in range(3)]

result = np.zeros_like(img_gray)
for mask in masks:
    result = cv.bitwise_or(result, mask)

plt.subplots(1, 2)
plt.suptitle("Task #3")
plt.subplot(1, 2, 1)
set_image(img_gray, "Source Image")
plt.subplot(1, 2, 2)
set_image(result, "Grown regions")
plt.tight_layout()
plt.show()