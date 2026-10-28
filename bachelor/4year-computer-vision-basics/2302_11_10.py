import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# ================================================================================

face_cascade = cv.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
eyes_cascade = cv.CascadeClassifier('cascades/haarcascade_eye.xml')

# ================================================================================

def set_image(img, title):
    plt.title(title)
    plt.axis('off')

    if len(img.shape) == 3 and img.shape[2] == 3:
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap='gray')
        
# ================================================================================

# ========================= Task #1 Harris corner detection ======================== #

img_gray = cv.imread("input_imgs/test_image_Smith.jpg", cv.IMREAD_GRAYSCALE).astype(np.float32)

threshold_params = [0.01, 0.05, 0.1]

dst = cv.cornerHarris(img_gray, 2, 3, k=0.04)
dst = cv.dilate(dst, None)
_, thresh1 = cv.threshold(dst, threshold_params[0] * dst.max(), 255, 0)
_, thresh2 = cv.threshold(dst, threshold_params[1] * dst.max(), 255, 0)
_, thresh3 = cv.threshold(dst, threshold_params[2] * dst.max(), 255, 0)

plt.suptitle("Task #1")
plt.subplot(1, 4, 1)
set_image(img_gray, "Source image")
plt.subplot(1, 4, 2)
set_image(thresh1, "Threshold=0.01%")
plt.subplot(1, 4, 3)
set_image(thresh2, "Threshold=0.05%")
plt.subplot(1, 4, 4)
set_image(thresh3, "Threshold=0.1%")
plt.tight_layout()
plt.show()

# ========================= Task #2 Haar face and eyes detection ======================== #

img = cv.imread("input_imgs/lena.jpg")

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_face = img.copy()
img_eyes = img.copy()

faces = face_cascade.detectMultiScale(img_gray, 1.2, 3)
for (x, y, w, h) in faces:
    cv.rectangle(img_face, (x, y), (x+w, y+h), (0, 255, 0), 5)

    face_roi = img_gray[y:y+h, x:x+w]
    eyes = eyes_cascade.detectMultiScale(face_roi, 1.2, 3)
    for (x2, y2, w2, h2) in eyes:
        cv.rectangle(img_eyes, (x + x2, y + y2), (x + x2 + w2, y + y2 + h2), (0, 255, 0), 5)

plt.suptitle("Task #2")
plt.subplot(1, 3, 1)
set_image(img, "Source image")
plt.subplot(1, 3, 2)
set_image(img_face, "Face detection")
plt.subplot(1, 3, 3)
set_image(img_eyes, "Eyes detection")
plt.tight_layout()
plt.show()

# ========================= Task #3 Haar video face and eye detection ======================== #

vid = cv.VideoCapture("input_vids/Jalinga_360.mp4")

target_time_codes = [9, 13, 28, 36, 43, 53, 65, 68, 78] # in seconds

frame_width     = int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height    = int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))
fps             = int(vid.get(cv.CAP_PROP_FPS))
num_frames      = int(vid.get(cv.CAP_PROP_FRAME_COUNT))

target_frames   = [time_code * fps for time_code in target_time_codes]
result_frames   = []

print(f"frame width: {frame_width}")
print(f"frame height: {frame_height}")
print(f"frame FPS: {fps}")
print(f"frames number: {num_frames}")

fourcc  = cv.VideoWriter_fourcc(*'mp4v')
out     = cv.VideoWriter('output_vids/Jalinga_360.mp4', fourcc, fps, (frame_width, frame_height))

frame_num = 0
while True:
    ret, frame = vid.read()

    if not ret:
        break

    out.write(frame)

    # apply detection to key frames
    frame_num += 1
    if frame_num in target_frames:
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(frame_gray, 1.2, 3)
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

        result_frames.append(frame)

plt.suptitle("Task #3")
for i in range(9):
    plt.subplot(3, 3, i + 1)
    set_image(result_frames[i], f"Recognition #{i + 1}")
plt.tight_layout()
plt.show()