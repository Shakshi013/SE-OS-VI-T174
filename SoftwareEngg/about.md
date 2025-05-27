# About the Project: OS Algorithm Visualizer

This project is a unified visualizer for core Operating System algorithms. It enables users to explore various scheduling, memory, and storage algorithms both through a web interface (Flask) and standalone desktop modules (Tkinter). Each algorithm is implemented independently for flexibility, allowing both browser-based interaction and local GUI simulation.

---

os3/\
├── app.py \
├── modules/\
│   ├── cpu_scheduling.py \
│   ├── memory_management.py \
│   ├── page_replacement.py \
│   └── disk_scheduling.py \
├── templates/\
    └── index.html  \


---

### ⚙️ Algorithm Modules (Standalone + Web)

Each of the following algorithm files in `/modules/`:
- Can be **executed independently** using Tkinter for a **desktop GUI**
- Are also integrated into the web interface using Flask routes and templates

1. **CPU Scheduling (`cpu_scheduling.py`)**
   - Algorithms: FCFS, SJF, Round Robin, Priority (preemptive/non-preemptive), Multilevel Queues
   - Inputs: Arrival time, burst time, priority, time quantum
   - Outputs: Gantt Chart, turnaround & waiting times

2. **Memory Management (`memory_management.py`)**
   - Algorithms: First Fit, Best Fit, Worst Fit
   - Visualizes how processes fit into available memory blocks

3. **Page Replacement (`page_replacement.py`)**
   - Algorithms: FIFO, LRU, Optimal
   - Shows page hits, faults, and real-time frame replacement animation

4. **Disk Scheduling (`disk_scheduling.py`)**
   - Algorithms: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK
   - Calculates total seek time and animates disk head movement

---

### 🌐 Web Interface (Flask-Based)

- **`app.py`**: Central Flask application that serves the interface and routes input to algorithm modules
- **`index.html`**: Dynamic front-end for algorithm selection and input
- **`style.css` & `script.js`**: Controls layout and interactivity

---

### 🧩 Dual Execution Mode

✅ **Web Mode**: Choose and run simulations directly in a browser via Flask  
✅ **Desktop Mode**: Run any individual algorithm file as a **Tkinter application**

---

### 📝 Summary

This OS visualizer serves both as a hands-on learning tool and a modular simulation suite. Whether accessed via a modern web UI or used locally as independent Tkinter GUIs, it helps users grasp the working of key OS algorithms with visual and interactive feedback.

