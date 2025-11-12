import os
import cv2
import xmltodict
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

image_dir = "imgs"
xml_dir = "xml" 

IMG_SIZE = 128
NUM_CLASSES = 4

def parse_xml(xml_file):
    with open(xml_file, 'r') as f:
        data = xmltodict.parse(f.read())
        label = data['annotation']['object']['name']
        return label

def load_data():
    images = []
    labels = []
    label_map = {'hello': 0, 'thanks': 1, 'yes': 2, 'no': 3} 

    for file_name in os.listdir(image_dir):
        if file_name.endswith('.jpg'):
            img_path = os.path.join(image_dir, file_name)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img_to_array(img)
            
            xml_file = file_name.replace('.jpg', '.xml')
            xml_path = os.path.join(xml_dir, xml_file)
            
            if os.path.exists(xml_path):
                label = parse_xml(xml_path)
                images.append(img)
                labels.append(label_map[label])
    
    return np.array(images), np.array(labels)

X, y = load_data()

X = X / 255.0
y = to_categorical(y, NUM_CLASSES)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def create_model():
    model = Sequential()
    model.add(Input(shape=(IMG_SIZE, IMG_SIZE, 3)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = create_model()
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

model.save('sign_language_model.keras')

loaded_model = load_model('sign_language_model.keras')

loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

loss, acc = loaded_model.evaluate(X_test, y_test)
print(f"Test accuracy: {acc * 100:.2f}%")