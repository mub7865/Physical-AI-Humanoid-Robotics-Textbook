# The Robot Lab: Building Your Arena 🏟️

## Choosing Your Robot

So, you have the Brain (Jetson) and the Eyes (RealSense). Now you need the Body.
Building a robot lab is a significant investment. You have three tiers of options depending on your budget and goals.

---

## Option A: The "Proxy" Approach (Recommended for Budget) 🐕

**Best For:** Students, Hobbyists, and Software Focus.

If you can't afford a $16,000 humanoid, don't worry. The software principles (ROS 2, VSLAM, Isaac Sim) transfer **90% effectively** from a four-legged robot to a two-legged one.

* **Robot:** **Unitree Go2 Edu**.
* **Price:** ~$1,800 - $3,000.
* **Pros:**
    * **Durable:** It can fall down and get back up.
    * **Support:** Excellent ROS 2 integration.
    * **Scalable:** Affordable enough for a university to buy 10 units.
* **Cons:** It is a quadruped (4 legs), not a biped (humanoid). You can't teach it to climb a ladder like a human.

---

## Option B: The "Miniature Humanoid" Approach 🧸

**Best For:** Table-top Experiments and Kinematics.

If you specifically want to study bipedal walking but have limited space/budget.

* **Robot:** **Unitree G1** (~$16k) or **Robotis OP3** (~$12k).
* **Budget Alternative:** **Hiwonder TonyPi Pro** (~$600).
    * **⚠️ Warning:** Cheap kits like Hiwonder usually run on Raspberry Pi. They **cannot** run NVIDIA Isaac ROS efficiently. [cite_start]You should use these only for kinematics (learning how legs move) and keep the heavy AI on your Jetson kit. [cite: 156-157]

---

## Option C: The "Premium" Lab 💎

**Best For:** Research Labs, Startups, and Capstone Projects.

If the goal is to actually deploy the Capstone to a real humanoid that can perform useful tasks.

* **Robot:** **Unitree G1 Humanoid**.
* **Price:** ~$16,000+.
* **Why:** It is one of the few commercially available humanoids that can actually walk dynamically (not just shuffle) and has an SDK open enough for students to inject their own ROS 2 controllers.

---

## Summary: Which One Should You Buy?

| Budget | Recommendation | Focus |
| :--- | :--- | :--- |
| **Under $1,000** | **Jetson Kit Only** | Focus on Simulation (Isaac Sim) and deploy vision models to the Edge Kit. |
| **$3,000** | **Unitree Go2** | Best balance. You get a real, robust robot to test navigation and AI. |
| **$16,000+** | **Unitree G1** | The real deal. Only for advanced research requiring bipedal locomotion. |

### Ready to Build?
Whether you have a simulation rig or a physical lab, the principles of Physical AI remain the same. Let's start building the brain.