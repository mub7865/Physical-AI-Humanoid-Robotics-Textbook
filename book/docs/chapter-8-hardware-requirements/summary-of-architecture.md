# Summary of Architecture: The Full Physical AI Stack 🏗️

## Putting It All Together

We have discussed workstations, edge kits, and robots. But how do they connect?
To teach Physical AI successfully, your lab infrastructure mimics a professional robotics deployment pipeline. It consists of three distinct layers: **Training**, **Inference**, and **Action**.

---

## The Architecture Table 📊

Here is the breakdown of the complete hardware stack required for this course:

| Component | Hardware | Function |
| :--- | :--- | :--- |
| **1. Sim Rig** | PC with RTX 4080 + Ubuntu 22.04 | **The Training Ground.** Runs Isaac Sim, Gazebo, and Unity. [cite_start]Uses high VRAM to train LLM/VLA models. [cite: 164] |
| **2. Edge Brain** | NVIDIA Jetson Orin Nano | **The Inference Engine.** Runs the deployed model. [cite_start]Students flash their ROS 2 nodes here to control the robot. [cite: 164] |
| **3. Sensors** | RealSense Camera + LiDAR | [cite_start]**The Eyes.** Connected to the Jetson to feed real-world data (Depth/RGB) to the AI. [cite: 164] |
| **4. Actuator** | Unitree Go2 or G1 (Shared) | [cite_start]**The Body.** Receives motor commands from the Jetson via Ethernet/Wi-Fi to move in the physical world. [cite: 164] |

---

## The Deployment Flow 🔄

1.  **Train in Simulation:** You build the world in Isaac Sim on your Workstation.
2.  **Transfer to Edge:** You optimize the model (using TensorRT) and copy it to the Jetson Orin.
3.  **Deploy to Reality:** The Jetson reads sensor data, processes it, and sends commands to the Robot Actuators.

### Important Note on Cloud
[cite_start]If you do not have access to RTX-enabled workstations, we must restructure the course to rely entirely on cloud-based instances (like AWS RoboMaker or NVIDIA's cloud delivery for Omniverse), though this introduces significant latency and cost complexity. [cite: 165]

### Conclusion
This architecture allows you to develop safely in the digital world and deploy confidently in the physical world.