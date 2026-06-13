import math

def simulate():
    t = 0; h = 0; v = 0

    m = 23200
    fuel = 11200
    apogee = False

    ts = []; hs = []; vs = []; ms = []

    while t <= 500:
        fuel_sec = 0
        f_thrust = 0
        if t <= 58 and fuel > 0:
            fuel_sec = 11200 / 58
            f_thrust = fuel_sec * 285 * 9.81

        if h >= 70000: air = 0
        else: air = 1.225 * math.exp(-h / 5000)

        f_drag = 0.5 * air * abs(v) * abs(v) * 0.35 * 7

        if v > 0: a_drag = -f_drag / m
        elif v < 0: a_drag = f_drag / m
        else: a_drag = 0

        a = f_thrust / m - 9.81 + a_drag

        ts += [t]; hs += [max(h, 0)]; vs += [v]; ms += [m]

        v = v + a * 0.1
        h = h + v * 0.1

        fuel = max(0, fuel - fuel_sec * 0.1)
        m = 12000 + fuel

        t = t + 0.1

        if v < 0 and h > 90000: apogee = True
        if apogee and h <= 0: break

    return ts, hs, vs, ms

ts, hs, vs, ms = simulate()

print(f"Max altitude: {max(hs):,.0f} m")
print(f"Apogee time: {ts[hs.index(max(hs))]:.1f} s")
print(f"Max upward velocity: {max(vs):,.0f} m/s")
print(f"Final mass: {ms[-1]:,.0f} kg")
