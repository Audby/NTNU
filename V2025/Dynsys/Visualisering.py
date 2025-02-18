import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Matrix A
A = np.array([[1, 3],
              [3, 1]])

# Define the system dx/dt = A x
def system(t, x):
    return A @ x  # Matrix multiplication

# Create a mesh grid for plotting the vector field
x_vals = np.linspace(-2, 2, 20)
y_vals = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x_vals, y_vals)

# Compute the vector field components at each point on the grid
U = A[0,0]*X + A[0,1]*Y
V = A[1,0]*X + A[1,1]*Y

fig, ax = plt.subplots(figsize=(6, 6))

# Plot the vector field using quiver
ax.quiver(X, Y, U, V, color='gray', alpha=0.5)

# Alternatively, you could use streamplot if you prefer smoother flow lines:
# ax.streamplot(X, Y, U, V, density=1, color='gray')

# Plot some trajectories by numerically integrating from a few initial conditions
t_span = (0, 2)    # time span for forward integration
t_eval = np.linspace(t_span[0], t_span[1], 200)

# Choose some initial conditions to see how they flow
initial_conditions = [
    [-1.5,  1.5],
    [ 1.5,  1.5],
    [-1.5, -1.5],
    [ 1.5, -1.5],
    [ 0.5,   0.0],
    [-0.5,   0.0],
]

for x0 in initial_conditions:
    # Integrate forward in time
    sol = solve_ivp(system, t_span, x0, t_eval=t_eval)
    ax.plot(sol.y[0], sol.y[1], 'b-', label='_nolegend_')  # forward trajectory
    
    # Integrate backward in time (to see full saddle structure)
    t_span_rev = (0, -2)
    sol_rev = solve_ivp(system, t_span_rev, x0, t_eval=np.linspace(0, -2, 200))
    ax.plot(sol_rev.y[0], sol_rev.y[1], 'r-', label='_nolegend_')  # backward trajectory

# Mark the origin
ax.plot(0, 0, 'ko', markersize=5)

# Eigenvectors: v1 = (1,1), v2 = (1,-1)
# We'll just plot lines from -2 to +2 in each eigen direction.
line_range = np.linspace(-2, 2, 2)

# line in direction (1,1) => y = x
ax.plot(line_range, line_range, 'g--', label='eigenvector λ=4') 

# line in direction (1,-1) => y = -x
ax.plot(line_range, -line_range, 'm--', label='eigenvector λ=-2')

ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_xlabel('$x_1$')
ax.set_ylabel('$x_2$')
ax.set_aspect('equal', 'box')
ax.set_title('Phase Portrait: Saddle (Eigenvalues 4 and -2)')

# Place a legend (suppress duplicates if you want)
ax.legend(loc='upper right')

plt.show()
