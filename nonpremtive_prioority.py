import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Patch

class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0
        self.timeline = []

def priority_non_preemptive(processes):
    time = 0
    completed = 0
    n = len(processes)
    log = []
    ready_queue = []
    timeline = []

    processes.sort(key=lambda p: p.arrival)

    while completed < n:
        for p in processes:
            if p.arrival <= time and p.completion == 0 and p not in ready_queue:
                ready_queue.append(p)

        ready_queue = [p for p in ready_queue if p.completion == 0]

        if ready_queue:
            ready_queue.sort(key=lambda p: (p.priority, p.arrival))
            current = ready_queue.pop(0)

            start = time
            end = time + current.burst
            timeline.append((current.pid, start, end))
            current.timeline.append((start, end))
            time = end

            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst
            completed += 1
        else:
            upcoming = [p.arrival for p in processes if p.completion == 0]
            if upcoming:
                time = min(upcoming)

    return processes, timeline

def show_gantt_chart(processes, timeline):
    fig, ax = plt.subplots(figsize=(12, 3.5))
    color_map = ['#5DADE2', '#58D68D', '#F4D03F', '#E59866', '#AF7AC5', '#85C1E9', '#F1948A']

    ax.set_xlim(0, max(e for _, _, e in timeline) + 1)
    ax.set_ylim(-1, 2)
    ax.set_title("Priority Non-Preemptive Scheduling - Gantt Chart")
    ax.set_xlabel("Time")
    ax.set_yticks([])

    legend_patches = [Patch(color=color_map[p.pid % len(color_map)], label=f'P{p.pid}') for p in processes]
    ax.legend(handles=legend_patches, title='Processes', bbox_to_anchor=(1.01, 1), loc='upper left')

    for pid, start, end in timeline:
        color = color_map[pid % len(color_map)]
        ax.barh(0, end - start, left=start, height=0.5, color=color, edgecolor='black')
        ax.text((start + end) / 2, 0, f"P{pid}", va='center', ha='center', fontsize=10)
        ax.text(start, -0.4, f"{start}", fontsize=8, ha='center')
    ax.text(timeline[-1][2], -0.4, f"{timeline[-1][2]}", fontsize=8, ha='center')

    plt.tight_layout()
    plt.show()

class PrioritySchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Priority Non-Preemptive Scheduling")
        self.root.geometry("600x450")

        self.frame_num = tk.Frame(root, pady=20)
        self.frame_num.pack()

        tk.Label(self.frame_num, text="Enter number of processes:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.num_entry = tk.Entry(self.frame_num, width=5, font=("Arial", 12))
        self.num_entry.pack(side=tk.LEFT, padx=10)

        self.btn_next = tk.Button(self.frame_num, text="Next", font=("Arial", 12), command=self.get_num_processes)
        self.btn_next.pack(side=tk.LEFT)

        self.input_frame = None
        self.result_frame = None

    def get_num_processes(self):
        try:
            self.num_processes = int(self.num_entry.get())
            if self.num_processes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for number of processes.")
            return

        self.frame_num.pack_forget()
        self.show_inputs()

    def show_inputs(self):
        self.input_frame = tk.Frame(self.root, padx=20, pady=20)
        self.input_frame.pack()

        tk.Label(self.input_frame, text=f"Enter arrival times (space separated):", font=("Arial", 12)).grid(row=0, column=0, sticky='w')
        self.arrival_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 12))
        self.arrival_entry.grid(row=1, column=0, pady=5)

        tk.Label(self.input_frame, text=f"Enter burst times (space separated):", font=("Arial", 12)).grid(row=2, column=0, sticky='w')
        self.burst_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 12))
        self.burst_entry.grid(row=3, column=0, pady=5)

        tk.Label(self.input_frame, text=f"Enter priorities (space separated, lower number = higher priority):", font=("Arial", 12), wraplength=500, justify='left').grid(row=4, column=0, sticky='w')
        self.priority_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 12))
        self.priority_entry.grid(row=5, column=0, pady=5)

        self.btn_submit = tk.Button(self.input_frame, text="Schedule", font=("Arial", 12), command=self.schedule_processes)
        self.btn_submit.grid(row=6, column=0, pady=10)

    def schedule_processes(self):
        try:
            arrival_times = list(map(int, self.arrival_entry.get().strip().split()))
            burst_times = list(map(int, self.burst_entry.get().strip().split()))
            priorities = list(map(int, self.priority_entry.get().strip().split()))
            if len(arrival_times) != self.num_processes or len(burst_times) != self.num_processes or len(priorities) != self.num_processes:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", f"Please enter exactly {self.num_processes} integers for arrival, burst, and priority times.")
            return

        self.processes = [Process(i + 1, arrival_times[i], burst_times[i], priorities[i]) for i in range(self.num_processes)]
        scheduled, timeline = priority_non_preemptive(self.processes)

        if self.result_frame:
            self.result_frame.destroy()
        self.result_frame = tk.Frame(self.root, padx=20, pady=20)
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("PID", "Arrival", "Burst", "Priority", "Completion", "Turnaround", "Waiting")
        tree = ttk.Treeview(self.result_frame, columns=columns, show="headings", height=self.num_processes)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=85)
        tree.pack(fill=tk.X)

        total_tat, total_wt = 0, 0
        for p in scheduled:
            total_tat += p.turnaround
            total_wt += p.waiting
            tree.insert("", "end", values=(p.pid, p.arrival, p.burst, p.priority, p.completion, p.turnaround, p.waiting))

        avg_tat = total_tat / self.num_processes
        avg_wt = total_wt / self.num_processes

        avg_label = tk.Label(self.result_frame, text=f"Average Turnaround Time: {avg_tat:.2f} | Average Waiting Time: {avg_wt:.2f}", font=("Arial", 12, "bold"), pady=10)
        avg_label.pack()

        self.root.after(100, lambda: show_gantt_chart(scheduled, timeline))

def main():
    root = tk.Tk()
    app = PrioritySchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()