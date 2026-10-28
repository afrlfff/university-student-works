import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# ================================================================================

def get_magnitude_spectrum(fshift):
    magnitude = np.abs(fshift)
    magnitude = np.log(magnitude + 1)
    magnitude = np.fft.ifftshift(magnitude)
    return magnitude

# ================================================================================

def butterworth_lowpass_filter(shape, D0, n=2):
    P, Q = shape
    u = np.arange(P)
    v = np.arange(Q)
    u = u - P // 2
    v = v - Q // 2
    U, V = np.meshgrid(v, u)
    D = np.sqrt(U**2 + V**2)
    H = 1 / (1 + (D / D0)**(2*n))
    return H

# ================================================================================

def set_image(img, title, cmap='gray'):
    plt.title(title)
    plt.imshow(img, cmap=cmap)
    plt.axis('off')

# ================================================================================

def apply_butterworth_filter(img, D0, n=2):
    if len(img.shape) == 3:
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY).astype(np.float32)
    else:
        img_gray = img.astype(np.float32)

    dft = np.fft.fft2(img_gray)
    dft_shift = np.fft.fftshift(dft)

    # make filter
    H = butterworth_lowpass_filter(img_gray.shape, D0, n)

    # apply filter
    filtered_dft = dft_shift * H

    # inverse transformation
    dft_ishift = np.fft.ifftshift(filtered_dft)
    img_back = np.fft.ifft2(dft_ishift)
    img_back = np.abs(img_back)

    return img_back, H, dft_shift

# ================================================================================

# ===== Task 1: Butterworth low-pass filter ===== #
img = cv.imread("input_imgs/white_sq.jpg")
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY).astype(np.float32)

# Амплитудный спектр исходного изображения
dft = np.fft.fft2(img_gray)
dft_shift = np.fft.fftshift(dft)
mag = get_magnitude_spectrum(dft_shift)

# NOTE: uncomment to test filter
    #for i, n in enumerate([1, 2, 5, 20]):
    #    plt.subplot(1, 4, i + 1)
    #    H = butterworth_lowpass_filter(img_gray.shape, D0=5, n=n)
    #    set_image(H, f"n={n}")
    #plt.tight_layout()
    #plt.show()

H = butterworth_lowpass_filter(img_gray.shape, 5)
G = dft_shift * H
g = np.fft.ifft2(np.fft.ifftshift(G))
filtered_img = np.real(g)

filtered_dft = np.fft.fft2(filtered_img)
filtered_dft_shift = np.fft.fftshift(filtered_dft)
filtered_mag = get_magnitude_spectrum(filtered_dft_shift)

plt.suptitle("Task #1")
plt.subplot(1, 2, 1)
set_image(img_gray, "Source image")
plt.subplot(1, 2, 2)
set_image(mag, "Amplitude spectrum")
plt.show()

D0_values = [0.05, 0.5, 10.0]
for i, D0 in enumerate(D0_values):
    H = butterworth_lowpass_filter(img_gray.shape, D0)
    G = dft_shift * H
    g = np.fft.ifft2(np.fft.ifftshift(G))
    filtered_img = np.real(g)

    plt.subplot(1, 3, i + 1)
    set_image(filtered_img, f'D0 = {D0}')

plt.suptitle('Task #1. Butterworth low-pass filter')
plt.tight_layout()
plt.show()

# ================================================ #

# ===== Task 2: Showing that: forward fft + back fft = source ===== #
img = cv.imread("input_imgs/moscow.jpg")
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY).astype(np.float32)

dft = np.fft.fft2(img_gray)
dft_shift = np.fft.fftshift(dft)
mag = get_magnitude_spectrum(dft_shift)

dft_ishift = np.fft.ifftshift(dft_shift)
img_back = np.fft.ifft2(dft_ishift)
img_back = np.real(img_back)

plt.suptitle("Task #2")

plt.subplot(1, 3, 1)
set_image(img_gray, "Source image")
plt.subplot(1, 3, 2)
set_image(mag, "Amplitude spectrum")
plt.subplot(1, 3, 3)
set_image(img_back, "Result")

plt.tight_layout()
plt.show()

# ================================================================= #