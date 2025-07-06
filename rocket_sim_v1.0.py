import numpy as np
import matplotlib.pyplot as plt

# === Constants ===
g = 9.81  # gravity (m/s^2)
mass_initial = 0.5  # kg
mass_final = 0.3    # kg after fuel is burned
thrust = 15         # N
burn_time = 3       # seconds
drag_coefficient = 0.75
dt = 0.01           # time step
total_time = 10     # seconds

# === Time setup ===
time = np.arange(0, total_time, dt)
altitude = np.zeros_like(time)
velocity = np.zeros_like(time)
acceleration = np.zeros_like(time)
mass = np.zeros_like(time)
mass[0] = mass_initial
fuel_burn_rate = (mass_initial - mass_final) / burn_time  # kg/s

# === Simulation Loop ===
for i in range(1, len(time)):
    t = time[i]

    # Update mass
    if t <= burn_time:
        mass[i] = mass[i-1] - fuel_burn_rate * dt
    else:
        mass[i] = mass[i-1]

    # Thrust logic
    current_thrust = thrust if t <= burn_time else 0

    # Drag force
    drag = drag_coefficient * velocity[i-1]**2 if velocity[i-1] > 0 else 0

    # Net force and motion
    net_force = current_thrust - (mass[i] * g) - drag
    acceleration[i] = net_force / mass[i]
    velocity[i] = velocity[i-1] + acceleration[i] * dt
    altitude[i] = max(0, altitude[i-1] + velocity[i] * dt)

# === Plotting ===
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time, altitude, label='Altitude (m)', color='blue')
plt.ylabel("Altitude (m)")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, velocity, label='Velocity (m/s)', color='green')
plt.ylabel("Velocity (m/s)")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time, acceleration, label='Acceleration (m/s²)', color='red')
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
