import numpy as np
import matplotlib.pyplot as plt

k = 1
m = 1
d = 0

time = 0
sim_time = 30
dt = 0.01

x_data = []
x_dot_data = []
t_data = []

x = 1
x_dot = 0

x_data.append(x)
x_dot_data.append(x_dot)
t_data.append(time)

i = 0
while time <= sim_time:
    x = x_data[i] + x_dot_data[i] * dt
    x_dot = x_dot_data[i] + (-k/m * x) * dt

    time = time + dt
    i = i+1

    x_data.append(x)
    x_dot_data.append(x_dot)
    t_data.append(time)

plt.plot(t_data, x_data, label="x(t)")
plt.plot(t_data, x_dot_data, label="x_dot")
plt.legend()
plt.grid(True)
plt.show()