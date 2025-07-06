import pygame
import pandas as pd

# === Load Flight & Log Data ===
flight_df = pd.read_csv("rocket_flight_data_for_pygame.csv")
log_df = pd.read_csv("rocket_terminal_log.csv")
altitudes = flight_df["Altitude"].values

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Rocket Launch Visual Simulator")
clock = pygame.time.Clock()

# === Rocket Visuals ===
rocket_width = 10
rocket_height = 30
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# === Fuel Gauge Settings ===
FUEL_X = 30
FUEL_Y = 50
FUEL_WIDTH = 20
FUEL_HEIGHT = 200
m_initial = log_df["Mass"].iloc[0]
m_final = min(log_df["Mass"])

# === Main Loop ===
running = True
frame = 0
frames_total = len(altitudes)

while running and frame < frames_total:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # === Rocket Position ===
    norm_alt = altitudes[frame]
    y_pos_raw = HEIGHT - int(norm_alt * (HEIGHT - 50))
    y_pos = min(HEIGHT - rocket_height, y_pos_raw)
    pygame.draw.rect(screen, RED, (WIDTH // 2 - rocket_width // 2, y_pos, rocket_width, rocket_height))

    # === Fuel Percentage ===
    current_mass = log_df["Mass"].iloc[frame]
    fuel_percent = max(0, (current_mass - m_final) / (m_initial - m_final))

    # === Draw Fuel Gauge ===
    pygame.draw.rect(screen, GRAY, (FUEL_X, FUEL_Y, FUEL_WIDTH, FUEL_HEIGHT))  # background
    fuel_fill_height = int(FUEL_HEIGHT * fuel_percent)
    pygame.draw.rect(screen, GREEN, (
        FUEL_X,
        FUEL_Y + (FUEL_HEIGHT - fuel_fill_height),
        FUEL_WIDTH,
        fuel_fill_height
    ))

    # === Update Display ===
    pygame.display.flip()
    clock.tick(30)

    # === Print Terminal Log ===
    log = log_df.iloc[frame]
    print(f"""
Time: {log['Time']:.2f}s | Mass: {log['Mass']:.3f}kg | Thrust: {log['Thrust']:.2f}N
Weight: {log['Weight']:.2f}N | Drag: {log['Drag']:.2f}N | Net Force: {log['Net Force']:.2f}N
Accel: {log['Acceleration']:.2f}m/s² | Vel: {log['Velocity']:.2f}m/s | Alt: {log['Altitude']:.2f}m
Fuel: {fuel_percent * 100:.1f}%
{"-"*60}
""")

    frame += 1

pygame.quit()
