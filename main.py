# pip install opencv-python
# pip install opencv-python-headless

import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Replace this path with the path to your video file
video_path = '/Users/faridsoroush/Desktop/IMG_8484.mp4'
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame
ret, prev_frame = cap.read()
if not ret:
    print("Error: No frame captured from the video.")
    cap.release()
    exit()

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Initialize the warp matrix
warp_mode = cv2.MOTION_TRANSLATION
warp_matrix = np.eye(2, 3, dtype=np.float32)

# Specify the number of iterations.
number_of_iterations = 5000

# Specify the termination criteria
termination_eps = 1e-10
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)

# Loop over the frames of the video
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit the loop if there are no frames left

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (cc, warp_matrix) = cv2.findTransformECC(prev_gray, frame_gray, warp_matrix, warp_mode, criteria)
    
    # Apply the transformation
    stabilized_frame = cv2.warpAffine(frame, warp_matrix, (frame.shape[1], frame.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    
    # Show the frames
    cv2.imshow('Original', frame)
    cv2.imshow('Stabilized', stabilized_frame)
    
    # Update the previous frame
    prev_gray = frame_gray.copy()

    # Break the loop if 'ESC' is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()



