import math

angle = math.radians(75)

def simulate():
    t = 0; x = 0; h = 0
    vx = 0; vh = 0
    ts = []; xs = []; hs = []; speeds = []; ms = []

    m = 23200; fuel = 11200

    while t <= 500:
        fuel_sec = 0; ft = 0
        if t <= 58 and fuel > 0:
            fuel_sec = 11200 / 58; ft = fuel_sec * 285 * 9.81

        if h >= 70000: air = 0
        else: air = 1.225 * math.exp(-h / 5000)

        speed = math.sqrt(vx * vx + vh * vh)
        fd = 0.5 * air * speed * speed * 0.35 * 7

        if speed > 0:
            adx = -fd * vx / speed / m; adh = -fd * vh / speed / m
        else:
            adx = 0; adh = 0

        ax = ft * math.cos(angle) / m + adx
        ah = ft * math.sin(angle) / m - 9.81 + adh

        ts += [t]; xs += [x]; hs += [max(h, 0)]; speeds += [speed]; ms += [m]

        vx = vx + ax * 0.1; vh = vh + ah * 0.1
        x = x + vx * 0.1; h = h + vh * 0.1

        fuel = max(0, fuel - fuel_sec * 0.1)

        m = 12000 + fuel
        t = t + 0.1
        if t > 1 and h <= 0:
            break
    return ts, xs, hs, speeds, ms

ts, xs, hs, speeds, ms = simulate()

print(f"Max altitude: {max(hs):,.0f} m")
print(f"Apogee time: {ts[hs.index(max(hs))]:.1f} s")
print(f"Flight range: {max(xs):,.0f} m")
print(f"Max speed: {max(speeds):,.0f} m/s")
print(f"Final mass: {ms[-1]:,.0f} kg")
