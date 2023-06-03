import cv2
import numpy as np
from tkinter import Tk
from tkinter.colorchooser import askcolor
import threading

# Initialize the camera
camera = cv2.VideoCapture(0)  # Change the value to the camera index if using multiple cameras

# Global variables for default color a and color b in BGR format
color_a = (0, 0, 0) # Black
color_b = (0, 255, 255) # Yellow

# Function to update color_a from color picker
def update_color_a():
    global color_a
    while True:
        color_a = askcolor(title="Choose Color A", parent=Tk())[0][::-1]

# Function to update color_b from color picker
def update_color_b():
    global color_b
    while True:
        color_b = askcolor(title="Choose Color B", parent=Tk())[0][::-1]

# Start the color picker threads
thread_a = threading.Thread(target=update_color_a)
thread_a.daemon = True
thread_a.start()

thread_b = threading.Thread(target=update_color_b)
thread_b.daemon = True
thread_b.start()

while True:
    # Read the current frame from the camera
    ret, frame = camera.read()

    # Convert the frame to grayscale
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    _, thresholded_frame = cv2.threshold(grayscale_frame, 100, 255, cv2.THRESH_BINARY)

    # Create a color mapping based on the thresholded image
    color_mapping = np.zeros_like(frame)
    color_mapping[thresholded_frame == 255] = color_a
    color_mapping[thresholded_frame == 0] = color_b

    # Display the resulting image
    cv2.imshow("Color Mapping", color_mapping)

    # Check for key press events
    key = cv2.waitKey(1) & 0xFF

    # Exit the loop if 'q' is pressed
    if key == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()