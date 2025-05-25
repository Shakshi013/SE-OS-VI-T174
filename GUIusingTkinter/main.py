import tkinter as tk
from tkinter import ttk

# Import your visualizer launchers
from memory_management import launch_memory_management
# from cpu_scheduler import launch_cpu_scheduler
# from disk_scheduler import launch_disk_scheduler

def main():
    root = tk.Tk()
    root.title("System Algorithm Visualizer")
    root.geometry("500x400")

    ttk.Label(root, text="Choose Module to Visualize", font=("Arial", 16)).pack(pady=20)

    ttk.Button(root, text="Memory Management", command=launch_memory_management).pack(pady=10)
    #ttk.Button(root, text="CPU Scheduling", command=launch_cpu_scheduler).pack(pady=10)
    #ttk.Button(root, text="Disk Scheduling", command=launch_disk_scheduler).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
