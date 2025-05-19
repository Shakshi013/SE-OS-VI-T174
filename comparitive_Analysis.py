import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Disk Scheduling Algorithms
def fcfs(requests, head):
    return [head] + requests

def sstf(requests, head):
    sequence = [head]
    reqs = requests.copy()
    while reqs:
        closest = min(reqs, key=lambda x: abs(x - head))
        sequence.append(closest)
        reqs.remove(closest)
        head = closest
    return sequence

def scan(requests, head, disk_size, direction="left"):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    if direction == "left":
        return [head] + left[::-1] + [0] + right
    else:
        return [head] + right + [disk_size - 1] + left[::-1]

def cscan(requests, head, disk_size):
    right = sorted([r for r in requests if r >= head])
    left = sorted([r for r in requests if r < head])
    return [head] + right + [disk_size - 1, 0] + left

# Parameters
requests = [82, 170, 43, 140, 24, 16, 190]
initial_head = 50
disk_size = 200

# Generate sequences
algos = {
    "FCFS": fcfs(requests, initial_head),
    "SSTF": sstf(requests, initial_head),
    "SCAN": scan(requests, initial_head, disk_size, "left"),
    "C-SCAN": cscan(requests, initial_head, disk_size)
}

# Set up the animation figure
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Real-Time Disk Scheduling Algorithms Simulation", fontsize=16)
algo_names = list(algos.keys())
axes = axs.flatten()
lines = []
points = []

# Initialize subplots
for i, name in enumerate(algo_names):
    ax = axes[i]
    ax.set_title(name)
    ax.set_xlim(0, len(algos[name]))
    ax.set_ylim(0, disk_size)
    ax.set_xlabel("Step")
    ax.set_ylabel("Cylinder")
    line, = ax.plot([], [], lw=2, marker='o')
    point, = ax.plot([], [], 'ro')
    lines.append(line)
    points.append(point)
    ax.grid(True)

# Animation update function
def update(frame):
    for i, name in enumerate(algo_names):
        seq = algos[name][:frame+1]
        steps = list(range(len(seq)))
        lines[i].set_data(steps, seq)
        if seq:
            points[i].set_data([steps[-1]], [seq[-1]])
    return lines + points

ani = animation.FuncAnimation(fig, update, frames=max(len(seq) for seq in algos.values()), interval=800, blit=True, repeat=False)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
