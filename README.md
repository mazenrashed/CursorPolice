# CursorPolice

**A lightweight macOS background utility to reclaim your CPU from runaway Java processes.**

---

## 🚀 The Problem
Many AI-powered editors, like **Cursor**, occasionally launch background Java tasks (indexing, language servers, etc.) that consume excessive system resources. It isn't uncommon to see these tasks hitting **600%+ CPU usage** and draining RAM, even when the editor is idle.

## ✅ The Solution
This project is a macOS-native background utility that monitors your active processes. The moment it detects a rogue Java task initiated by the editor, it automatically terminates it, ensuring your Mac stays cool, fast, and responsive.

### Key Features
* **Automatic Monitoring:** Runs silently in the background.
* **Resource Efficient:** Negligible footprint on your own CPU/RAM.
* **Persistence:** Automatically starts when you log in to macOS.
* **Instant Action:** Kills high-drain tasks the moment they appear.

---

## 🛠 Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/project-name.git](https://github.com/yourusername/project-name.git)
cd project-name

```

### 2. Run the Installer

The installer sets up the background service and ensures it launches on system startup.

```bash
./install.sh

```

### 3. Check Status & Logs

To see the tool in action or verify which processes have been terminated, run:

```bash
./status.sh

```

---

## 📂 Project Structure

* `install.sh`: Configures the launch agent and permissions.
* `status.sh`: Displays a real-time log of the monitor's activity.
* `monitor.sh` (or your binary): The core logic that watches the process list.

## ⚠️ Disclaimer

This tool is specifically designed to kill Java tasks spawned by the editor environment that are deemed "runaway." Please ensure you do not have other critical Java-based development tasks running that you wish to keep active.

---

## 🤝 Contributing

Feel free to open an issue or submit a pull request if you have ideas for better process detection or support for other operating systems.
