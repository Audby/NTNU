#!/usr/bin/env python
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

###############################################################################
# 1) SYMBOLIC DEFINITIONS
###############################################################################

# Define symbols for system parameters
J, M, R, g, T_o = sp.symbols("J M R g T_o", real=True, positive=True)

# Generalized coordinates and their time derivatives
x, theta = sp.symbols("x theta", real=True)
x_dot, theta_dot = sp.symbols("xdot thetadot", real=True)

# Group coordinates into vectors
q = sp.Matrix([x, theta])
q_dot = sp.Matrix([x_dot, theta_dot])

# -------------------------------
# Position of the ball’s center
# (p = [x*cos(theta) - R*sin(theta), x*sin(theta) + R*cos(theta)])
p = sp.Matrix([
    x * sp.cos(theta) - R * sp.sin(theta),
    x * sp.sin(theta) + R * sp.cos(theta)
])
# Its time derivative: p_dot = Jacobian(p,q)*q_dot
p_dot = p.jacobian(q) * q_dot

# -------------------------------
# Kinetic Energy

# Beam (pure rotation)
T_beam = 0.5 * J * theta_dot**2

# Ball (translation)
T_ball_trans = 0.5 * M * (p_dot.dot(p_dot))

# Ball (rotation); note: for a solid sphere I_ball = (2/5)*M*R^2,
# and its rotation rate is the sum of the beam’s rotation and the rolling:
I_ball = (2 * M * R**2) / 5
omega = theta_dot + x_dot / R
T_ball_rot = 0.5 * I_ball * omega**2

# Total kinetic energy
T_total = T_beam + T_ball_trans + T_ball_rot

# -------------------------------
# Potential Energy (ball’s center; note: height = p[1])
V = M * g * (x * sp.sin(theta) + R * sp.cos(theta))

# -------------------------------
# Lagrangian
L = T_total - V

# -------------------------------
# Generalized force: only a torque on the beam (i.e. on theta)
Q = sp.Matrix([0, T_o])

# -------------------------------
# Compute derivatives for Lagrange’s equations:
# Lagrange’s eqn: d/dt(∂L/∂q_dot) - ∂L/∂q = Q
#
# To get the mass matrix we need the Hessian of L with respect to q_dot:
dL_dq = sp.Matrix([sp.diff(L, var) for var in (x, theta)])
dL_dqdot = sp.Matrix([sp.diff(L, var) for var in (x_dot, theta_dot)])
d2L_dqdot2 = sp.Matrix([[sp.diff(dL_dqdot[i], var) for var in (x_dot, theta_dot)]
                          for i in range(2)])
# Also compute the mixed derivatives (∂^2L/∂q_dot∂q):
d2L_dqdotdq = sp.Matrix([[sp.diff(dL_dq[i], var) for var in (x_dot, theta_dot)]
                           for i in range(2)])

# The mass matrix (W) and remaining terms (RHS):
W_expr = sp.simplify(d2L_dqdot2)
RHS_expr = sp.simplify(Q + (dL_dq - d2L_dqdotdq * q_dot))

# -------------------------------
# Lambdify the expressions.
# We will let the lambdified functions depend on:
#   - the state: (x, theta, x_dot, theta_dot)
#   - parameters: (J, M, R, g)
#   - external torque T_o
state_syms = (x, theta, x_dot, theta_dot)
param_syms = (J, M, R, g)

W_func = sp.lambdify((state_syms, param_syms, T_o), W_expr, "numpy")
RHS_func = sp.lambdify((state_syms, param_syms, T_o), RHS_expr, "numpy")

###############################################################################
# 2) NUMERICAL DYNAMICS
###############################################################################
def ball_and_beam_ode(t, y, param_values, torque_value=0.0):
    """
    Computes the time derivative of the state.
    
    y: [x, theta, x_dot, theta_dot]
    param_values: (J, M, R, g)
    torque_value: external torque (T_o)
    Returns: [x_dot, theta_dot, x_ddot, theta_ddot]
    """
    # Unpack state variables
    x_val, theta_val, xdot_val, thetadot_val = y
    # Unpack parameters
    J_val, M_val, R_val, g_val = param_values

    # Prepare tuples of numerical values
    state_vals = (x_val, theta_val, xdot_val, thetadot_val)
    param_vals = (J_val, M_val, R_val, g_val)

    # Evaluate the mass matrix and RHS vector
    W_mat = np.array(W_func(state_vals, param_vals, torque_value), dtype=float)
    RHS_vec = np.array(RHS_func(state_vals, param_vals, torque_value), dtype=float).flatten()

    # Solve for accelerations: W * q_ddot = RHS  ->  q_ddot = inv(W) * RHS
    q_ddot = np.linalg.solve(W_mat, RHS_vec)

    return [xdot_val, thetadot_val, q_ddot[0], q_ddot[1]]

###############################################################################
# 3) SIMULATION
###############################################################################
if __name__ == "__main__":
    # Numeric parameter values
    J_val = 1.0
    M_val = 10.0
    R_val = 0.25
    g_val = 9.82

    # Initial state: [x, theta, x_dot, theta_dot]
    y0 = [0.1, np.deg2rad(5), 0.0, 0.0]

    # Time span for simulation
    t_span = (0, 10)
    t_eval = np.linspace(0, 10, 300)

    # For this simulation, let the external torque be zero.
    torque_val = 0.0

    # Solve the ODE
    sol = solve_ivp(
        fun=lambda t, y: ball_and_beam_ode(t, y, (J_val, M_val, R_val, g_val), torque_val),
        t_span=t_span, y0=y0, t_eval=t_eval
    )

    ts = sol.t
    ys = sol.y  # ys has shape (4, len(ts))

    ###############################################################################
    # 4) ANIMATION WITH MATPLOTLIB
    ###############################################################################
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim([-1.5, 1.5])  # Room for a beam of length ~3
    ax.set_ylim([-1.0, 1.5])

    # Define the beam: a line from -L/2 to +L/2 (pivot at origin)
    beam_length = 3.0
    line_beam, = ax.plot([], [], 'r-', lw=3)
    point_ball, = ax.plot([], [], 'bo', markersize=12)

    def init():
        line_beam.set_data([], [])
        point_ball.set_data([], [])
        return line_beam, point_ball

    def update(frame):
        # Extract current state
        x_  = ys[0, frame]     # ball's position along beam
        th_ = ys[1, frame]     # beam angle
        
        # Beam endpoints in beam's local frame
        L = beam_length
        xA = -L/2
        xB = +L/2
        # Rotate endpoints to world frame
        xA_world = xA * np.cos(th_)
        yA_world = xA * np.sin(th_)
        xB_world = xB * np.cos(th_)
        yB_world = xB * np.sin(th_)
        line_beam.set_data([xA_world, xB_world], [yA_world, yB_world])

        # Compute ball center position in world coordinates:
        # p = [ x*cos(th) - R*sin(th), x*sin(th) + R*cos(th) ]
        px = x_ * np.cos(th_) - R_val * np.sin(th_)
        py = x_ * np.sin(th_) + R_val * np.cos(th_)
        point_ball.set_data([px], [py])

        return line_beam, point_ball

    ani = animation.FuncAnimation(
        fig, update, frames=len(ts), interval=30, blit=True, init_func=init
    )

    plt.title("Ball on Beam (2D Animation)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()
