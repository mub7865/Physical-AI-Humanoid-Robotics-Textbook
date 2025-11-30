# Weekly Breakdown: Weeks 6-7 – Building the Digital Twin 🗓️

## Overview

Over the next two weeks, we will leave the abstract world of code and enter the visual world of simulation. You will build your robot's **Digital Twin**—a clone that lives inside the computer.

By the end of Week 7, you will have a simulated environment where your robot can move, see, and interact with physics, all without risking expensive hardware.

---

## 📅 Week 6: The Physics Lab (Gazebo)

**Goal:** Master Rigid Body Dynamics and Sensor Simulation.

We start with the industry standard for robotic simulation. It may not look pretty, but its physics are rock solid.

* **Setting up the World:** Learn to create `.world` files in Gazebo. Add a sun, a ground plane, and obstacles (cubes, cylinders).
* **Spawning the Robot:** Take the URDF you wrote in Module 1 and "spawn" it into the Gazebo world.
* **Adding Sensors:** Attach a virtual **LiDAR** and a **Depth Camera** to your robot.
    * *Activity:* Visualize the laser scan lines in RViz while the robot is in Gazebo.
* **Controlling the Robot:** Write a Python node that sends velocity commands (`cmd_vel`) to the simulated robot and watch it move.

**Key Deliverable:** A Gazebo simulation where a mobile robot can be driven around using your keyboard.

---

## 📅 Week 7: The Art Studio (Unity)

**Goal:** High-Fidelity Rendering and Human Interaction.

Now we upgrade the visuals. We will move our robot from the "Lab" to the "Real World" (virtually).

* **Unity for Robotics:** Setting up the Unity Editor with the URDF Importer package.
* **Importing Assets:** Bringing your robot into a photorealistic Unity scene (e.g., a furnished living room or a warehouse).
* **The ROS-TCP Connector:** Establishing a bridge between ROS 2 (Linux) and Unity (Windows/Linux).
    * *Challenge:* Sending motor commands from ROS 2 -> Unity.
    * *Challenge:* Sending camera images from Unity -> ROS 2.
* **Simulating Humans:** Adding a human avatar that walks around the scene to test obstacle avoidance.

**Key Deliverable:** A Unity scene where your robot navigates a realistic environment, streaming camera data back to ROS 2.

---

## 🏆 Assessment: Gazebo Simulation Implementation

At the end of these two weeks, you will be assessed on your ability to create a functional simulation.

**The Project:**
You must submit a ROS 2 Package (`my_bot_gazebo`) containing:
1.  **URDF/Xacro:** A description of a 4-wheeled robot or a simple arm.
2.  **World File:** A Gazebo environment with at least 3 obstacles.
3.  **Launch File:** A script that launches Gazebo, spawns the robot, and starts Rviz automatically.

### Ready to Enter the Simulation?
Let's fire up Gazebo and defy gravity.