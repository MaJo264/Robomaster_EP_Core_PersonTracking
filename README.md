# 🤖 Autonomous Person Tracking — RoboMaster EP Core

Real-time person tracking and autonomous navigation on a physical robot platform,
combining YOLOv3 object detection with the RoboMaster SDK for closed-loop control.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![YOLOv3](https://img.shields.io/badge/Detection-YOLOv3-green)
![RoboMaster](https://img.shields.io/badge/Platform-RoboMaster%20EP%20Core-red)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Overview

This project implements a three-stage autonomous robotic system on the
**DJI RoboMaster EP Core** — a programmable ground robot platform. The system
combines real-time computer vision with robot control to achieve:

- Autonomous point-to-point navigation
- Dynamic obstacle detection and avoidance
- Real-time person tracking with trajectory adjustment

Built as part of an MSc in Automotive Embedded Systems (ESIGELEC, Rouen).

---

## 🎥 Demo

> Demo videos are included in the repository:
> - `VID-20240626-WA0006.mp4` — Autonomous navigation
> - `VID-20240626-WA0008.mp4` — Person tracking in action

---

## 🏗️ System Architecture
```
Camera Feed
    │
    ▼
YOLOv3 Detection ──► Bounding Box + Class
    │
    ▼
Tracking Logic ──► Target Selection + State Estimation
    │
    ▼
RoboMaster SDK ──► Motor Commands + Trajectory Adjustment
    │
    ▼
Physical Robot Response
```

---

## 🎯 Features

### 1. Autonomous Navigation (A → B)
Programs the RoboMaster EP Core to navigate from a defined start point to a
destination using the built-in motion control API and onboard sensors for
accurate positioning.

### 2. Object Detection & Avoidance
Integrates YOLOv3 to detect obstacles in the robot's camera feed in real time.
Detected object coordinates are combined with sensor distance measurements to
calculate collision-free path adjustments on the fly.

### 3. Real-Time Person Tracking
Uses YOLOv3 to detect and lock onto a target person. The robot continuously
adjusts its heading and speed based on the target's position in the frame —
maintaining a safe following distance and re-acquiring the target after
occlusions.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Object Detection | YOLOv3 |
| Robot Control | RoboMaster SDK |
| Language | Python 3.8+ |
| Environment | Anaconda |
| IDE | Visual Studio Code |

---

## 📁 Repository Structure
```
├── autonomous.py          # Point A → B navigation logic
├── objectdetection.py     # YOLOv3 obstacle detection + avoidance
├── persontracking.py      # Real-time person tracking pipeline
├── Yellowdetect.py        # Colour-based detection utility
├── import.py              # Dependency and SDK initialisation
└── VID-20240626-WA*.mp4   # Demo videos
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- Anaconda
- DJI RoboMaster EP Core (connected via Wi-Fi or USB)
- RoboMaster SDK

### Installation
```bash
# Clone the repository
git clone https://github.com/MaJo264/Robomaster_EP_Core_PersonTracking.git
cd Robomaster_EP_Core_PersonTracking

# Create and activate a virtual environment
conda create -n robomaster python=3.8
conda activate robomaster

# Install dependencies
pip install robomaster opencv-python numpy
```

### Running
```bash
# Autonomous navigation
python autonomous.py

# Object detection and avoidance
python objectdetection.py

# Person tracking
python persontracking.py
```

---

## 📊 Results

All three objectives were successfully validated on real hardware:

- ✅ Autonomous A→B navigation with sensor-based obstacle avoidance
- ✅ Real-time object detection and dynamic path adjustment using YOLOv3
- ✅ Continuous person tracking with real-time trajectory correction

---

## 🔮 Future Work

- Upgrade detection backbone to YOLOv8 for improved accuracy and speed
- Implement Kalman filtering for smoother state estimation under occlusion
- Add multi-person tracking with Re-Identification (ReID)
- Improve robustness under varying lighting conditions
- Implement SLAM-based mapping for more complex navigation scenarios

---

## 👤 Author

**Avin Joseph**
MSc Automotive Embedded Systems — ESIGELEC, Rouen
[LinkedIn](https://linkedin.com/in/avin-joseph) · [GitHub](https://github.com/MaJo264)
