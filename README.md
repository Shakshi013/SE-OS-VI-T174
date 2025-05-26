🖥️ OS-Based Algorithm Visualiser
This project is a comprehensive visualizer for key Operating System algorithms, including CPU Scheduling, Page Replacement, Memory Management, and Disk Scheduling.
It provides a clear, interactive, and animated representation of how these algorithms work — perfect for educational use and classroom demonstrations.

🚀 Features
🔄 CPU Scheduling Algorithms
FCFS, SJF, SRTF, Priority (Preemptive & Non-Preemptive), Round Robin, Multilevel Queue, Multilevel Feedback Queue.

💾 Memory Management
First Fit, Best Fit, Worst Fit allocation visualizations.

📄 Page Replacement Algorithms
FIFO, LRU, Optimal, Second Chance.

💽 Disk Scheduling Algorithms
FCFS, SSTF, SCAN, CSCAN, LOOK, CLOOK.

📊 Real-time Gantt Chart Visualizations
With logs explaining why each process/step was selected.

📌 Dynamic GUI
Interactive inputs and animated execution for better understanding.

🧪 Bulk Testing Support
Input/output testing using .txt files for validation and comparison.

🔧 Core Components
cpu_scheduling/
Implements different CPU scheduling algorithms.

Generates Gantt chart data and logs for execution steps.

memory_management/
Visualizes memory block allocation based on various fit strategies.

page_replacement/
Simulates how pages are replaced in memory using classical algorithms.

disk_scheduling/
Shows how disk head moves based on different disk access algorithms.

🛠️ Setup Instructions

1. Clone the Repository
git clone https://github.com/Shakshi013/SE-OS-VI-T174.git
cd SE-OS-VI-T174

2. Install Dependencies
pip install -r requirements.txt

3. Run the GUI
python app.py

🧪 How to Use
Launch the GUI interface.

Choose a category: CPU, Page, Disk, or Memory.

Enter the number of processes/blocks/requests.

Click “Submit” and watch the animation step-by-step.

View the detailed log panel explaining every decision the algorithm makes.

📌 Summary
This project is a modular, interactive, and extensible toolkit for visualizing key Operating System algorithms.
It's ideal for:

OS practical sessions

Demos during presentations

Self-learning through animations and logs

It helps you understand not just the output, but also the why behind every algorithmic decision.
