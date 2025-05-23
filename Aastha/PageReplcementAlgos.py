
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Patch

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Visual Simulator")
        self.root.geometry("1200x750")

        self.pages = []
        self.steps = []
        self.memory_states = []
        self.current_step = 0

        # Algorithm Descriptions
        self.algo_descriptions = {
            "LRU": "LRU (Least Recently Used): Replaces the page that hasn't been used for the longest time.",
            "FIFO": "FIFO (First-In-First-Out): Replaces the oldest loaded page in memory.",
            "Optimal": "Optimal: Replaces the page that will not be used for the longest period in the future.",
            "LFU": "LFU (Least Frequently Used): Replaces the page with the lowest access frequency.",
            "MFU": "MFU (Most Frequently Used): Replaces the page with the highest access frequency.",
        }
 
        # Algorithm Description Label
        self.algo_description_text = tk.StringVar()
        ttk.Label(root, textvariable=self.algo_description_text,
                  font=("Arial", 20, "italic"), foreground="blue",
                  anchor="w", wraplength=1100, justify="left").pack(fill='x', padx=10, pady=(10, 0))

        # Input Frame
        input_frame = ttk.Frame(root)
        input_frame.pack(fill='x', pady=10)

        ttk.Label(input_frame, text="Pages (space-separated):").pack(side='left', padx=20)
        self.pages_entry = ttk.Entry(input_frame, width=30)
        self.pages_entry.pack(side='left', padx=8)

        ttk.Label(input_frame, text="Frames:").pack(side='left', padx=8)
        self.frames_entry = ttk.Entry(input_frame, width=5)
        self.frames_entry.pack(side='left', padx=8)

        ttk.Label(input_frame, text="Algorithm:").pack(side='left', padx=8)
        self.algorithm_var = tk.StringVar(value="LRU")
        algo_combo = ttk.Combobox(input_frame, textvariable=self.algorithm_var,
                                  values=list(self.algo_descriptions.keys()),
                                  state="readonly", width=20)
        algo_combo.pack(side='left', padx=8)
        algo_combo.bind("<<ComboboxSelected>>", self.update_description)

        ttk.Button(input_frame, text="Run Simulation", command=self.run_simulation).pack(side='left', padx=8)

        # Step Text
        # Step Text
        self.step_text = tk.StringVar()
        self.step_label = ttk.Label(root, textvariable=self.step_text, font=("Arial", 30), anchor="w")
        self.step_label.pack(fill='x', padx=10)

# Output and Graph
        main_frame = ttk.Frame(root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        self.output_text = tk.Text(left_frame, height=20, font=("Arial", 12))
        self.output_text.pack(fill='both', expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)

       
        self.figure, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

# Next Step Button - Moved to Bottom
        self.next_button = ttk.Button(root, text="Next Step", command=self.next_step, state='disabled')
        self.next_button.pack(pady=10)


        # Set initial description
        self.update_description()

    def update_description(self, event=None):
        selected_algo = self.algorithm_var.get()
        description = self.algo_descriptions.get(selected_algo, "No description available.")
        self.algo_description_text.set(description)

    def run_simulation(self):
        try:
            pages_input = self.pages_entry.get().strip()
            frames_input = self.frames_entry.get().strip()

            if not pages_input or not frames_input:
                raise ValueError("Both pages and frames must be provided.")

            self.pages = list(map(int, pages_input.split()))
            num_frames = int(frames_input)

            if num_frames <= 0:
                raise ValueError("Number of frames must be greater than 0.")

            algorithm = self.algorithm_var.get()

            if algorithm == "LRU":
                self.steps, faults, self.memory_states = self.simulate_lru(self.pages, num_frames)
            elif algorithm == "FIFO":
                self.steps, faults, self.memory_states = self.simulate_fifo(self.pages, num_frames)
            elif algorithm == "Optimal":
                self.steps, faults, self.memory_states = self.simulate_optimal(self.pages, num_frames)
            elif algorithm == "LFU":
                self.steps, faults, self.memory_states = self.simulate_lfu(self.pages, num_frames)
            elif algorithm == "MFU":
                self.steps, faults, self.memory_states = self.simulate_mfu(self.pages, num_frames)

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Total Page Faults: {faults}\n")

            self.current_step = 0
            self.next_button.config(state='normal')  # Enable the Next Step button
            self.draw_step()  # Show the first step immediately
            self.current_step += 1


        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def next_step(self):
     if self.current_step >= len(self.memory_states):
        self.next_button.config(state='disabled')
        return
     self.draw_step()
     self.current_step += 1


    def draw_step(self):
        if not self.memory_states:
            return

        memory, page, step_type = self.memory_states[self.current_step]

        self.ax.clear()

        colors = []
        for i, val in enumerate(memory):
            if val == page and step_type == 'Fault' and i == len(memory) - 1:
                colors.append('lightcoral')
            else:
                colors.append('lightgreen')

        self.ax.barh(range(len(memory)), [1]*len(memory), color=colors, edgecolor='black', height=0.6)

        for i, val in enumerate(memory):
            self.ax.text(2, i, str(val), ha='center', va='center', fontsize=12, color='black')

        self.ax.set_yticks(range(len(memory)))
        self.ax.set_yticklabels([f'Frame {i+1}' for i in range(len(memory))])
        self.ax.set_xticks([])
        self.ax.set_xlim(0, 1)
        self.ax.set_title(f"Step {self.current_step + 1}: Page {page} ({step_type})")

        self.ax.legend(handles=[
            Patch(facecolor='lightgreen', edgecolor='black', label='Hit'),
            Patch(facecolor='lightcoral', edgecolor='black', label='Page Fault')
        ], loc='upper right')

        self.canvas.draw()

        self.step_text.set(self.steps[self.current_step])
        self.output_text.insert(tk.END, self.steps[self.current_step] + "\n")
        self.output_text.see(tk.END)

    def simulate_lru(self, pages, num_frames):
        memory = []
        faults = 0
        steps = []
        states = []
        for i, page in enumerate(pages):
            hit = page in memory
            if hit:
                memory.remove(page)
                memory.append(page)
            else:
                faults += 1
                if len(memory) < num_frames:
                    memory.append(page)
                else:
                    memory.pop(0)
                    memory.append(page)
            step_type = "Hit" if hit else "Fault"
            steps.append(f"Step {i+1} - Page: {page} -> {step_type}, Memory: {memory}")
            states.append((memory.copy(), page, step_type))
        return steps, faults, states

    def simulate_fifo(self, pages, num_frames):
        memory = []
        pointer = 0
        faults = 0
        steps = []
        states = []
        for i, page in enumerate(pages):
            hit = page in memory
            if not hit:
                faults += 1
                if len(memory) < num_frames:
                    memory.append(page)
                else:
                    memory[pointer] = page
                    pointer = (pointer + 1) % num_frames
            step_type = "Hit" if hit else "Fault"
            steps.append(f"Step {i+1} - Page: {page} -> {step_type}, Memory: {memory}")
            states.append((memory.copy(), page, step_type))
        return steps, faults, states

    def simulate_optimal(self, pages, num_frames):
     memory = []
     faults = 0
     steps = []
     states = []

     for i, page in enumerate(pages):
        if page in memory:
            step_type = "Hit"
        else:
            faults += 1
            step_type = "Fault"
            if len(memory) < num_frames:
                memory.append(page)
            else:
                # Predict future use of pages in memory
                future_uses = []
                for m_page in memory:
                    if m_page in pages[i+1:]:
                        future_uses.append(pages[i+1:].index(m_page))
                    else:
                        future_uses.append(float('inf'))  # Will not be used again

                # Replace the page with the farthest future use
                replace_index = future_uses.index(max(future_uses))
                memory[replace_index] = page

        steps.append(f"Step {i+1} - Page: {page} -> {step_type}, Memory: {memory}")
        states.append((memory.copy(), page, step_type))

     return steps, faults, states


    def simulate_lfu(self, pages, num_frames):
     from collections import defaultdict, deque

     memory = []
     freq = defaultdict(int)
     last_used = defaultdict(int)  # To break ties by recency if needed
     faults = 0
     steps = []
     states = []

     for i, page in enumerate(pages):
        freq[page] += 1
        last_used[page] = i
        hit = page in memory

        if not hit:
            faults += 1
            if len(memory) < num_frames:
                memory.append(page)
            else:
                # Find the least frequently used page
                min_freq = min(freq[p] for p in memory)
                candidates = [p for p in memory if freq[p] == min_freq]
                
                # Break tie using least recently used (LRU strategy)
                page_to_remove = min(candidates, key=lambda p: last_used[p])
                memory.remove(page_to_remove)
                memory.append(page)

        step_type = "Hit" if hit else "Fault"
        steps.append(f"Step {i+1} - Page: {page} -> {step_type}, Memory: {memory}")
        states.append((memory.copy(), page, step_type))

     return steps, faults, states


    def simulate_mfu(self, pages, num_frames):
     from collections import defaultdict

     memory = []
     freq = defaultdict(int)
     faults = 0
     steps = []
     states = []

     for i, page in enumerate(pages):
        freq[page] += 1
        hit = page in memory

        if not hit:
            faults += 1
            if len(memory) < num_frames:
                memory.append(page)
            else:
                # Find the most frequently used page in memory
                max_freq = -1
                page_to_remove = None
                for p in memory:
                    if freq[p] > max_freq:
                        max_freq = freq[p]
                        page_to_remove = p
                memory.remove(page_to_remove)
                memory.append(page)

        step_type = "Hit" if hit else "Fault"
        steps.append(f"Step {i+1} - Page: {page} -> {step_type}, Memory: {memory}")
        states.append((memory.copy(), page, step_type))

     return steps, faults, states


if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()

