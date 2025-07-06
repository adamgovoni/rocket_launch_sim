import pygame
import pandas as pd

# === Load Flight & Log Data ===
flight_df = pd.read_csv("rocket_flight_data_for_pygame.csv")
log_df = pd.read_csv("rocket_terminal_log.csv")
altitudes = flight_df["Altitude"].values

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Rocket Launch Visual Simulator")
clock = pygame.time.Clock()

# === Rocket Visuals ===
rocket_width = 10
rocket_height = 30
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# === Main Loop ===
running = True
frame = 0
frames_total = len(altitudes)

while running and frame < frames_total:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # === Clear Screen ===
    screen.fill(BLACK)

    # === Get Scaled Altitude and Clamp to Launch Pad ===
    norm_alt = altitudes[frame]
    y_pos_raw = HEIGHT - int(norm_alt * (HEIGHT - 50))
    y_pos = min(HEIGHT - rocket_height, y_pos_raw)  # prevent falling off the screen

    # === Draw Rocket ===
    pygame.draw.rect(screen, RED, (WIDTH // 2 - rocket_width // 2, y_pos, rocket_width, rocket_height))

    # === Display Frame ===
    pygame.display.flip()
    clock.tick(30)

    # === Print Terminal Log ===
    log = log_df.iloc[frame]
    print(f"""
Time: {log['Time']:.2f}s | Mass: {log['Mass']:.3f}kg | Thrust: {log['Thrust']:.2f}N
Weight: {log['Weight']:.2f}N | Drag: {log['Drag']:.2f}N | Net Force: {log['Net Force']:.2f}N
Accel: {log['Acceleration']:.2f}m/s² | Vel: {log['Velocity']:.2f}m/s | Alt: {log['Altitude']:.2f}m
{"-"*60}
""")

    frame += 1

pygame.quit()
