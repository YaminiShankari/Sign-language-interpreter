# 🖐️ Sign Language Interpreter

This project uses Computer Vision and Deep Learning to recognize basic hand gestures corresponding to common sign language words — all in real time through your webcam!

It captures gesture images, trains a custom CNN (Convolutional Neural Network) model using TensorFlow, and interprets live gestures into words like “hello”, “thanks”, “yes”, and “no”.

# 📂 Project Files Overview

BACKEND FILES

1️⃣ dataset_collection.py

🎥 Purpose: Collects gesture images for each sign label.

-Opens your webcam and captures images for defined labels (hello, thanks, yes, no).   
-Stores them in a structured dataset directory.   
-Automatically creates subfolders and saves around 35 images per label.   

🧠 Tip: Keep consistent lighting and background while recording your gestures.

2️⃣ labelImg.exe

🖊️ Purpose: Annotate gesture images for model training.

-After capturing your gesture images using dataset_collection.py, use LabelImg to draw bounding boxes around your hand and assign the correct label (like hello, thanks, yes, no).   
-This generates .xml files in Pascal VOC format for each image.   

📍 Steps to use:

Open labelImg.exe   
Load your captured image folder   
Draw a box around your hand region   
Assign the appropriate label name    
Save → generates image_name.xml   

⚡ Why it matters:
These XML annotations are crucial for linking each image to its correct class during training — your train.py reads them to pair the image data with its label.

3️⃣ train.py

🧩 Purpose: Trains a CNN model for gesture classification.

-Loads gesture images and corresponding XML annotation files.   
-Preprocesses images (resizing, normalization, one-hot encoding).   
-Builds a 3-layer CNN model with ReLU activations and softmax output.   
-Trains and validates the model using an 80/20 split.   
-Saves the trained model as sign_language_model.keras.   

⚙️ Model Architecture Overview:

Conv2D → MaxPooling2D (x3 layers)   
Flatten → Dense (128 neurons)   
Output Layer: 4 neurons (softmax for 4 gesture classes)   

4️⃣ final.py

👁️ Purpose: Real-time gesture recognition and prediction.

-Loads the trained model.   
-Detects your hand using HSV color filtering (skin segmentation).   
-Extracts the hand region, preprocesses it, and predicts the gesture.   
-Displays real-time predictions with bounding boxes and labels.   

5️⃣ server.py

🌐 Purpose: Serves the backend API for the frontend.

-Runs a Flask server with CORS enabled.   
-Accepts base64-encoded images from the frontend.   
-Returns predicted gesture and confidence.   

FRONTEND FILES

The frontend is built with React, using Webcam for live capture and Axios to communicate with the Flask backend.

1️⃣ App.jsx

🎨 Purpose: Handles the user interface and live webcam feed.

-Switches between home page and interpreter page.   
-Captures webcam frames every second and sends to backend API.   
-Displays predicted gesture and confidence in real-time.   
-Includes animations via framer-motion and responsive design with Tailwind CSS.   

2️⃣ Dependencies

Ensure these packages are installed for the frontend:   
npm install react react-dom react-scripts axios react-webcam framer-motion tailwindcss

3️⃣ Starting the Frontend   

cd frontend   
npm install   
npm run dev   

# 💡 Future Enhancements

-Add more gestures (like sorry, please)   
-Integrate with a voice output system   
-Improve accuracy with MediaPipe hand landmarks   

# 🏁 Results

✅ Accurate real-time detection   
✅ Smooth performance with webcam feed   
✅ Easy dataset expansion and retraining   

# ✨ Credits

Developer: Yamini Shankari AJ 👩‍💻
Tech Stack: Python, OpenCV, TensorFlow, Keras, React, Tailwind CSS
“Breaking barriers through gestures — one sign at a time.” 🌍
