import numpy as np
import matplotlib.pyplot as plt

###############################################################################
# 1) Exact solution for damped mass-spring system
###############################################################################
def exact_solution_damped_msd(t, m, d, k):
    """
    Returns x(t) for the damped mass-spring system:
        m*x'' + d*x' + k*x = 0
    with x(0) = 1, x'(0) = 0.
    
    Parameters:
    -----------
    t : float or 1D array
        Time(s) at which to evaluate the solution.
    m : float
        Mass (kg).
    d : float
        Damping coefficient (Ns/m).
    k : float
        Spring constant (N/m).
        
    Returns:
    --------
    x : array
        The exact solution x(t) at each time in t.
    """
    t = np.atleast_1d(t)  # handle scalar or vector input
    x = np.zeros_like(t, dtype=float)

    # Natural freq (undamped) and damping factor
    omega0 = np.sqrt(k/m)   # "natural frequency"
    delta  = d/(2*m)        # damping factor

    # 3 possible damping regimes: underdamped, critically damped, overdamped
    # We'll check them in that order:
    if np.isclose(delta, omega0, rtol=1e-14):
        # ~~~~~ Critically Damped ~~~~~
        # x(t) = e^(-delta*t) [1 + delta*t]
        for i, ti in enumerate(t):
            x[i] = np.exp(-delta*ti) * (1.0 + delta*ti)

    elif delta < omega0:
        # ~~~~~ Underdamped ~~~~~
        # x(t) = e^(-delta*t) [ cos(omega_d*t) + (delta/omega_d)*sin(omega_d*t) ]
        omega_d = np.sqrt(omega0**2 - delta**2)
        for i, ti in enumerate(t):
            e_term = np.exp(-delta*ti)
            x[i] = e_term * (
                np.cos(omega_d*ti) + 
                (delta/omega_d)*np.sin(omega_d*ti)
            )

    else:
        # ~~~~~ Overdamped ~~~~~
        # roots: r1, r2 = -delta ± sqrt(delta^2 - omega0^2)
        under_sqrt = delta**2 - omega0**2
        root = np.sqrt(under_sqrt)
        r1 = -delta + root
        r2 = -delta - root

        # Solve for constants A,B given x(0)=1 and x'(0)=0
        # A + B = 1
        # A*r1 + B*r2 = 0
        # => A = -r2/(r1-r2), B = r1/(r1-r2)
        A = -r2 / (r1 - r2)
        B =  r1 / (r1 - r2)

        for i, ti in enumerate(t):
            x[i] = A*np.exp(r1*ti) + B*np.exp(r2*ti)

    return x


###############################################################################
# 2) Forward Euler integrator
###############################################################################
def forward_euler(m, d, k, x0=1.0, v0=0.0, dt=0.01, t_end=5.0):
    """
    Forward Euler numerical integration of:
      m*x'' + d*x' + k*x = 0
    with x(0)=x0, x'(0)=v0.
    
    Returns arrays: (t_vals, x_vals, v_vals).
    """
    N = int(np.ceil(t_end/dt))
    t_vals = np.zeros(N+1)
    x_vals = np.zeros(N+1)
    v_vals = np.zeros(N+1)

    # Initial conditions
    x_vals[0] = x0
    v_vals[0] = v0
    t_vals[0] = 0.0

    for i in range(N):
        x_old = x_vals[i]
        v_old = v_vals[i]

        # Euler updates
        # dx/dt = v
        # dv/dt = -(k/m)*x - (d/m)*v
        x_new = x_old + dt*v_old
        v_new = v_old + dt*(-(k/m)*x_old - (d/m)*v_old)

        x_vals[i+1] = x_new
        v_vals[i+1] = v_new
        t_vals[i+1] = t_vals[i] + dt

    return t_vals, x_vals, v_vals


###############################################################################
# 3) Choose system parameters, solve, compare
###############################################################################
if __name__ == "__main__":

    # Parameters
    m = 1.0     # mass (kg)
    k = 1     # spring constant (N/m)
    d = 2     # damping (Ns/m)
    dt = 0.01   # Euler step
    t_end = 30  # total simulation time

    # 3a) Exact solution
    t_exact = np.linspace(0, t_end, 1000)
    x_exact = exact_solution_damped_msd(t_exact, m, d, k)

    # 3b) Forward Euler
    t_eul, x_eul, v_eul = forward_euler(m, d, k, x0=1, v0=0, dt=dt, t_end=t_end)

    # 3c) Compare & compute error
    # Evaluate the exact solution at the Euler time points
    x_exact_eulerTimes = exact_solution_damped_msd(t_eul, m, d, k)
    error = np.abs(x_eul - x_exact_eulerTimes)

    # 3d) Plot results
    plt.figure(figsize=(10, 6))

    # Top subplot: position vs. time
    plt.subplot(2,1,1)
    plt.plot(t_eul, x_eul, 'bo-', label='Forward Euler', markevery=50)
    plt.plot(t_exact, x_exact, 'r--', label='Exact solution')
    plt.title(f"Mass-Spring-Damper (m={m}, k={k}, d={d}, dt={dt})")
    plt.xlabel("Time [s]")
    plt.ylabel("x(t)")
    plt.grid(True)
    plt.legend()

    # Bottom subplot: error vs. time
    plt.subplot(2,1,2)
    plt.plot(t_eul, error, 'k')
    plt.title("Absolute Error = |x_Euler - x_Exact|")
    plt.xlabel("Time [s]")
    plt.ylabel("Error")
    plt.grid(True)

    plt.tight_layout()
    plt.show()
