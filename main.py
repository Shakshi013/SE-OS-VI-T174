import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import webbrowser

# Dictionary for linking algorithm display names to filenames
ALGORITHMS = {
    "FCFS (First Come First Serve)": "fcfs_dynamic",
    "SJF (Shortest Job First)": "sjf",
    "SRTF (Shortest Remaining Time First)": "srtf",
    "Round Robin": "round_robin",
    "Priority (Non-Preemptive)": "nonpremtive_prioority",
    "Priority (Preemptive)": "priority_preemptive",
    "Multilevel Queue": "multilevel",
    "Multilevel Feedback Queue": "multilevel_feedback_queue",
}

# Definitions (term: explanation)
DEFINITIONS = {
    "Arrival Time": "The time at which a process enters the ready queue.",
    "Burst Time": "The total time required by a process for execution on the CPU.",
    "Turnaround Time": "The total time taken from arrival to completion of a process.",
    "Waiting Time": "The time a process spends waiting in the ready queue.",
    "Preemptive Scheduling": "Processes can be interrupted and moved out of CPU.",
    "Non-Preemptive Scheduling": "Once a process gets the CPU, it cannot be removed.",
    "Quantum": "A fixed time slice given to each process in Round Robin scheduling.",
    "Queue": "A level in multilevel or MLFQ scheduler where processes are scheduled.",
}

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Visualizer")
        self.root.geometry("600x400")
        self.root.configure(bg="white")

        self.create_main_page()

    def create_main_page(self):
        title = tk.Label(self.root, text="CPU Scheduling Algorithms", font=("Helvetica", 18, "bold"), bg="white")
        title.pack(pady=20)

        self.selected_algo = tk.StringVar()
        algo_dropdown = ttk.Combobox(self.root, textvariable=self.selected_algo, state="readonly", width=50)
        algo_dropdown['values'] = list(ALGORITHMS.keys())
        algo_dropdown.pack(pady=10)
        algo_dropdown.set("Select an algorithm to visualize")

        tk.Button(self.root, text="Start Simulation", command=self.run_selected_algorithm, width=25, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Label(self.root, text="Definitions", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
        defs_frame = tk.Frame(self.root, bg="white")
        defs_frame.pack()

        for term in DEFINITIONS:
            btn = tk.Button(defs_frame, text=term, font=("Arial", 10), bg="#e0e0e0", command=lambda t=term: self.open_definition(t))
            btn.pack(pady=2, fill='x', padx=50)

    def open_definition(self, term):
        win = tk.Toplevel(self.root)
        win.title(term)
        win.geometry("400x200")
        tk.Label(win, text=term, font=("Helvetica", 14, "bold")).pack(pady=10)
        tk.Label(win, text=DEFINITIONS[term], wraplength=350, font=("Arial", 12)).pack(padx=10)

    def run_selected_algorithm(self):
        algo_name = self.selected_algo.get()
        if algo_name not in ALGORITHMS:
            messagebox.showerror("Error", "Please select a valid algorithm.")
            return

        module_name = ALGORITHMS[algo_name]
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'main'):
                module.main()  # assumes your script has a main() method to launch GUI
            else:
                messagebox.showerror("Error", f"The module '{module_name}' does not have a 'main()' function.")
        except ModuleNotFoundError:
            messagebox.showerror("File Not Found", f"The file '{module_name}.py' was not found in the directory.")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
