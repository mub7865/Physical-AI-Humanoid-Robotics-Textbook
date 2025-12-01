---
sidebar_label: 'Hardware Requirements'
---
# Chapter 8: Hardware Requirements – Building the Physical AI Lab 🛠️

## The Cost of Reality

Physical AI is technically demanding. Unlike web development where a simple laptop suffices, Robotics sits at the intersection of three heavy computational loads:
1.  [cite_start]**Physics Simulation** (Isaac Sim / Gazebo) [cite: 119]
2.  [cite_start]**Visual Perception** (SLAM / Computer Vision) [cite: 119]
3.  [cite_start]**Generative AI** (LLMs / VLA Models) [cite: 119]

To run these simultaneously, you need power. Because the capstone involves a "Simulated Humanoid," the primary investment must be in **High-Performance Workstations**. [cite_start]However, to fulfill the "Physical AI" promise, you also need **Edge Computing Kits** (brains without bodies) or specific robot hardware. [cite: 120-121]

---

## 1. The "Digital Twin" Workstation (Required) 🖥️

This is the most critical component. We use **NVIDIA Isaac Sim**, which is an Omniverse application. It requires **RTX (Ray Tracing)** capabilities.

[cite_start]**⚠️ Warning:** Standard laptops (MacBooks or non-RTX Windows machines) **will not work**. [cite: 124]

| Component | Recommendation | Why? |
| :--- | :--- | :--- |
| **GPU** | **NVIDIA RTX 4070 Ti (12GB)** or higher. | **The Bottleneck.** High VRAM is needed to load USD assets and run VLA models. [cite_start]Ideal: RTX 3090/4090 (24GB) for smoother Sim-to-Real training. [cite: 125-127] |
| **CPU** | Intel Core i7 (13th Gen+) or AMD Ryzen 9. | [cite_start]Physics calculations (Rigid Body Dynamics) in Gazebo/Isaac are CPU-intensive. [cite: 128-129] |
| **RAM** | **64 GB DDR5** (32 GB Minimum). | Complex scene rendering consumes massive memory. [cite_start]32GB will crash during complex scenes. [cite: 130] |
| **OS** | **Ubuntu 22.04 LTS**. | ROS 2 (Humble/Iron) is native to Linux. [cite_start]While Isaac runs on Windows, ROS 2 development is frictionless on Linux. [cite: 131-133] |

---

## 2. The "Physical AI" Edge Kit 🧠

Since a full humanoid robot is expensive ($16k+), students learn "Physical AI" by setting up the **Nervous System** on a desk. [cite_start]This kit is used for Module 3 (Isaac ROS) and Module 4 (VLA). [cite: 135-136]

### [cite_start]The Economy Student Kit (~$700) [cite: 185]

| Component | Model | Function | Price (Approx) |
| :--- | :--- | :--- | :--- |
| **The Brain** | **NVIDIA Jetson Orin Nano (8GB)** | Runs the inference stack. Students deploy ROS 2 nodes here. | ~$249 |
| **The Eyes** | **Intel RealSense D435i** | Provides RGB (Color) and Depth (Distance). Includes IMU for SLAM. | ~$349 |
| **The Ears** | **ReSpeaker USB Mic Array** | Far-field microphone for voice commands (Whisper). | ~$69 |
| **Misc** | SD Card (128GB) + Power | High-endurance storage for the OS. | ~$30 |

> **Note:** Do not buy the D435 (non-i). [cite_start]The 'i' stands for IMU (Inertial Measurement Unit), which is essential for visual navigation. [cite: 185]

---

## 3. The Robot Lab Options 🤖

For the "Physical" part of the course, you have three tiers depending on your budget.

### Option A: The "Proxy" Approach (Recommended)
Use a quadruped (dog) or a robotic arm as a proxy. The software principles transfer 90% effectively to humanoids.
* **Robot:** **Unitree Go2 Edu** (~$1,800 - $3,000).
* **Pros:** Highly durable, excellent ROS 2 support.
* [cite_start]**Cons:** Not a biped (humanoid). [cite: 146-151]

### Option B: The "Miniature Humanoid" Approach
Small, table-top humanoids.
* **Robot:** **Unitree G1** (~$16k) or **Robotis OP3** (~$12k).
* **Budget Alt:** **Hiwonder TonyPi Pro** (~$600). *Warning: These run on Raspberry Pi and cannot run Isaac ROS efficiently. [cite_start]Use only for kinematics.* [cite: 152-157]

### Option C: The "Premium" Lab
If the goal is to deploy the Capstone to a real humanoid.
* **Robot:** **Unitree G1 Humanoid**.
* [cite_start]**Why:** It is one of the few commercially available humanoids that walks dynamically and has an open SDK. [cite: 158-161]

---

## 4. Cloud-Native Lab (High OpEx Alternative) ☁️

If you cannot afford an RTX workstation, you can rent one in the cloud ("The Ether Lab").

* [cite_start]**Instance:** AWS **g5.2xlarge** (A10G GPU, 24GB VRAM). [cite: 170]
* [cite_start]**Software:** NVIDIA Isaac Sim on Omniverse Cloud. [cite: 171]
* **Cost:** ~$1.50/hour. [cite_start]Approx **$205 per quarter** (for 120 hours). [cite: 173-176]

### The Latency Trap ⚠️
Simulating in the cloud works well, but **controlling** a real robot from the cloud is dangerous due to latency.
[cite_start]**Solution:** Train in the Cloud -> Download Model -> Flash to Local Jetson Kit. [cite: 186-188]

---

## Summary of Architecture

[cite_start]To teach this successfully, your lab infrastructure should look like this: [cite: 164]

| Component | Hardware | Function |
| :--- | :--- | :--- |
| **Sim Rig** | PC with RTX 4080 + Ubuntu | Runs Isaac Sim, Gazebo, Unity. |
| **Edge Brain** | Jetson Orin Nano | Runs the "Inference" stack. |
| **Sensors** | RealSense + Lidar | Feeds real-world data to AI. |
| **Actuator** | Unitree Go2 or G1 | Receives motor commands. |

### Ready to Build?
Acquire your hardware, set up your Ubuntu machine, and let's begin the journey into Physical AI.