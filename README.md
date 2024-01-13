# Video Stabilization Tool

This repository contains a Python script for video stabilization using OpenCV and a GUI for side-by-side comparison of the original and stabilized videos using Tkinter.

## Overview

The `video_stabilizer.py` script provides an easy-to-use tool for stabilizing shaky videos. It utilizes the ECC (Enhanced Correlation Coefficient) algorithm in OpenCV to align frames and correct unwanted camera movements. The result is a smoother and more professional-looking video.

Additionally, the script features a Tkinter-based GUI (`VideoPlayer` class) to compare the original and stabilized videos side by side, giving you an immediate sense of the stabilization effect.

## Features

- Video stabilization using ECC algorithm in OpenCV.
- GUI for side-by-side comparison of original and stabilized videos.
- Frame-by-frame playback control.
- Easy-to-use slider for navigating through the video.

## Requirements

- Python 3
- OpenCV
- NumPy
- Pillow (PIL)
- Tkinter

## Usage

1. Install the required libraries: pip install numpy opencv-python pillow
2. Clone this repository: git clone [URL]
3. Run the script: python video_stabilizer.py
4. The script will prompt for the input video file and the desired output file path.

## File Structure

- `video_stabilizer.py`: The main script containing all the functionality for video stabilization and the GUI.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

