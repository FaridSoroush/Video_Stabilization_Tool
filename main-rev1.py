import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import time

class VideoPlayer:
    def __init__(self, video_path):
        self.window = tk.Tk()
        self.window.title("Video Stabilization Comparison")

        self.cap = cv2.VideoCapture(video_path)
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Scale factor for the video frames
        self.scale_percent = 0.5  # Adjust this as needed

        # Set the width and height based on the scale
        self.width = int(self.cap.get(3) * self.scale_percent)
        self.height = int(self.cap.get(4) * self.scale_percent)

        self.canvas = tk.Canvas(self.window, width=self.width * 2, height=self.height)  # Adjusted to resized dimensions
        self.canvas.pack()

        self.slider = tk.Scale(self.window, from_=0, to=self.length, orient="horizontal", command=self.slider_used)
        self.slider.pack(fill="x", expand=True)

        self.play_button = tk.Button(self.window, text="Play", command=self.play_video)
        self.play_button.pack()

        self.current_frame = 0
        self.playing = False

        # Initialize these attributes before calling update_frame
        self.prev_gray = None
        self.warp_mode = cv2.MOTION_TRANSLATION
        self.warp_matrix = np.eye(2, 3, dtype=np.float32)
        self.criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000, 1e-10)

        self.photo_image_reference = None

        self.update_frame()

        self.window.mainloop()


    def play_video(self):
        self.playing = not self.playing
        if self.playing:
            self.play_button.config(text="Pause")
            self.update_frame()  # Start updating frames
        else:
            self.play_button.config(text="Play")


    def slider_used(self, value):
        self.current_frame = int(value)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        self.update_frame()

    def update_frame(self):
        start_time = time.time()  # Start timing
        print("Updating frame...")  # Debug print
        if self.playing:
            self.current_frame += 1
            self.slider.set(self.current_frame)

        ret, frame = self.cap.read()
        if not ret:
            self.playing = False
            print("Failed to capture the frame.")  # Debug print
            return

        stabilized_frame = self.apply_stabilization(frame)

        # Resize frames to fit the window if they are too large
        frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_AREA)
        stabilized_frame = cv2.resize(stabilized_frame, (self.width, self.height), interpolation=cv2.INTER_AREA)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stabilized_frame = cv2.cvtColor(stabilized_frame, cv2.COLOR_BGR2RGB)

        frame_photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        stabilized_frame_photo = ImageTk.PhotoImage(image=Image.fromarray(stabilized_frame))

        # Update the canvas with new images
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_image(0, 0, image=frame_photo, anchor=tk.NW, tags="frame_image")
        self.canvas.create_image(self.width, 0, image=stabilized_frame_photo, anchor=tk.NW, tags="stabilized_frame_image")

        # Store the photo images to prevent garbage collection
        self.photo_image_reference = (frame_photo, stabilized_frame_photo)

        elapsed_time = time.time() - start_time  # End timing
        print(f"Processed frame in {elapsed_time:.2f} seconds.")  # Print the time taken to process the frame

        if self.playing:
            self.window.after(30, self.update_frame)  # Schedule the next frame update


    def apply_stabilization(self, frame):
        # Convert to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Initialize prev_gray if it's the first frame
        if self.prev_gray is None:
            self.prev_gray = frame_gray
            return frame

        # Calculate the transformation
        (cc, self.warp_matrix) = cv2.findTransformECC(self.prev_gray, frame_gray, self.warp_matrix, self.warp_mode, self.criteria)

        # Apply the transformation
        stabilized_frame = cv2.warpAffine(frame, self.warp_matrix, (frame.shape[1], frame.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

        # Update previous frame
        self.prev_gray = frame_gray

        return stabilized_frame


video_path = '/Users/faridsoroush/Desktop/coffee.mp4'  # Update this path
VideoPlayer(video_path)
