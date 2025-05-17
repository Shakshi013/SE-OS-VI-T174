import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import Patch

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.start = None
        self.completion = None
        self.turnaround = None
        self.waiting = None

def sjf_non_preemptive(processes):
    processes.sort(key=lambda p: p.arrival)
    time = 0
    completed = 0
    n = len(processes)
    ready_queue = []
    timeline = []
    visited = [False] * n

    while completed < n:
        # Add processes to ready queue if they have arrived
        for i in range(n):
            if processes[i].arrival <= time and not visited[i] and processes[i] not in ready_queue:
                ready_queue.append(processes[i])

        if ready_queue:
            # Pick process with shortest burst time
            ready_queue.sort(key=lambda p: p.burst)
            current = ready_queue.pop(0)
            idx = current.pid - 1
            visited[idx] = True

            # If CPU idle, mark idle time
            if time < current.arrival:
                for idle in range(time, current.arrival):
                    timeline.append((idle, None, "CPU Idle (Waiting for process arrival)"))
                time = current.arrival

            current.start = time
            for t in range(current.burst):
                explanation = f"At time {time}: Process P{current.pid} executing (Burst: {current.burst})"
                timeline.append((time, current.pid, explanation))
                time += 1

            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst

            completed += 1
        else:
            # CPU Idle - no process ready
            timeline.append((time, None, "CPU Idle (No process available)"))
            time += 1

    return processes, timeline

def visualize_timeline(timeline, processes):
    fig, ax = plt.subplots(figsize=(16, 3.5))
    ax.set_xlim(0, len(timeline))
    ax.set_ylim(-0.5, 1.5)
    ax.axis('off')

    explanation_box = ax.text(0, 1.2, "", fontsize=12, ha='left', wrap=True)

    color_map = ['#5DADE2', '#58D68D', '#F4D03F', '#E59866', '#AF7AC5', '#85C1E9', '#F1948A']
    legend_patches = [Patch(color=color_map[(p.pid-1) % len(color_map)], label=f'P{p.pid}') for p in processes]
    ax.legend(handles=legend_patches, title='Processes', bbox_to_anchor=(1.01, 1), loc='upper left')

    def animate(i):
        if i >= len(timeline):
            return
        time, pid, explanation = timeline[i]
        color = "#bbbbbb" if pid is None else color_map[(pid-1) % len(color_map)]
        rect = patches.Rectangle((time, 0), 1, 1, facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        label = "Idle" if pid is None else f"P{pid}"
        ax.text(time + 0.5, 0.5, label, ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        ax.text(time, -0.2, str(time), ha='center', fontsize=9)
        explanation_box.set_text(explanation)

    ani = animation.FuncAnimation(fig, animate, frames=len(timeline), interval=600, repeat=False)
    plt.title("SJF Non-Preemptive Scheduling - Gantt Chart with Explanation", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.show()

class SJFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SJF Non-Preemptive Scheduling - Interactive GUI")
        self.root.geometry("700x500")

        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack()

        self.build_initial_inputs()

    def build_initial_inputs(self):
        tk.Label(self.main_frame, text="Enter Number of Processes:").grid(row=0, column=0, sticky='w')
        self.num_processes_entry = tk.Entry(self.main_frame)
        self.num_processes_entry.grid(row=0, column=1, pady=10)

        tk.Button(self.main_frame, text="Submit", command=self.setup_fields).grid(row=0, column=2, padx=10)

    def setup_fields(self):
        try:
            self.num = int(self.num_processes_entry.get())
            if self.num <= 0:
                raise ValueError("Enter a number greater than 0")

            for widget in self.main_frame.winfo_children()[1:]:
                widget.destroy()

            tk.Label(self.main_frame, text=f"Enter {self.num} Arrival Times (space-separated):").grid(row=1, column=0, sticky='w')
            self.arrival_entry = tk.Entry(self.main_frame, width=50)
            self.arrival_entry.grid(row=1, column=1, columnspan=2, pady=5)

            tk.Label(self.main_frame, text=f"Enter {self.num} Burst Times (space-separated):").grid(row=2, column=0, sticky='w')
            self.burst_entry = tk.Entry(self.main_frame, width=50)
            self.burst_entry.grid(row=2, column=1, columnspan=2, pady=5)

            tk.Button(self.main_frame, text="Run SJF", command=self.run_sjf).grid(row=3, column=1, pady=10)

            self.output_label = tk.Label(self.main_frame, text="", justify='left', font=("Courier", 10))
            self.output_label.grid(row=4, column=0, columnspan=3)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def run_sjf(self):
        try:
            arrival_times = list(map(int, self.arrival_entry.get().strip().split()))
            burst_times = list(map(int, self.burst_entry.get().strip().split()))

            if len(arrival_times) != self.num or len(burst_times) != self.num:
                raise ValueError("Mismatch in number of times entered.")

            processes = [Process(pid=i + 1, arrival=arrival_times[i], burst=burst_times[i]) for i in range(self.num)]
            final_processes, timeline = sjf_non_preemptive(processes)

            result = "PID | Arrival | Burst | Start | Completion | Turnaround | Waiting\n"
            result += "-" * 65 + "\n"
            total_tat = total_wt = 0
            for p in final_processes:
                total_tat += p.turnaround
                total_wt += p.waiting
                result += f"{p.pid:3} | {p.arrival:7} | {p.burst:5} | {p.start:5} | {p.completion:10} | {p.turnaround:10} | {p.waiting:7}\n"

            result += f"\nAverage Turnaround Time: {total_tat / self.num:.2f}"
            result += f"\nAverage Waiting Time   : {total_wt / self.num:.2f}"

            self.output_label.config(text=result)
            visualize_timeline(timeline, final_processes)

        except Exception as e:
            messagebox.showerror("Invalid Input", str(e))

def main():
    root = tk.Tk()
    app = SJFApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
