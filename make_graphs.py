import math
import matplotlib.pyplot as plt


def simulate_1d():
    t = 0; h = 0; v = 0
    m = 23200; fuel = 11200
    apogee = False
    ts = []; speeds = []; accs = []

    while t <= 500:
        fuel_sec = 0; ft = 0
        if t <= 58 and fuel > 0:
            fuel_sec = 11200 / 58
            ft = fuel_sec * 285 * 9.81

        if h >= 70000: air = 0
        else: air = 1.225 * math.exp(-h / 5000)

        fd = 0.5 * air * abs(v) * abs(v) * 0.35 * 7

        if v > 0: ad = -fd / m
        elif v < 0: ad = fd / m
        else: ad = 0

        a = ft / m - 9.81 + ad

        ts += [t]; speeds += [abs(v)]; accs += [abs(a)]

        v = v + a * 0.1
        h = h + v * 0.1
        fuel = max(0, fuel - fuel_sec * 0.1)
        m = 12000 + fuel
        t = t + 0.1

        if v < 0 and h > 90000: apogee = True
        if apogee and h <= 0: break

    return ts, speeds, accs


def simulate_2d():
    angle = math.radians(75)
    t = 0; x = 0; h = 0
    vx = 0; vh = 0
    m = 23200; fuel = 11200
    ts = []; speeds = []; accs = []

    while t <= 500:
        fuel_sec = 0; ft = 0
        if t <= 58 and fuel > 0:
            fuel_sec = 11200 / 58
            ft = fuel_sec * 285 * 9.81

        if h >= 70000: air = 0
        else: air = 1.225 * math.exp(-h / 5000)

        speed = math.sqrt(vx * vx + vh * vh)
        fd = 0.5 * air * speed * speed * 0.35 * 7

        if speed > 0:
            adx = -fd * vx / speed / m
            adh = -fd * vh / speed / m
        else:
            adx = 0
            adh = 0

        ax = ft * math.cos(angle) / m + adx
        ah = ft * math.sin(angle) / m - 9.81 + adh
        acc = math.sqrt(ax * ax + ah * ah)

        ts += [t]; speeds += [speed]; accs += [acc]

        vx = vx + ax * 0.1
        vh = vh + ah * 0.1
        x = x + vx * 0.1
        h = h + vh * 0.1
        fuel = max(0, fuel - fuel_sec * 0.1)
        m = 12000 + fuel
        t = t + 0.1

        if t > 1 and h <= 0:
            break

    return ts, speeds, accs


ts1, speeds1, accs1 = simulate_1d()
ts2, speeds2, accs2 = simulate_2d()

plt.figure(figsize=(8, 5))
plt.plot(ts1, speeds1, label="1D")
plt.plot(ts2, speeds2, label="2D")
plt.title("Speed over time")
plt.xlabel("Time, s")
plt.ylabel("Speed, m/s")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("graph_speed_time.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(ts1, accs1, label="1D")
plt.plot(ts2, accs2, label="2D")
plt.title("Acceleration over time")
plt.xlabel("Time, s")
plt.ylabel("Acceleration, m/s^2")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("graph_acceleration_time.png", dpi=150)
plt.close()
