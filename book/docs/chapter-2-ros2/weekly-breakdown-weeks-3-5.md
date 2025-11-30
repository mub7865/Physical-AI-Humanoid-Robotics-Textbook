# Weekly Breakdown: Weeks 3-5 – Mastering ROS 2 Fundamentals 🗓️

## Overview

Over the next three weeks, we will transition from theory to practice. You will stop reading about robots and start programming them. We will dive deep into the **ROS 2 Architecture**, moving from basic concepts to building fully functional software packages.

By the end of Week 5, you will be able to write a Python application that can control a robot's behavior, manage its configuration, and launch complex systems with a single command.

---

## 📅 Week 3: The Architecture & Core Concepts

**Goal:** Understand the "Language" of Robots.

In the first week of this module, we focus on the vocabulary and structure of the Robot Operating System.

* [cite_start]**ROS 2 Architecture:** We will explore how ROS 2 differs from ROS 1, focusing on its real-time capabilities and decentralized nature (DDS - Data Distribution Service). [cite: 90]
* **The Computation Graph:** You will learn to visualize the network of running processes using tools like `rqt_graph`.
* [cite_start]**Nodes:** You will write your first "Hello World" Node in Python. [cite: 91]
* **Workspaces:** Setting up your `colcon` workspace (`ros2_ws`) to organize your development environment.

**Key Deliverable:** A running ROS 2 environment and your first custom Node.

---

## 📅 Week 4: Communication Patterns

**Goal:** Make Nodes Talk to Each Other.

A robot is useless if its parts can't communicate. This week is all about the data flow.

* [cite_start]**Topics (Pub/Sub):** You will build a "Talker" and a "Listener" to understand asynchronous streaming data (like video feeds or sensor readings). [cite: 91]
* [cite_start]**Services (Req/Res):** You will implement synchronous communication for immediate tasks (e.g., "Reset the simulation"). [cite: 91]
* [cite_start]**Actions (Goal-Oriented):** You will learn about long-running tasks that provide feedback, such as "Navigate to the Kitchen" (which takes time and might fail). [cite: 91]

**Key Deliverable:** A Python script where one node sends commands and another executes them.

---

## 📅 Week 5: Professional Development Tools

**Goal:** Package Your Code for Distribution.

Real-world robotics code isn't just a loose collection of scripts. It is organized, configurable, and scalable.

* [cite_start]**Building ROS 2 Packages:** You will learn to structure your code using `ros2 pkg create`, managing dependencies (`package.xml`) and installation rules (`setup.py`). [cite: 92]
* [cite_start]**Launch Files:** Instead of opening 10 terminal tabs to run 10 nodes, you will write **Python Launch Files** to start the entire robot system with one command. [cite: 93]
* [cite_start]**Parameter Management:** You will learn how to change a robot's settings (e.g., maximum speed, camera resolution) dynamically without rewriting the code. [cite: 93]

**Key Deliverable:** A custom ROS 2 Package containing launch files and configurable parameters.

---

## 🏆 Assessment: ROS 2 Package Development Project

At the end of these three weeks, you will be assessed on your ability to combine these skills.

**The Project:**
[cite_start]You will be required to develop a complete **ROS 2 Package**[cite: 114]. This package must include:
1.  A Publisher Node (Simulating a Sensor).
2.  A Subscriber Node (Processing Data).
3.  A Launch File to start both simultaneously.
4.  Parameters to adjust the data frequency.

### Ready to Code?
Let's open our terminals and start with **Week 3: The Architecture**.