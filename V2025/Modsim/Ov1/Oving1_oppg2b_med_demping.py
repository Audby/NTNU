import numpy as np
import matplotlib.pyplot as plt

# System parameters
k = 5         # Spring constant (N/m)
m = 1         # Mass (kg)
d = 0         # Damping coefficient (Ns/m), set to 0 for now

# Simulation settings
sim_time = 30  # Total simulation time (s)
dt = 0.01      # Time step size (s)

# Initialize arrays to store data
x_data = []       # Position values
x_dot_data = []   # Velocity values
t_data = []       # Time values

# Initial conditions
x = 1             # Initial position (1 m away from equilibrium)
x_dot = 0         # Initial velocity (0 m/s)
time = 0

# Store initial values
x_data.append(x)
x_dot_data.append(x_dot)
t_data.append(time)

# Forward Euler integration
while time <= sim_time:
    # Save current state
    x_old = x
    x_dot_old = x_dot

    # Euler updates
    x = x_old + x_dot_old * dt
    x_dot = x_dot_old + (-k/m * x_old - d/m * x_dot_old) * dt

    # Advance time
    time += dt

    # Store the new values
    x_data.append(x)
    x_dot_data.append(x_dot)
    t_data.append(time)

print(x_data[50], x_data[1000], x_data[1500], x_data[2200], x_data[3000])

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(t_data, x_data, label="x(t) - Position", linewidth=2)
plt.plot(t_data, x_dot_data, label="x'(t) - Velocity", linewidth=2)
plt.title("Mass-Spring-Damper System (Forward Euler Integration)", fontsize=14)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("State", fontsize=12)
plt.legend()
plt.grid(True)
plt.show()