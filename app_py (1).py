# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gVFvmFpHsnMFGgBAsE-ein5kKXdK609Q
"""

from ultralytics import YOLO

# Load the pre-trained YOLO model from the .pt file (YOLOv5 or YOLOv8 supports this)
model = YOLO('/content/yolov11_baseline_model.pt')  # Load the pre-trained model from the .pt file

# Set the model to evaluation mode (necessary before inference)
model.eval()

from ultralytics import YOLO
import cv2
from google.colab.patches import cv2_imshow # Import the cv2_imshow function
import torch

device = torch.device("cpu")  # Force PyTorch to use CPU instead of GPU

# Load the model and move it to the CPU
model = YOLO('/content/yolov11_baseline_model.pt').to(device)
# Set the model to evaluation mode (necessary before inference)
model.eval()

# Load an image (replace with the correct image loading method)
image = cv2.imread('/content/4_jpeg.rf.773d5cde271979d2ad1618675bb6f933.jpg')  # Replace with your image path

# Run inference
result= model(image)

results0 = results[0]

# Now you can use the plot method on the Results object
results0.plot()  # This will plot the detections (boxes, masks, etc.) on the image


# If you want to visualize the result using the built-in plot method
boxes = results0.boxes

# If you want to manually process the bounding boxes (for custom visualization):
for box in boxes:
    # Get the bounding box coordinates and confidence score (using .xywh for [center_x, center_y, width, height])
    x_center, y_center, width, height = box.xywh[0]  # Center (x, y) and size (width, height)
    confidence = box.conf[0]  # Confidence score
    class_id = box.cls[0]  # Class ID (predicted class)

    # Convert from center coordinates to corner coordinates
    x1, y1 = int(x_center - width / 2), int(y_center - height / 2)
    x2, y2 = int(x_center + width / 2), int(y_center + height / 2)

    # Draw the bounding box on the image (Green rectangle)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Format the label with class and confidence
    label = f"Class: {int(class_id)} Conf: {confidence:.2f}"

    # Put the label above the bounding box (Blue text)
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# Display the image with bounding boxes
cv2_imshow(image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image

# Load the pre-trained YOLOv11 model from the .pt file
device = torch.device("cpu")  # Force PyTorch to use CPU instead of GPU

# Load the model and move it to the CPU
model = YOLO('/content/yolov11_baseline_model.pt').to(device)
# Define the Streamlit app
st.title("YOLOv11 Object Detection")
st.write("Upload an image to perform object detection using the YOLOv11 model")

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the uploaded file to an OpenCV image
    image = Image.open(uploaded_file)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Run inference on the uploaded image
    result = model(image)
    result0 = result[0]

    # Plot detection results on the image
    result0.plot()  # This will plot the detections (boxes, masks, etc.) on the image

    # If you want to visualize the bounding boxes manually:
    boxes = result0.boxes
    for box in boxes:
        x_center, y_center, width, height = box.xywh[0]  # Center (x, y) and size (width, height)
        confidence = box.conf[0]  # Confidence score
        class_id = box.cls[0]  # Class ID (predicted class)

        # Convert from center coordinates to corner coordinates
        x1, y1 = int(x_center - width / 2), int(y_center - height / 2)
        x2, y2 = int(x_center + width / 2), int(y_center + height / 2)

        # Draw the bounding box on the image (Green rectangle)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Format the label with class and confidence
        label = f"Class: {int(class_id)} Conf: {confidence:.2f}"

        # Put the label above the bounding box (Blue text)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Convert the image back to RGB for display
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Display the image with bounding boxes in Streamlit
    st.image(image, caption="Processed Image with Detections", use_column_width=True)

