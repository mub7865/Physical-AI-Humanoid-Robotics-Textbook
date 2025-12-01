# Weekly Breakdown: Weeks 11-12 – Building the Humanoid 🗓️

## Overview

We have arrived at the most challenging and exciting part of the course. Until now, we have dealt with generic robots (wheels and simple arms). Now, we tackle the **Humanoid Form**.

Building a robot that walks on two legs without falling over is one of the hardest problems in physics and control theory. Over the next two weeks, you will learn the math behind bipedal locomotion and the dexterity required for human-like manipulation.

By the end of Week 12, you will understand how to make a robot stand up, walk, and shake your hand.

---

## 📅 Week 11: The Physics of Walking (Locomotion)

**Goal:** Master Bipedal Balance and Dynamics.

Humanoids are inherently unstable. Unlike a 4-wheeled car, if you turn off a humanoid, it falls down. We need active control systems to fight gravity.

* **Kinematics & Dynamics:**
    * **Forward Kinematics:** "If I set my hip angle to 30° and knee to 45°, where is my foot?"
    * **Inverse Kinematics (IK):** "I want my foot to step *here*. What angles should my joints be?"
* **Bipedal Locomotion:**
    * **The Inverted Pendulum Model:** Simplifying a complex robot into a stick balancing on a cart.
    * **ZMP (Zero Moment Point):** The mathematical criterion for stability. If the ZMP stays within the foot's support polygon, the robot stays upright.
* **Balance Control:** Implementing PID controllers and MPC (Model Predictive Control) to adjust posture in real-time when pushed.

**Key Deliverable:** A simulation in Gazebo/Isaac where a bipedal robot maintains balance while standing on one leg.

---

## 📅 Week 12: Hands & Humans (Manipulation & HRI)

**Goal:** Dexterous Grasping and Natural Interaction.

A humanoid isn't just legs; it's hands and a face. This week focuses on interacting with the world and the people in it.

* **Manipulation & Grasping:**
    * **The Humanoid Hand:** Moving beyond simple "Open/Close" grippers to multi-fingered hands.
    * **Grasp Planning:** How to pick up a delicate egg vs. a heavy hammer. Calculating force and friction cones.
* **Human-Robot Interaction (HRI):**
    * **Social Navigation:** How to move through a crowd without being "creepy" or aggressive.
    * **Non-Verbal Cues:** Using head gaze and arm gestures to signal intent (e.g., looking at a door before walking through it).
    * **Safety:** ensuring the robot yields to humans and operates with compliant joints (softness).

**Key Deliverable:** A manipulation task where the robot identifies an object, plans a grasp, and lifts it without slipping.

---

## 🏆 Assessment: The "Pick and Place" Challenge

At the end of Module 4, you will combine locomotion and manipulation.

**The Project:**
You must deploy a simulation where a humanoid robot:
1.  **Walks** from a starting point to a table (Locomotion).
2.  **Identifies** a target object using Vision.
3.  **Grasps** the object securely (Manipulation).
4.  **Places** it in a bin.

### Ready for the Final Stretch?
Only one week remains. Next, we will add the final layer of intelligence: **Conversational AI**.