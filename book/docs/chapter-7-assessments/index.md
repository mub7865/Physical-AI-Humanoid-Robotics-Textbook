---
sidebar_label: 'Assessments & Capstone Projects'
---
# Chapter 7: Assessments & Capstone Project 🏆

## Proving Your Skills

Welcome to the proving grounds. In the world of Physical AI, theory is useless without execution. You cannot simply "know" how a robot walks; you must write the code that *makes* it walk.

This chapter outlines the **Four Major Assessments** required to graduate from this course. These are not multiple-choice quizzes. They are **Build Projects**. You will write code, run simulations, and deploy AI models.

By completing these projects, you will build a **GitHub Portfolio** that demonstrates your ability to bridge the gap between digital AI and physical robotics.

---

## 1. Project A: The ROS 2 Package (Module 1) 📦

**Theme:** "The Nervous System"
**Goal:** Demonstrate mastery of Nodes, Topics, and Services.

### The Challenge
You must build a ROS 2 package named `my_security_robot`. This robot monitors a "door" and raises an alarm if it opens.

### Requirements:
1.  **Sensor Node (Publisher):** Write a Python node (`door_sensor.py`) that simulates a door status.
    * It publishes a boolean `True` (Open) or `False` (Closed) to the topic `/door_status` every 1 second.
    * Use `random` to randomly toggle the state.
2.  **Brain Node (Subscriber):** Write a Python node (`security_system.py`) that subscribes to `/door_status`.
    * If it receives `True`, it must print: **"ALARM! INTRUDER DETECTED!"**
    * If it receives `False`, it prints: "System Secure."
3.  **Launch File:** Create a Python launch file (`security.launch.py`) that starts both nodes simultaneously with one command.

**Grading Criteria:**
* Clean `package.xml` and `setup.py` configuration.
* Nodes communicate successfully without crashing.
* Launch file works correctly.

---

## 2. Project B: The Simulation World (Module 2) 🌍

**Theme:** "The Digital Twin"
**Goal:** Create a custom physics environment in Gazebo.

### The Challenge
You must architect a simulation environment representing a **"Mars Habitat."**

### Requirements:
1.  **World Design:** Create a `.world` file in Gazebo.
    * Ground plane: Red Martian soil (change color/texture).
    * Obstacles: At least 5 "Rocks" (Geometric shapes) and 1 "Base Station" (Building model).
2.  **The Robot:** Import a simple 4-wheeled rover (URDF) into this world.
3.  **Sensors:** Attach a **LiDAR** to the rover.
4.  **Verification:** Launch RViz and show the LiDAR's red laser lines hitting the "Rocks."

**Grading Criteria:**
* World loads without errors.
* Robot spawns correctly on the terrain (not falling through).
* LiDAR data is visible in RViz.

---

## 3. Project C: The Perception Pipeline (Module 3) 👁️

**Theme:** "The AI Brain"
**Goal:** Use NVIDIA Isaac ROS to give the robot sight.

### The Challenge
You must build a **"Visual Navigation"** system. The robot must find a specific object in a room without bumping into walls.

### Requirements:
1.  **VSLAM:** Use `isaac_ros_visual_slam` to map a room using only a camera (no LiDAR allowed).
2.  **Object Detection:** Integrate a pre-trained YOLO model using `isaac_ros_yolov8`.
    * The robot must identify a "Chair" and draw a bounding box around it.
3.  **Mapping:** Drive the robot around manually (teleop) and generate a 2D occupancy map of the room.

**Grading Criteria:**
* Map quality (Are walls straight?).
* Detection accuracy (Does it recognize the chair?).
* Use of Hardware Acceleration (GPU usage).

---

## 4. The Capstone: The Autonomous Humanoid (Module 4) 🤖🎓

**Theme:** "Vision-Language-Action"
**Goal:** The Final Exam. Integrate Voice, LLMs, and Action.

### The Challenge
You will deploy a simulated **Humanoid Robot** in a home environment (Kitchen/Living Room). The robot must perform a task based on a spoken command.

### The Scenario
User speaks: ***"I spilled some water. Please clean it up."***

### The Pipeline You Must Build:
1.  **Voice-to-Text (Whisper):**
    * Capture the audio.
    * Transcribe it to text: "I spilled some water. Please clean it up."
2.  **Reasoning (LLM Planner):**
    * Send text to GPT-4o.
    * LLM output: `["Find sponge", "Go to spill", "Wipe floor"]`.
3.  **Visual Grounding (VLM):**
    * Robot scans the room.
    * Identifies "Sponge" on the counter and "Water Spill" on the floor.
    * Returns XYZ coordinates.
4.  **Action (Nav2 + Manipulation):**
    * Robot walks to the sponge.
    * Robot grasps the sponge.
    * Robot walks to the spill and executes a wiping motion.

### Submission Requirements:
* **Video Demo:** A 90-second screen recording showing the full loop (Voice -> Action).
* **Codebase:** A link to your GitHub repository containing the ROS 2 packages and Agent logic.
* **Architecture Diagram:** A drawing explaining how your Nodes, Topics, and AI models connect.

---

## Rubric: How You Will Be Graded

| Component | Weight | Criteria |
| :--- | :--- | :--- |
| **Functionality** | 40% | Does the robot actually do what was asked? |
| **Code Quality** | 30% | Is the code modular, commented, and efficient? |
| **Integration** | 20% | Do the AI and Robot talk to each other smoothly? |
| **Creativity** | 10% | Did you add extra features (e.g., the robot tells a joke while working)? |

### Final Words
This Capstone is not just an assignment; it is a **Portfolio Piece**. If you can build this, you are ready to work at companies like Tesla, Figure, or Boston Dynamics.

**Good luck, Engineer.**