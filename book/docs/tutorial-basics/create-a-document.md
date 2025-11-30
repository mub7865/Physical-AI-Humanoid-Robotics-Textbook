# Setting Up Your Development Environment 💻

## The Software Stack

You have your hardware ready. Now let's build the brain.
Robotics software is complex. It relies on a specific stack of operating systems, middleware, and simulators. If you get this wrong, nothing will work.

Follow this guide to set up your **"Digital Twin" Workstation**.

---

## 1. The Operating System: Ubuntu 22.04 LTS 🐧

**Crucial Rule:** Do not use Windows or macOS for ROS 2 development unless you are an expert.
ROS 2 (Humble/Iron) is native to Ubuntu Linux.

### Installation Steps:
1.  **Download:** Get the [Ubuntu 22.04 LTS ISO](https://ubuntu.com/download/desktop).
2.  **Create Bootable Drive:** Use **Rufus** (Windows) or **BalenaEtcher** to flash a USB stick.
3.  **Dual Boot:** Partition your hard drive to keep Windows (for gaming/Adobe) and install Ubuntu alongside it.
    * *Minimum Space:* 100 GB for Ubuntu.

> **Why not Virtual Machines (VM)?** VMs cannot access the GPU directly. Isaac Sim requires direct hardware access. You MUST boot natively.

---

## 2. Installing ROS 2 (Humble Hawksbill) 🐢

ROS 2 Humble is the current Long Term Support (LTS) version.

**The "One-Liner" Setup:**
Open your terminal (`Ctrl+Alt+T`) and run these commands (carefully):

```bash
# 1. Set locale
locale  # check for UTF-8

# 2. Add ROS 2 repository
sudo apt update && sudo apt install curl -y
sudo curl -sSL [https://raw.githubusercontent.com/ros/rosdistro/master/ros.key](https://raw.githubusercontent.com/ros/rosdistro/master/ros.key) -o /usr/share/keyrings/ros-archive-keyring.gpg

# 3. Add to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] [http://packages.ros.org/ros2/ubuntu](http://packages.ros.org/ros2/ubuntu) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 4. Install ROS 2
sudo apt update
sudo apt install ros-humble-desktop -y

# 5. Environment Setup (The Magic Command)
source /opt/ros/humble/setup.bash