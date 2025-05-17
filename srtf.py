import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.start = None
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0

def srtf_preemptive(processes):
    time = 0
    completed = 0
    n = len(processes)
    timeline = []
    log = []
    ready_queue = []
    current = None
    processes.sort(key=lambda p: p.arrival)

    while completed < n:
        for p in processes:
            if p.arrival == time:
                ready_queue.append(p)
                log.append(f"Time {time}: Process P{p.pid} arrived and added to queue.")

        ready_queue = sorted(ready_queue, key=lambda p: (p.remaining, p.arrival))

        if ready_queue:
            if current != ready_queue[0]:
                current = ready_queue[0]
                if current.start is None:
                    current.start = time
                explanation = f"Time {time}: P{current.pid} selected (Shortest remaining time = {current.remaining})."
                log.append(explanation)
            else:
                explanation = f"Time {time}: P{current.pid} continues executing."

            current.remaining -= 1
            timeline.append((time, current.pid, explanation))

            if current.remaining == 0:
                current.completion = time + 1
                current.turnaround = current.completion - current.arrival
                current.waiting = current.turnaround - current.burst
                ready_queue.remove(current)
                completed += 1
                current = None
        else:
            timeline.append((time, None, "CPU Idle (no process available)"))
        time += 1
    return processes, timeline, log

def visualize_dynamic_timeline(timeline):
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
        ax.text(time + 0.5, 0.5, label, ha='center', va='center', fontsize=11, fontweight='bold')
        ax.text(time, -0.3, f"{time}", ha='center', fontsize=9)
        explanation_box.set_text(explanation)

    ani = animation.FuncAnimation(fig, animate, frames=len(timeline), interval=600, repeat=False)
    plt.title("SRTF (Preemptive SJF) Gantt Chart ", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Wrap GUI setup in a main() function
def main():
    def run_scheduler():
        try:
            n = int(entry_num.get())
            arrival_times = list(map(int, entry_arrival.get().strip().split()))
            burst_times = list(map(int, entry_burst.get().strip().split()))

            if not (len(arrival_times) == len(burst_times) == n):
                messagebox.showerror("Input Error", "Mismatch in number of arrival/burst times.")
                return

            processes = [Process(i + 1, arrival_times[i], burst_times[i]) for i in range(n)]
            scheduled, timeline, log = srtf_preemptive(processes)

            for row in tree.get_children():
                tree.delete(row)

            total_tat = total_wt = 0
            for p in scheduled:
                total_tat += p.turnaround
                total_wt += p.waiting
                tree.insert('', 'end', values=(f"P{p.pid}", p.arrival, p.burst, p.start, p.completion, p.turnaround, p.waiting))

            avg_tat = total_tat / n
            avg_wt = total_wt / n

            label_avg.config(text=f"Average Turnaround Time: {avg_tat:.2f}     Average Waiting Time: {avg_wt:.2f}")
            visualize_dynamic_timeline(timeline)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")

    root = tk.Tk()
    root.title("SRTF (Preemptive SJF) Scheduler")
    root.geometry("800x600")
    root.configure(bg="#f2f2f2")

    title = tk.Label(root, text="SRTF (Preemptive SJF) Scheduler", font=("Arial", 18, "bold"), bg="#f2f2f2")
    title.pack(pady=10)

    frame_inputs = tk.Frame(root, bg="#f2f2f2")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="Number of Processes:", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_num = tk.Entry(frame_inputs, width=30)
    entry_num.grid(row=0, column=1, padx=5)

    tk.Label(frame_inputs, text="Arrival Times (space-separated):", font=("Arial", 12), bg="#f2f2f2").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_arrival = tk.Entry(frame_inputs, width=30)
    entry_arrival.grid(row=1, column=1, padx=5)

    tk.Label(frame_inputs, text="Burst Times (space-separated):", font=("Arial", 12), bg="#f2f2f2").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_burst = tk.Entry(frame_inputs, width=30)
    entry_burst.grid(row=2, column=1, padx=5)

    run_button = tk.Button(root, text="Run SRTF Scheduling", command=run_scheduler, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    run_button.pack(pady=10)

    tree_frame = tk.Frame(root)
    tree_frame.pack()

    columns = ("PID", "Arrival", "Burst", "Start", "Completion", "Turnaround", "Waiting")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=100)

    tree.pack(pady=10)

    label_avg = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#333")
    label_avg.pack(pady=10)

    root.mainloop()
if __name__ == "__main__":
    main()
