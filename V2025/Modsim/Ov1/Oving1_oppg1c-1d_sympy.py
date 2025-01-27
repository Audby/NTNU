import sympy as sp

t = sp.Symbol('t', real=True)
x = sp.Function('x')(t)

ode = sp.Eq(x.diff(t, 2) + x, 0)

sol = sp.dsolve(
    ode, 
    ics={x.subs(t, 0): 1, x.diff(t).subs(t, 0): 0}
)

print(sol)

sp.plot(sol.rhs, (t,0,30), title="Masse-fjær-demper", xlabel="t", ylabel="x(t)")
