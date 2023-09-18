import cv2
import numpy as np
import pandas as pd

# Load CSV data
csv_file = '/home/josva/kolam/output_coordinates.csv'  # Path to your CSV file
data = pd.read_csv(csv_file)

# Calculate the farthest points in x and y directions
max_x = data['x'].max()
min_x = data['x'].min()
max_y = data['y'].max()
min_y = data['y'].min()

# Set the desired screen resolution
width = 720  # Set the width to 720 pixels
height = 640  # Set the height to 640 pixels

# Initialize video capture
cap = cv2.VideoCapture(0)  # Change to the appropriate video source if needed

# Set the video capture resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
fps = 30.0

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

# Initialize circle parameters
circle_radius = 10
circle_thickness = -1  # Filled circle
circle_color = (0, 0, 255)  # Red color (BGR format)

# Initialize current row index
current_row = 0

while True:
    # Read frame from video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate the current position of the moving point
    current_x = int(data.values[current_row][0]) - min_x + 50
    current_y = int(data.values[current_row][1]) - min_y + 50

    # Draw thick blue circle for the moving point
    cv2.circle(frame, (int(current_x), int(current_y)), circle_radius + 5, (255, 0, 0), circle_thickness)

    # Show the frame
    cv2.imshow('Video Stream', frame)

    # Write the frame to the output video file
    out.write(frame)

    # Increment the current row index to move from top to bottom
    current_row += 1

    # If we reach the end of the CSV data, break the loop
    if current_row >= len(data):
        break

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    # Break the loop if 'q' key is pressed
    if key == ord('q'):
        break

# Release video capture and close windows
cap.release()
out.release()
cv2.destroyAllWindows()

