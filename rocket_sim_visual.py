import pygame
import pandas as pd
import time

# === Load flight data ===
df = pd.read_csv("rocket_flight_data_for_pygame.csv")
altitudes = df["Altitude"].values

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Rocket properties
rocket_width = 10
rocket_height = 30

# Main loop
running = True
frame = 0
while running and frame < len(altitudes):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Calculate rocket position
    norm_alt = altitudes[frame]
    y_pos = HEIGHT - int(norm_alt * (HEIGHT - 50))  # padding from top

    # Draw rocket
    pygame.draw.rect(screen, RED, (WIDTH//2 - rocket_width//2, y_pos, rocket_width, rocket_height))

    # Update display
    pygame.display.flip()
    clock.tick(60)
    frame += 1

pygame.quit()
