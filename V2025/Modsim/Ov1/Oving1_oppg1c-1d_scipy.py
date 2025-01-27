import sympy as sm
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

sm.init_printing(use_latex='mathjax')

def MFD(t, X):
    return [X[1], -X[0]]

x0 = [1, 0]

t_span = (0, 30)
t_eval = np.linspace(0,30,300)

k = 1
d = 0
m = 1

solution = solve_ivp(MFD, t_span, x0, t_eval = t_eval)

plt.figure(figsize=(10, 5))
plt.plot(solution.t, solution.y[0], label='x(t) - SciPy Solution', color='blue')
plt.title('Solution of the ODE with SciPy')
plt.xlabel('Time (t)')
plt.ylabel('x(t)')
plt.legend()
plt.grid()
plt.show()