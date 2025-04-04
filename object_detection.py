import cv2
import torch
import pyttsx3
import numpy as np
from ultralytics import YOLO

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Load YOLOv5 Model
model = YOLO("yolov5m.pt")  # Medium model for better accuracy

# Predefined real-world width of objects (in cm)
KNOWN_WIDTHS = {
    "person": 40,  # Average shoulder width
    "chair": 50,
    "car": 180,
    "bottle": 7,
    "cup": 8
}

# Focal length of the camera (calibrate for your webcam)
FOCAL_LENGTH = 615  # Adjust based on testing

# Function to estimate distance based on object width in pixels
def estimate_distance(object_width_pixels, real_width_cm):
    if object_width_pixels > 0:
        return (FOCAL_LENGTH * real_width_cm) / object_width_pixels
    return -1  # Invalid distance

# Start Video Capture
cap = cv2.VideoCapture(0)

previous_objects = {}
frame_skip = 3  # Process every 3rd frame
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))  # Reduce resolution for faster processing

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Skip frames to improve speed

    results = model(frame)  # Run YOLO on the frame

    detected_objects = {}

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Get bounding box
            confidence = box.conf[0]  # Confidence score
            if confidence < 0.5:
                continue  # Skip low-confidence objects
            class_id = int(box.cls[0])  # Object class ID
            label = model.names[class_id]  # Get object name

            object_width_pixels = x2 - x1  # Width in pixels

            # Estimate distance from the camera
            real_width_cm = KNOWN_WIDTHS.get(label, 30)  # Default to 30cm if unknown
            distance = estimate_distance(object_width_pixels, real_width_cm)

            detected_objects[label] = (int(x1), int(y1), int(distance))

            # Draw Bounding Box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {distance:.1f} cm", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Object-to-Object Distance Calculation
    object_names = list(detected_objects.keys())
    for i in range(len(object_names)):
        for j in range(i + 1, len(object_names)):
            obj1, obj2 = object_names[i], object_names[j]
            x1, y1, d1 = detected_objects[obj1]
            x2, y2, d2 = detected_objects[obj2]

            pixel_distance = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))
            real_distance = (d1 + d2) / 2  # Approximate real-world distance

            text = f"{obj1} & {obj2}: {real_distance:.1f} cm apart"
            print(text)
            engine.say(text)
            engine.runAndWait()

    # Show Output
    cv2.imshow("Object Detection", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release Resources
cap.release()
cv2.destroyAllWindows()
