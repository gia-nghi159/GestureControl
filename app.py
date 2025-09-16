import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
import numpy as np
from PIL import Image
import time
import pyautogui
from collections import deque 

# configurations
MODEL_PATH = "gesture_best.pth" 
NUM_CLASSES = 4
CLASS_NAMES = ['fist', 'like', 'no_gesture', 'palm']
ACTION_COOLDOWN = 2.0  

HISTORY_LENGTH = 15 # number of recent frames to consider
CONFIRMATION_THRESHOLD = 12 # how many frames must be the same to confirm a gesture

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Using device:", device)

model = models.mobilenet_v2(weights=None)
num_ftrs = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_ftrs, NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=False))
model.to(device)
model.eval()

data_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

last_action_time = 0

prediction_history = deque(maxlen=HISTORY_LENGTH)

print("Starting gesture recognition. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    input_tensor = data_transforms(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)
        _, preds = torch.max(outputs, 1)
        raw_prediction = CLASS_NAMES[preds.item()]
    
    prediction_history.append(raw_prediction)
    # determine the most common prediction in the recent history
    if len(prediction_history) == HISTORY_LENGTH:
        most_common_prediction = max(set(prediction_history), key=list(prediction_history).count)
        # check if this prediction is consistent enough
        if list(prediction_history).count(most_common_prediction) >= CONFIRMATION_THRESHOLD:
            confirmed_gesture = most_common_prediction
        else:
            confirmed_gesture = "..." 
        confirmed_gesture = "..." 

    current_time = time.time()
    action_text = ""
    
    if current_time - last_action_time > ACTION_COOLDOWN:
        if confirmed_gesture == 'palm':
            pyautogui.press('space')
            action_text = "ACTION: Play/Pause"
            last_action_time = current_time
        
        elif confirmed_gesture == 'like':
            pyautogui.press('volumeup')
            action_text = "ACTION: Volume Up"
            last_action_time = current_time
        
        elif confirmed_gesture == 'fist':
            pyautogui.press('volumedown')
            action_text = "ACTION: Volume Down"
            last_action_time = current_time

    # display the confirmed gesture
    cv2.putText(frame, f"Gesture: {confirmed_gesture}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    if action_text:
        cv2.putText(frame, action_text, (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    
    cv2.imshow('Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Exiting...")
cap.release()
cv2.destroyAllWindows()