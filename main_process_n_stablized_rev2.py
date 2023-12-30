import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import time

def stabilize_video(input_path, output_path):
    # Capture the input video from the given path
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Retrieve the total number of frames, frame width, and height from the video metadata
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Initialize the video writer to save the output stabilized video
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 20, (frame_width, frame_height))

    # Set up the warp mode for affine transformation and the warp matrix
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    
    # Define criteria to terminate the ECC algorithm (number of iterations or a certain accuracy threshold)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000, 1e-10)

    # Initialize previous frame's grayscale image
    prev_gray = None

    # Loop through all the frames in the video
    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the current frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # For the first frame, there is no previous frame to align to, so save as is
        if prev_gray is None:
            prev_gray = frame_gray
            out.write(frame)
            continue

        # Calculate the warp matrix which aligns the current frame to the previous frame
        (cc, warp_matrix) = cv2.findTransformECC(prev_gray, frame_gray, warp_matrix, warp_mode, criteria)

        # Apply the affine transformation to stabilize the frame
        stabilized_frame = cv2.warpAffine(frame, warp_matrix, (frame_width, frame_height), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

        # Write the stabilized frame to the output video
        out.write(stabilized_frame)

        # Update the previous frame to the current one for the next iteration
        prev_gray = frame_gray

        # Report the progress of the stabilization process
        progress = (i + 1) / total_frames * 100
        print(f"Stabilizing video: {progress:.2f}% complete", end='\r')

    # Release the video capture and writer objects
    cap.release()
    out.release()
    print("\nVideo stabilization complete and saved to", output_path)

class VideoPlayer:
    def __init__(self, original_video_path, stabilized_video_path):
        # Set up the main window using Tkinter
        self.window = tk.Tk()
        self.window.title("Video Stabilization Comparison")

        # Capture the original and stabilized videos
        self.cap_original = cv2.VideoCapture(original_video_path)
        self.cap_stabilized = cv2.VideoCapture(stabilized_video_path)

        # Calculate the length of the video for the slider
        self.length = int(self.cap_original.get(cv2.CAP_PROP_FRAME_COUNT))

        # Scale the video frames for display in the GUI
        self.scale_percent = 0.5
        self.width = int(self.cap_original.get(3) * self.scale_percent)
        self.height = int(self.cap_original.get(4) * self.scale_percent)

        # Set up the canvas to display the videos side by side
        self.canvas = tk.Canvas(self.window, width=self.width * 2, height=self.height)
        self.canvas.pack()

        # Create a slider to seek through the video
        self.slider = tk.Scale(self.window, from_=0, to=self.length, orient="horizontal", command=self.slider_used)
        self.slider.pack(fill="x", expand=True)

        # Add a play button to start and stop video playback
        self.play_button = tk.Button(self.window, text="Play", command=self.play_video)
        self.play_button.pack()

        # Initialize control variables for playback and image reference
        self.current_frame = 0
        self.playing = False
        self.photo_image_reference = None

        # Start the frame update process and the main event loop
        self.update_frame()
        self.window.mainloop()

    # Function to handle play/pause button press
    def play_video(self):
        self.playing = not self.playing
        if self.playing:
            self.play_button.config(text="Pause")
            self.update_frame()
        else:
            self.play_button.config(text="Play")

    # Function to handle slider movement
    def slider_used(self, value):
        self.current_frame = int(value)
        self.cap_original.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        self.cap_stabilized.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        self.update_frame()

    # Function to update the frame on the canvas
    def update_frame(self):
        start_time = time.time()
        if self.playing:
            self.current_frame += 1
            self.slider.set(self.current_frame)

        # Read the next frame from both the original and stabilized videos
        ret_original, frame_original = self.cap_original.read()
        ret_stabilized, frame_stabilized = self.cap_stabilized.read()
        if not ret_original or not ret_stabilized:
            self.playing = False
            return

        # Resize and convert color for display
        frame_original = cv2.resize(frame_original, (self.width, self.height), interpolation=cv2.INTER_AREA)
        frame_stabilized = cv2.resize(frame_stabilized, (self.width, self.height), interpolation=cv2.INTER_AREA)
        frame_original = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)
        frame_stabilized = cv2.cvtColor(frame_stabilized, cv2.COLOR_BGR2RGB)

        # Convert the frames to PhotoImage and update the canvas
        frame_photo = ImageTk.PhotoImage(image=Image.fromarray(frame_original))
        stabilized_frame_photo = ImageTk.PhotoImage(image=Image.fromarray(frame_stabilized))
        self.canvas.create_image(0, 0, image=frame_photo, anchor=tk.NW)
        self.canvas.create_image(self.width, 0, image=stabilized_frame_photo, anchor=tk.NW)

        # Keep a reference to the PhotoImages to prevent garbage collection
        self.photo_image_reference = (frame_photo, stabilized_frame_photo)

        elapsed_time = time.time() - start_time
        if self.playing:
            # Schedule the next frame update
            self.window.after(30, self.update_frame)

# Stabilize the video and save it
input_video_path = '/Users/faridsoroush/Desktop/coffee.mp4'  # Replace with the path to your input video
output_video_path = '/Users/faridsoroush/Desktop/coffee_stabilized.mp4'  # Replace with the desired path for the stabilized video
stabilize_video(input_video_path, output_video_path)

# Play the original and stabilized videos side by side
VideoPlayer(input_video_path, output_video_path)
