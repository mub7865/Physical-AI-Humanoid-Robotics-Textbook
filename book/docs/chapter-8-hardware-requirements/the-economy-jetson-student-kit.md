# The Economy Jetson Student Kit 🧠

## Physical AI on a Budget

While High-Performance Workstations allow us to simulate the world, to truly master **Physical AI**, we need to touch the real world. A full humanoid robot costs over $16,000, which is out of reach for most students.

However, the **"Brain"** and **"Senses"** of a humanoid robot are surprisingly affordable.

We have designed the **Economy Jetson Student Kit**. This kit replicates the entire nervous system of a $100,000 robot on your desk for approximately **$700**. [cite_start]It is best for learning ROS 2, Basic Computer Vision, and Sim-to-Real control. [cite: 183-184]

---

## 1. The Component Breakdown 🛠️

Here is exactly what you need to build your Edge AI rig.

### A. The Brain: NVIDIA Jetson Orin Nano (8GB)
* **Model:** Jetson Orin Nano Super Dev Kit.
* **Why:** This is the industry standard for Embodied AI. It delivers **40 TOPS** (Trillion Operations Per Second) of AI performance. [cite_start]It is small enough to fit on a drone but powerful enough to run modern Neural Networks. [cite: 137-139]
* [cite_start]**Price:** ~$249 (New official MSRP). [cite: 185]

### B. The Eyes: Intel RealSense D435i
* **Why:** A normal webcam is 2D. Robots need 3D. The RealSense D435i is an **RGB-D** camera. It sees color (RGB) and Distance (Depth).
* **Critical Feature:** The 'i' stands for **IMU** (Inertial Measurement Unit). This internal gyroscope allows the robot to know its orientation, which is essential for VSLAM (Visual SLAM). [cite_start]**Do not buy the D435 (non-i).** [cite: 140-141, 185]
* [cite_start]**Price:** ~$349. [cite: 185]

### C. The Ears: ReSpeaker USB Mic Array v2.0
* **Why:** For Module 4 (VLA), we need to speak to the robot. A standard microphone picks up too much motor noise. [cite_start]The ReSpeaker is a **Far-Field Microphone** designed to hear voice commands clearly from across the room. [cite: 143, 185]
* [cite_start]**Price:** ~$69. [cite: 185]

---

## 2. The Shopping List (Bill of Materials) 🧾

| Component | Model | Price (Approx.) | Notes |
| :--- | :--- | :--- | :--- |
| **The Brain** | NVIDIA Jetson Orin Nano Super Dev Kit (8GB) | **$249** | Capable of 40 TOPS. [cite_start]Ensure you get the 8GB version for running LLMs. [cite: 185] |
| **The Eyes** | Intel RealSense D435i | **$349** | Includes IMU (Essential for SLAM). |
| **The Ears** | ReSpeaker USB Mic Array v2.0 | **$69** | Far-field microphone for voice commands. |
| **Wi-Fi** | (Included in Super Dev Kit) | **$0** | The new kits come with pre-installed Wi-Fi modules. |
| **Storage** | microSD Card (128GB) | **~$20** | [cite_start]Buy a "High Endurance" card, as OS logging can wear out cheap cards. [cite: 185] |
| **Power** | Jumper Wires / Power Supply | **~$10** | Basic connectivity. |
| **TOTAL** | | **~$700** | |

---

## 3. Why this specific hardware?

You might wonder, *"Can I use a Raspberry Pi?"*
**No.**
While a Raspberry Pi is great for simple projects, it does not have a **GPU (CUDA Cores)**. Physical AI requires running deep learning models (like YOLO or VSLAM) at 30 frames per second. A Raspberry Pi would run these at 1 FPS. The Jetson Orin is purpose-built for AI workloads.

This kit will serve you from Module 3 (Perception) all the way to the Capstone Project.