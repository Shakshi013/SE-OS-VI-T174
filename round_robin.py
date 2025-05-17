import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0
        self.timeline = []

def round_robin(processes, quantum):
    # (same code as before)
    # ... [keep your round_robin code unchanged] ...
    time = 0
    queue = []
    completed = 0
    n = len(processes)
    arrival_index = 0
    processes.sort(key=lambda x: x.arrival)

    timeline = []
    log = []

    while completed < n:
        while arrival_index < n and processes[arrival_index].arrival <= time:
            log.append(f"Time {time}: Process P{processes[arrival_index].pid} arrived and added to queue.")
            queue.append(processes[arrival_index])
            arrival_index += 1

        if not queue:
            timeline.append((time, None, "CPU Idle (No process available)"))
            time += 1
            continue

        curr = queue.pop(0)
        exec_time = min(curr.remaining, quantum)
        start = time
        end = time + exec_time
        curr.timeline.append((start, end))
        curr.remaining -= exec_time

        for t in range(start, end):
            explanation = f"At time {start}: P{curr.pid} executes for {exec_time} units (Remaining: {curr.remaining})"
            timeline.append((t, curr.pid, explanation))

        time = end

        while arrival_index < n and processes[arrival_index].arrival <= time:
            log.append(f"Time {time}: Process P{processes[arrival_index].pid} arrived and added to queue.")
            queue.append(processes[arrival_index])
            arrival_index += 1

        if curr.remaining > 0:
            queue.append(curr)
        else:
            curr.completion = time
            curr.turnaround = curr.completion - curr.arrival
            curr.waiting = curr.turnaround - curr.burst
            completed += 1

    return processes, timeline, log

def visualize_timeline(timeline):
    # (same as before)
    fig, ax = plt.subplots(figsize=(16, 3.5))
    ax.set_xlim(0, len(timeline))
    ax.set_ylim(-0.5, 1.5)
    ax.axis('off')
    explanation_box = ax.text(0, 1.2, "", fontsize=12, ha='left', wrap=True)

    def animate(i):
        if i >= len(timeline): return
        time, pid, explanation = timeline[i]
        color = "#cccccc" if pid is None else f"C{pid % 10}"
        rect = patches.Rectangle((time, 0), 1, 1, facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        label = "Idle" if pid is None else f"P{pid}"
        ax.text(time + 0.5, 0.5, label, ha='center', va='center', fontsize=12, fontweight='bold', color='black')
        ax.text(time, -0.3, f"{time}", ha='center', fontsize=9)
        explanation_box.set_text(explanation)

    ani = animation.FuncAnimation(fig, animate, frames=len(timeline), interval=600, repeat=False)
    plt.title("Round Robin Gantt Chart", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.show()

def main():
    root = tk.Tk()
    root.title("Round Robin Scheduler")
    root.geometry("750x600")
    tk.Label(root, text="Round Robin Scheduling Simulator", font=('Helvetica', 16, 'bold')).pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    entry_num = tk.Entry(input_frame, width=30)
    entry_arrival = tk.Entry(input_frame, width=30)
    entry_burst = tk.Entry(input_frame, width=30)
    entry_quantum = tk.Entry(input_frame, width=30)

    labels = ["Number of Processes:", "Arrival Times (space separated):", "Burst Times (space separated):", "Time Quantum:"]
    entries = [entry_num, entry_arrival, entry_burst, entry_quantum]

    for i in range(4):
        tk.Label(input_frame, text=labels[i], font=('Arial', 11)).grid(row=i, column=0, sticky='e', padx=5, pady=5)
        entries[i].grid(row=i, column=1, padx=5, pady=5)

    table_frame = tk.Frame(root)
    table_frame.pack(pady=10)

    label_avg = tk.Label(root, text="", font=('Arial', 12, 'bold'))
    label_avg.pack(pady=5)

    def run_simulation():
        try:
            num_processes = int(entry_num.get())
            arrival_times = list(map(int, entry_arrival.get().split()))
            burst_times = list(map(int, entry_burst.get().split()))
            quantum = int(entry_quantum.get())

            if not (len(arrival_times) == len(burst_times) == num_processes):
                messagebox.showerror("Input Error", "Number of inputs doesn't match number of processes")
                return

            processes = [Process(i + 1, arrival_times[i], burst_times[i]) for i in range(num_processes)]
            scheduled, timeline, log = round_robin(processes, quantum)

            for widget in table_frame.winfo_children():
                widget.destroy()

            headers = ["PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"]
            for col, header in enumerate(headers):
                tk.Label(table_frame, text=header, font=('Arial', 11, 'bold')).grid(row=0, column=col)

            total_tat = 0
            total_wt = 0
            for i, p in enumerate(scheduled):
                values = [p.pid, p.arrival, p.burst, p.completion, p.turnaround, p.waiting]
                for j, val in enumerate(values):
                    tk.Label(table_frame, text=val, font=('Arial', 10)).grid(row=i + 1, column=j)
                total_tat += p.turnaround
                total_wt += p.waiting

            avg_tat = total_tat / num_processes
            avg_wt = total_wt / num_processes
            label_avg.config(text=f"Average Turnaround Time: {avg_tat:.2f} | Average Waiting Time: {avg_wt:.2f}")

            visualize_timeline(timeline)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")

    tk.Button(root, text="Run Simulation", font=('Arial', 12, 'bold'), bg='lightblue', command=run_simulation).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
