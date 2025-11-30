# Appendix: ROS 2 Cheatsheet & Troubleshooting 🚑

## The Engineer's Survival Guide

Robotics is hard. You will face errors. You will forget commands.
This page is your quick-reference guide to surviving the chaotic world of ROS 2. Bookmark it. You will need it.

---

## 1. The ROS 2 Command Cheatsheet 📝

Forget the syntax? Here are the commands you will use 99% of the time.

### 🏃 Running Nodes
* **Run a node:** `ros2 run <package_name> <executable_name>`
* **List running nodes:** `ros2 node list`
* **Get node info:** `ros2 node info <node_name>`

### 📡 Managing Topics (The Nervous System)
* **List active topics:** `ros2 topic list`
* **See data flowing (Live):** `ros2 topic echo <topic_name>`
* **Check frequency (Hz):** `ros2 topic hz <topic_name>`
* **Publish manually:** `ros2 topic pub <topic_name> <msg_type> <args>`

### 📦 Building & Workspace
* **Build everything:** `colcon build`
* **Build one package:** `colcon build --packages-select <package_name>`
* **The Golden Rule:** Always source after building!
    * `source install/setup.bash`

---

## 2. Debugging Tools 🐞

When things break (and they will), don't guess. Use tools.

### A. RQT Graph (`rqt_graph`)
This visualizes your node network.
* **Command:** `rqt_graph`
* **Use:** If Node A isn't talking to Node B, check the graph. Are they connected? Is the arrow missing?

### B. ROS 2 Doctor (`ros2 doctor`)
The automated mechanic.
* **Command:** `ros2 doctor`
* **Use:** It checks your network, system version, and installed packages for warnings.

### C. RViz 2 (`rviz2`)
The robot's eye view.
* **Command:** `rviz2`
* **Use:** If your Lidar isn't showing up, add the "LaserScan" display in RViz. If it's red/error, check your "Frame ID".

---

## 3. Troubleshooting Common Errors ⚠️

### "Command 'ros2' not found"
* **Cause:** You didn't source the main ROS installation.
* **Fix:** Run `source /opt/ros/humble/setup.bash` (or add it to `~/.bashrc`).

### "Package not found" (after building)
* **Cause:** You didn't source your workspace overlay.
* **Fix:** Go to workspace root and run `source install/setup.bash`.

### "Nodes can't see each other"
* **Cause:** Network isolation.
* **Fix:** Check your `ROS_DOMAIN_ID`. Both computers/terminals must have the same ID (default is 0).
    * `export ROS_DOMAIN_ID=0`

### "Gazebo crashes on startup"
* **Cause:** Usually graphics driver issues.
* **Fix:** Ensure `nvidia-smi` shows your GPU is active. Try killing the server: `killall gzserver`.

---

## 4. Where to get help? 🆘

* **ROS Answers:** The StackOverflow for robotics.
* **Official Docs:** [docs.ros.org](https://docs.ros.org) (Always read the Humble documentation).
* **GitHub Issues:** If a specific package (like `nav2`) breaks, check their repo.

### Final Advice
**"It works on my machine"** is not a valid excuse in robotics. Always test on the hardware (Jetson) early and often.