# Blind Navigation System - AI Assistive Navigation Model with Real-Time Obstacle Detection

## 🚀 Overview
The **Blind Navigation System** is an AI-powered assistive model designed to help visually impaired individuals navigate their surroundings safely. Using **Object Detection, NLP, and Computer Vision**, the system detects obstacles in real time and provides voice-based feedback for navigation.

## 🛠 Features
✅ **Real-time Object Detection** using YOLOv5 & OpenCV  
✅ **Speech Recognition & Text-to-Speech** for voice-based interaction  
✅ **GPS & Geolocation-based Navigation**  
✅ **Deep Learning & NLP-powered assistance**  
✅ **Portable & Cost-Effective AI Solution**  

## ⚙️ How the Model Works  

### **1️⃣ Capturing the Environment**  
- The system uses a **camera** to continuously capture the surroundings.  
- The live video feed is processed in real-time using **OpenCV**.  

### **2️⃣ Object Detection & Recognition**  
- The captured frames are passed through the **YOLOv5 object detection model**.  
- The model detects obstacles (e.g., walls, people, vehicles, poles) and classifies them.  
- The bounding boxes and labels for detected objects are generated.  

### **3️⃣ Audio Feedback for Navigation**  
- The detected obstacles are converted into a **verbal description** using **NLP & Text-to-Speech** (`pyttsx3`).  
- The system provides real-time **voice alerts** to inform the user about obstacles.  
- If a critical obstacle is detected, the system gives **urgent warnings** (e.g., "Obstacle ahead, step left").  

### **4️⃣ GPS-Based Navigation **  
- If enabled, **Geopy** fetches the user's location and provides **GPS-based navigation**.  
- The system can suggest directions based on predefined locations or waypoints.  

### **5️⃣ User Interaction via Speech Commands**  
- The user can give voice commands using `SpeechRecognition`.  
- Commands like "Guide me to the Target Destination".  

### **6️⃣ Continuous Monitoring & Adaptive Responses**  
- The system continuously updates as the user moves.  
- It dynamically adjusts alerts based on object proximity and movement.  
- The response time is optimized for real-time usability.  

## 🏗️ Tech Stack
- **Computer Vision**: OpenCV, YOLOv5
- **Deep Learning**: PyTorch, NumPy
- **Natural Language Processing (NLP)**: SpeechRecognition, pyttsx3
- **Programming Language**: Python
- **Geolocation Services**: Geopy

## 🔧 Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/blind-navigation-system.git
cd blind-navigation-system
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the System
```bash
python blind_navigation.py
```

## 📌 Usage
- Start the script using `python blind_navigation.py`.
- The system will detect objects and provide **audio feedback**.
- If using **GPS mode**, the system will guide the user based on location.

## 📊 Results & Performance
- Achieved **high accuracy** in object detection.
- Real-time response with minimal latency.
- Successfully tested in **various environments**.

## 🎯 Future Improvements
- Integration with **Edge AI for faster processing**.
- **Mobile App Deployment** for broader accessibility.
- Addition of **more real-time navigation features**.

## 🤝 Contributing
Contributions are welcome! Feel free to submit **issues or pull requests**.
