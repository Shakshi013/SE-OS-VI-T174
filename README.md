🖥️ OS-Based Algorithm Visualiser
This project is a comprehensive visualizer for key Operating System algorithms including CPU Scheduling, Page Replacement, Memory Management, and Disk Scheduling. It provides a clear, interactive, and animated representation of how these algorithms work, making it perfect for educational purposes and demonstrations.

🚀 Features
🔄 CPU Scheduling Algorithms: FCFS, SJF, SRTF, Priority (Preemptive & Non-Preemptive), Round Robin, Multilevel Queue, Multilevel Feedback Queue.

💾 Memory Management: First Fit, Best Fit, Worst Fit allocation visualizations.

📄 Page Replacement Algorithms: FIFO, LRU, Optimal, Second Chance.

💽 Disk Scheduling Algorithms: FCFS, SSTF, SCAN, CSCAN, LOOK, CLOOK.

📊 Real-time Gantt Chart visualizations and log explanations.

📌 Dynamic GUI with interactive inputs and animated process execution.

🧪 Supports bulk testing with .txt input/output for algorithm verification.

🔧 Core Components
cpu_scheduling
Implements different CPU scheduling algorithms.

Generates Gantt chart data and logs execution steps.

memory_management
Visualizes memory block allocation based on different fit strategies.

page_replacement
Simulates how pages are replaced in memory using classical algorithms.

disk_scheduling
Shows how disk head moves based on different disk access strategies.


                                              🛠️ Setup Instructions
    Clone the Repository
git clone https://github.com/Shakshi013/SE-OS-VI-T174.git
cd SE-OS-VI-T174


    Install Dependencies
pip install -r requirements.txt


    Run the GUI

python app.py


    
    
  🧪 How to Use
Choose the category (CPU/Page/Disk/Memory).

Enter the number of processes/blocks/requests.

Submit and watch the algorithm animate step-by-step.

View logs explaining why each step occurred.

📌 Summary
This project is a modular, extensible toolkit for visualizing key OS algorithms. Ideal for OS courses, presentations, and demos — helping you understand not just the output, but the why behind it.

