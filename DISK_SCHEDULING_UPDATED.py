import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MaxNLocator
import textwrap


class DiskSchedulingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Algorithm Visualizer")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")
        
        # Algorithm documentation
        self.algo_docs = {
            "FCFS": {
                "description": "First-Come, First-Served - Services requests in the order they arrive",
                "algorithm": "1. Start from initial head position\n2. Service requests in the order they were received\n3. Calculate total head movement",
                "advantages": "• Simple to implement\n• Fair to all requests",
                "disadvantages": "• Poor performance with scattered requests\n• High seek times",
                "complexity": "Time: O(n)\nSpace: O(1)"
            },
            "SSTF": {
                "description": "Shortest Seek Time First - Services the nearest request first",
                "algorithm": "1. Start from initial head position\n2. Find request with minimum seek time\n3. Service that request\n4. Repeat until all requests are serviced",
                "advantages": "• Better performance than FCFS\n• Reduces average seek time",
                "disadvantages": "• Can cause starvation\n• Not optimal for all cases",
                "complexity": "Time: O(n^2)\nSpace: O(1)"
            },
            "SCAN": {
                "description": "Elevator Algorithm - Moves back and forth across the disk",
                "algorithm": "1. Start from initial head position\n2. Move in a direction (left/right)\n3. Service all requests along the way\n4. Reverse direction at end of disk\n5. Repeat until all requests serviced",
                "advantages": "• No starvation\n• Good for heavy loads",
                "disadvantages": "• Long wait times for some requests",
                "complexity": "Time: O(n log n)\nSpace: O(1)"
            },
            "C-SCAN": {
                "description": "Circular SCAN - Services requests in one direction only",
                "algorithm": "1. Start from initial head position\n2. Move in one direction (e.g., right)\n3. Service requests along the way\n4. Jump to start (without servicing)\n5. Repeat",
                "advantages": "• More uniform wait times\n• Better than SCAN for some workloads",
                "disadvantages": "• Wastes time returning to start",
                "complexity": "Time: O(n log n)\nSpace: O(1)"
            },
            "LOOK": {
                "description": "Improved SCAN - Only goes as far as last request",
                "algorithm": "1. Start from initial head position\n2. Move in a direction\n3. Service requests until last request\n4. Reverse direction\n5. Repeat",
                "advantages": "• More efficient than SCAN\n• Doesn't go to disk ends unnecessarily",
                "disadvantages": "• Still has some unnecessary movement",
                "complexity": "Time: O(n log n)\nSpace: O(1)"
            },
            "C-LOOK": {
                "description": "Circular LOOK - Services requests in one direction only",
                "algorithm": "1. Start from initial head position\n2. Move in one direction\n3. Service requests until last request\n4. Jump to first request in opposite end\n5. Repeat",
                "advantages": "• Most efficient of SCAN variants\n• Minimal wasted movement",
                "disadvantages": "• Slightly more complex to implement",
                "complexity": "Time: O(n log n)\nSpace: O(1)"
            }
        }

        # Main container
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel (controls and docs)
        left_panel = tk.Frame(main_frame, bg="#f0f0f0", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        # Right panel (visualization)
        right_panel = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Control Frame
        control_frame = tk.Frame(left_panel, bg="#f0f0f0", bd=1, relief=tk.RIDGE)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Algorithm Selection
        tk.Label(control_frame, text="Algorithm:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_menu = ttk.Combobox(control_frame, textvariable=self.algo_var, 
                                     values=list(self.algo_docs.keys()), width=15)
        self.algo_menu.grid(row=0, column=1, padx=5, pady=5)
        self.algo_menu.bind("<<ComboboxSelected>>", self.update_documentation)

        # Initial Position
        tk.Label(control_frame, text="Initial Position:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.init_pos_entry = tk.Entry(control_frame, width=15)
        self.init_pos_entry.grid(row=1, column=1, padx=5, pady=5)
        self.init_pos_entry.insert(0, "50")

        # Requests
        tk.Label(control_frame, text="Requests:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.requests_entry = tk.Entry(control_frame, width=15)
        self.requests_entry.grid(row=2, column=1, padx=5, pady=5)
        self.requests_entry.insert(0, "90,12,56,77")

        # Direction (for SCAN/C-SCAN)
        tk.Label(control_frame, text="Direction:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.direction_var = tk.StringVar(value="right")
        ttk.Radiobutton(control_frame, text="Right", variable=self.direction_var, value="right").grid(row=3, column=1, padx=5, sticky="w")
        ttk.Radiobutton(control_frame, text="Left", variable=self.direction_var, value="left").grid(row=4, column=1, padx=5, sticky="w")

        # Disk Size
        tk.Label(control_frame, text="Disk Size:", font=("Arial", 12), bg="#f0f0f0").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.disk_size_entry = tk.Entry(control_frame, width=15)
        self.disk_size_entry.grid(row=5, column=1, padx=5, pady=5)
        self.disk_size_entry.insert(0, "200")

        # Run Button
        run_btn = tk.Button(control_frame, text="Visualize", font=("Arial", 12, "bold"),
                          bg="#4CAF50", fg="white", command=self.visualize)
        run_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # Documentation Frame
        doc_frame = tk.Frame(left_panel, bg="#f0f0f0", bd=1, relief=tk.RIDGE)
        doc_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Documentation Title
        tk.Label(doc_frame, text="Algorithm Documentation", font=("Arial", 14, "bold"), 
                bg="#f0f0f0").pack(pady=5)

        # Documentation Text
        self.doc_text = scrolledtext.ScrolledText(doc_frame, wrap=tk.WORD, width=45, height=20,
                                               font=("Arial", 11), bg="white", bd=0)
        self.doc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Visualization Frame
        self.viz_frame = tk.Frame(right_panel, bg="#ffffff")
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Results Frame
        self.results_frame = tk.Frame(right_panel, bg="#f0f0f0", height=150)
        self.results_frame.pack(fill=tk.X, padx=10, pady=10)

        # Initialize plot
        self.fig = None
        self.ax_disk = None
        self.ax_chart = None
        self.canvas = None
        self.animation = None

        # Initialize documentation
        self.update_documentation()

    def update_documentation(self, event=None):
        """Update the documentation panel based on selected algorithm"""
        algo = self.algo_var.get()
        doc = self.algo_docs.get(algo, {})
        
        # Format documentation
        text = f"Algorithm: {algo}\n{'='*50}\n\n"
        text += f"Description:\n{textwrap.fill(doc.get('description', ''), width=50)}\n\n"
        text += f"Algorithm Steps:\n{doc.get('algorithm', '')}\n\n"
        text += f"Advantages:\n{doc.get('advantages', '')}\n\n"
        text += f"Disadvantages:\n{doc.get('disadvantages', '')}\n\n"
        text += f"Complexity:\n{doc.get('complexity', '')}"
        
        # Update text widget
        self.doc_text.config(state=tk.NORMAL)
        self.doc_text.delete(1.0, tk.END)
        self.doc_text.insert(tk.INSERT, text)
        self.doc_text.config(state=tk.DISABLED)

    def show_results_popup(self, algorithm, sequence, total_movement, metrics):
        popup = tk.Toplevel(self.root)
        popup.title("Disk Scheduling Results")
        popup.geometry("500x250")
        popup.configure(bg="#f0f0f0")
        
        # Algorithm label
        tk.Label(popup, text=f"Algorithm: {algorithm}", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5, anchor="w", padx=10)
        
        # Sequence label (scrollable if long)
        seq_text = " → ".join(map(str, sequence))
        seq_frame = tk.Frame(popup, bg="#f0f0f0")
        seq_frame.pack(fill=tk.X, padx=10, pady=5)
        
        seq_scroll = tk.Scrollbar(seq_frame, orient=tk.HORIZONTAL)
        seq_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        seq_label = tk.Text(seq_frame, height=2, wrap=tk.NONE, xscrollcommand=seq_scroll.set, bg="#f0f0f0", borderwidth=0, font=("Arial", 12))
        seq_label.insert(tk.END, f"Sequence: {seq_text}")
        seq_label.config(state=tk.DISABLED)
        seq_label.pack(fill=tk.X)
        
        seq_scroll.config(command=seq_label.xview)
        
        # Metrics Frame
        metrics_frame = tk.Frame(popup, bg="#f0f0f0")
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(metrics_frame, text="Performance Metrics:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        tk.Label(metrics_frame, text=f"Total Head Movement: {total_movement} cylinders", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        tk.Label(metrics_frame, text=f"Throughput: {metrics['throughput']:.2f} requests/cylinder", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        tk.Label(metrics_frame, text=f"Avg Seek Time: {metrics['avg_seek_time']:.2f} cylinders/request", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        
        # Close button
        close_btn = tk.Button(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=10)

    def visualize(self):
        try:
            # Get inputs
            algorithm = self.algo_var.get()
            initial_pos = int(self.init_pos_entry.get())
            requests = [int(x.strip()) for x in self.requests_entry.get().split(",")]
            disk_size = int(self.disk_size_entry.get())
            direction = self.direction_var.get()
            
            # Validate inputs
            if initial_pos < 0 or initial_pos >= disk_size:
                raise ValueError(f"Initial position must be between 0 and {disk_size-1}")
            for req in requests:
                if req < 0 or req >= disk_size:
                    raise ValueError(f"Request {req} is outside disk range (0-{disk_size-1})")
                    
            # Clear previous visualization
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if self.animation:
                self.animation.event_source.stop()
                
            # Calculate sequence based on algorithm
            sequence, total_movement, metrics = self.calculate_sequence(algorithm, initial_pos, requests, disk_size, direction)
            
            # Update results
            self.update_results(algorithm, sequence, total_movement, metrics)
            
            # Create visualization
            self.create_dual_visualization(disk_size, initial_pos, requests, sequence)
            self.show_results_popup(algorithm, sequence, total_movement, metrics)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            
    def calculate_sequence(self, algorithm, initial_pos, requests, disk_size, direction):
        sequence = [initial_pos]
        reqs = requests.copy()
        current_pos = initial_pos
        total_movement = 0
        metrics = {
            "total_requests": len(requests),
            "throughput": 0,
            "avg_seek_time": 0
        }
        
        if algorithm == "FCFS":
            for req in reqs:
                total_movement += abs(req - current_pos)
                current_pos = req
                sequence.append(req)
                
        elif algorithm == "SSTF":
            while reqs:
                closest = min(reqs, key=lambda x: abs(x - current_pos))
                total_movement += abs(closest - current_pos)
                current_pos = closest
                sequence.append(closest)
                reqs.remove(closest)
                
        elif algorithm == "SCAN":
            if direction == "right":
                reqs_sorted = sorted([r for r in reqs if r >= current_pos])
                reqs_sorted += [disk_size - 1] + sorted([r for r in reqs if r < current_pos], reverse=True)
            else:
                reqs_sorted = sorted([r for r in reqs if r <= current_pos], reverse=True)
                reqs_sorted += [0] + sorted([r for r in reqs if r > current_pos])
                
            for pos in reqs_sorted:
                total_movement += abs(pos - current_pos)
                current_pos = pos
                sequence.append(pos)
                
        elif algorithm == "C-SCAN":
            if direction == "right":
                reqs_sorted = sorted([r for r in reqs if r >= current_pos])
                reqs_sorted += [disk_size - 1, 0] + sorted([r for r in reqs if r < current_pos])
            else:
                reqs_sorted = sorted([r for r in reqs if r <= current_pos], reverse=True)
                reqs_sorted += [0, disk_size - 1] + sorted([r for r in reqs if r > current_pos], reverse=True)
                
            for pos in reqs_sorted:
                total_movement += abs(pos - current_pos)
                current_pos = pos
                sequence.append(pos)
                
        elif algorithm == "LOOK":
            if direction == "right":
                reqs_sorted = sorted([r for r in reqs if r >= current_pos])
                reqs_sorted += sorted([r for r in reqs if r < current_pos], reverse=True)
            else:
                reqs_sorted = sorted([r for r in reqs if r <= current_pos], reverse=True)
                reqs_sorted += sorted([r for r in reqs if r > current_pos])
                
            for pos in reqs_sorted:
                total_movement += abs(pos - current_pos)
                current_pos = pos
                sequence.append(pos)
                
        elif algorithm == "C-LOOK":
            if direction == "right":
                reqs_sorted = sorted([r for r in reqs if r >= current_pos])
                reqs_sorted += sorted([r for r in reqs if r < current_pos])
            else:
                reqs_sorted = sorted([r for r in reqs if r <= current_pos], reverse=True)
                reqs_sorted += sorted([r for r in reqs if r > current_pos], reverse=True)
                
            for pos in reqs_sorted:
                total_movement += abs(pos - current_pos)
                current_pos = pos
                sequence.append(pos)
        
        # Calculate metrics
        metrics["throughput"] = len(requests) / (total_movement if total_movement > 0 else 1)
        metrics["avg_seek_time"] = total_movement / len(requests) if requests else 0
        
        return sequence, total_movement, metrics
        
    def update_results(self, algorithm, sequence, total_movement, metrics):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Create a grid for results
        results_grid = tk.Frame(self.results_frame, bg="#f0f0f0")
        results_grid.pack(fill=tk.X, padx=10, pady=5)
            
        # Algorithm info
        tk.Label(results_grid, text=f"Algorithm: {algorithm}", 
                font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5)
                
        # Sequence
        seq_text = " → ".join(map(str, sequence))
        tk.Label(results_grid, text=f"Sequence: {seq_text}", 
                font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5)
                
        # Metrics
        metrics_frame = tk.Frame(results_grid, bg="#f0f0f0")
        metrics_frame.grid(row=0, column=1, rowspan=2, padx=20)
        
        tk.Label(metrics_frame, text="Performance Metrics:", 
                font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, sticky="w")
        
        tk.Label(metrics_frame, text=f"Total Head Movement: {total_movement} cylinders", 
                font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        
        tk.Label(metrics_frame, text=f"Throughput: {metrics['throughput']:.2f} requests/cylinder", 
                font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=1, sticky="w", padx=20)
                
        tk.Label(metrics_frame, text=f"Avg Seek Time: {metrics['avg_seek_time']:.2f} cylinders/request", 
                font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="w")
                
    def create_dual_visualization(self, disk_size, initial_pos, requests, sequence):
        # Create figure with two subplots
        self.fig = plt.figure(figsize=(12, 6))
        gs = GridSpec(1, 2, width_ratios=[1, 1.5])
        self.ax_disk = self.fig.add_subplot(gs[0], polar=True)
        self.ax_chart = self.fig.add_subplot(gs[1])
        
        # Disk visualization setup
        self.setup_disk_visualization(disk_size, initial_pos, requests)
        
        # Chart visualization setup
        self.setup_chart_visualization(sequence)
        
        # Create animation objects for disk
        self.disk_path, = self.ax_disk.plot([], [], 'r-', linewidth=2, alpha=0.7)
        self.disk_pointer, = self.ax_disk.plot([], [], 'ro', markersize=10)
        
        # Create animation objects for chart
        self.chart_line, = self.ax_chart.plot([], [], 'b-', linewidth=2)
        self.chart_points, = self.ax_chart.plot([], [], 'bo', markersize=8)
        self.chart_current, = self.ax_chart.plot([], [], 'ro', markersize=10)
        
        # Animation function
        def update(frame):
            if frame == 0:
                return self.disk_path, self.disk_pointer, self.chart_line, self.chart_points, self.chart_current
            
            # Update disk visualization
            current_pos = sequence[frame]
            prev_pos = sequence[frame-1]
            
            # Calculate angles (convert to radians)
            angle = 2 * np.pi * current_pos / disk_size
            prev_angle = 2 * np.pi * prev_pos / disk_size
            
            # For smooth movement along circumference
            if abs(current_pos - prev_pos) > disk_size/2:  # Handle wrap-around
                if current_pos > prev_pos:
                    # Moving left through 0
                    angles = np.linspace(prev_angle, 2*np.pi, 10)
                    angles = np.concatenate([angles, np.linspace(0, angle, 10)])
                else:
                    # Moving right through end
                    angles = np.linspace(prev_angle, 0, 10)
                    angles = np.concatenate([angles, np.linspace(2*np.pi, angle, 10)])
            else:
                angles = np.linspace(prev_angle, angle, 20)
            
            # Update disk path
            self.disk_path.set_data(angles, np.ones_like(angles))
            self.disk_pointer.set_data([angle], [1])
            
            # Highlight current position on disk
            for i, txt in enumerate(self.ax_disk.texts):
                if txt.get_text() == str(current_pos):
                    txt.set_color('red')
                    txt.set_fontweight('bold')
                else:
                    txt.set_color('black')
                    txt.set_fontweight('normal')
            
            # Update chart visualization
            x_data = [pos for pos in sequence[:frame+1]]
            y_data = list(range(frame+1))
            self.chart_line.set_data(x_data, y_data)
            self.chart_points.set_data(x_data, y_data)
            self.chart_current.set_data([current_pos], [frame])
            
            # Adjust chart limits if needed
            if frame > self.ax_chart.get_xlim()[1] - 2:
                self.ax_chart.set_xlim(0, len(sequence))
            
            return self.disk_path, self.disk_pointer, self.chart_line, self.chart_points, self.chart_current
            
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Start animation
        self.animation = FuncAnimation(self.fig, update, frames=len(sequence), 
                                     interval=800, blit=True, repeat=False)
        
    def setup_disk_visualization(self, disk_size, initial_pos, requests):
        self.ax_disk.clear()
        self.ax_disk.set_theta_zero_location('N')
        self.ax_disk.set_theta_direction(-1)
        self.ax_disk.set_ylim(0, 1.2)
        self.ax_disk.set_xticks([])
        self.ax_disk.set_yticks([])
        self.ax_disk.set_title("Disk Head Movement (Circumference Path)", pad=20)
        
        # Draw disk outline with better colors
        theta = np.linspace(0, 2*np.pi, 100)
        radius = np.ones(100)
        self.ax_disk.plot(theta, radius, '#4682B4', linewidth=3, alpha=0.7)
        
        # Mark only important positions (0, disk_size-1, initial, and requests)
        important_positions = {0, disk_size-1, initial_pos}
        important_positions.update(requests)
        
        for pos in sorted(important_positions):
            angle = 2 * np.pi * pos / disk_size
            color = '#FF6347' if pos in requests else '#2E8B57' if pos == initial_pos else '#4682B4'
            marker = 'o'
            size = 8 if pos in (0, disk_size-1, initial_pos) else 6
            self.ax_disk.plot(angle, 1, marker=marker, color=color, markersize=size)
            self.ax_disk.text(angle, 1.1, str(pos), ha='center', va='center', 
                             color=color, fontweight='bold' if pos in (0, disk_size-1, initial_pos) else 'normal')
        
        # Add legend
        self.ax_disk.plot([], [], 'o', color='#2E8B57', markersize=8, label='Initial Position')
        self.ax_disk.plot([], [], 'o', color='#FF6347', markersize=6, label='Request')
        self.ax_disk.plot([], [], 'o', color='#4682B4', markersize=8, label='Boundary')
        self.ax_disk.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
    def setup_chart_visualization(self, sequence):
        self.ax_chart.clear()
        self.ax_chart.set_ylim(0, len(sequence)-1)
        self.ax_chart.set_xlim(min(sequence)-10, max(sequence)+10)
        self.ax_chart.set_ylabel("Step Number")
        self.ax_chart.set_xlabel("Track Number")
        self.ax_chart.set_title("Head Movement Sequence", pad=20)
        self.ax_chart.grid(True, alpha=0.3)
        
        self.ax_chart.yaxis.set_major_locator(MaxNLocator(integer=True))
        # Add vertical lines for each unique position
        for pos in sorted(set(sequence)):
            self.ax_chart.axvline(x=pos, color='gray', linestyle='--', alpha=0.3)
        
        # Add initial point
        self.ax_chart.plot(sequence[0], 0, 'yo', markersize=8, label='Start')
        self.ax_chart.legend()

def main():
    root = tk.Tk()
    app = DiskSchedulingVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()