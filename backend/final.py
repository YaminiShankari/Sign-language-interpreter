import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('sign_language_model.h5')

label_map = {0: 'hello', 1: 'thanks', 2: 'yes', 3: 'no'}

confidence_threshold = 0.5

def preprocess_frame(frame):
    img = cv2.resize(frame, (128, 128))
    img = img.astype('float32') / 255.0 
    img = np.expand_dims(img, axis=0)
    return img

def detect_hand(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        hand_contour = max(contours, key=cv2.contourArea)
        
        if cv2.contourArea(hand_contour) > 1000:
            x, y, w, h = cv2.boundingRect(hand_contour)
            return (x, y, w, h), mask
    return None, mask

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    hand_box, mask = detect_hand(frame)
    
    if hand_box:
        x, y, w, h = hand_box
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        hand_roi = frame[y:y + h, x:x + w]
        
        processed_hand = preprocess_frame(hand_roi)
        
        predictions = model.predict(processed_hand)
        max_probability = np.max(predictions[0])
        predicted_class = np.argmax(predictions[0])
        
        if max_probability >= confidence_threshold:
            predicted_label = label_map[predicted_class]
        else:
            predicted_label = "No sign detected"
        
        cv2.putText(frame, f'Predicted: {predicted_label}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
    else:
        cv2.putText(frame, "No hand detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)
    
    cv2.imshow('Sign Language Recognition', frame)
    cv2.imshow('Hand Mask', mask) 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
