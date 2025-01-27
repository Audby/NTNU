import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

k = 1
m = 1
d = 0.5

###############################################################################
# 1) The EXACT solution as a Python (numpy) function
###############################################################################
t_symbol = sp.Symbol('t', real=True)
# Suppose the exact solution is cos(sqrt(k/m)*t)
omega = sp.sqrt(k/m)      # symbolic
x_exact_expr = sp.cos(omega*t_symbol)
x_exact_fn   = sp.lambdify(t_symbol, x_exact_expr, 'numpy')

###############################################################################
# 2) The FORWARD EULER solution
###############################################################################

def forward_euler(m, d, k, x0=1.0, v0=0.0, dt=0.01, t_end=30.0):
    N = int(np.ceil(t_end/dt))
    t_vals = np.zeros(N+1)
    x_vals = np.zeros(N+1)
    v_vals = np.zeros(N+1)

    x_vals[0] = x0
    v_vals[0] = v0
    t_vals[0] = 0.0

    for i in range(N):
        x_old = x_vals[i]
        v_old = v_vals[i]
        
        # x' = v
        # v' = -(k/m)*x - (d/m)*v
        x_vals[i+1] = x_old + dt*v_old
        v_vals[i+1] = v_old + dt*(-k/m*x_old - d/m*v_old)
        t_vals[i+1] = t_vals[i] + dt

    return t_vals, x_vals, v_vals

t_eul, x_eul, v_eul = forward_euler(m, d, k, dt=0.01, t_end=30.0)

###############################################################################
# 3) Evaluate EXACT solution on the Euler time grid & measure error
###############################################################################
x_exact_vals = x_exact_fn(t_eul)
error = np.abs(x_eul - x_exact_vals)

###############################################################################
# 4) Plot
###############################################################################
plt.figure(figsize=(10,6))

# Upper plot: solution curves
plt.subplot(2,1,1)
plt.plot(t_eul, x_eul, 'b', label="Forward Euler (x)")
plt.plot(t_eul, x_exact_vals, 'r--', label="Exact (x)")
plt.title("x(t) comparison")
plt.legend()
plt.grid(True)

# Lower plot: error
plt.subplot(2,1,2)
plt.plot(t_eul, error, 'k', label="Absolute Error")
plt.title("Error over time")
plt.xlabel("Time (s)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
