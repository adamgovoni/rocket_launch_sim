# NOTE: Displays in feet, screen follows rocket up, no fixed altitude ruler

import pygame
import random
import math
import time as systime

# === Pygame Setup ===
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Rocket Simulator (Feet, Follow Mode)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)

# === Sound ===
try:
    explosion_sound = pygame.mixer.Sound("explosion.wav")
except:
    explosion_sound = None

# === Colors ===
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
CYAN = (0, 255, 255)

# === Rocket Parameters ===
m0 = 3.0
mf = 1.0
thrust = 400.0
burn_time = 12
base_drag_coef = 0.03
g = 9.81
dt = 0.033
mass_loss_rate = (m0 - mf) / burn_time

# === Air Density Model ===
def air_density(alt_m):
    rho0 = 1.225
    scale_height = 8500.0
    return rho0 * math.exp(-alt_m / scale_height)

# === Countdown ===
def countdown():
    for i in reversed(range(1, 4)):
        screen.fill(BLACK)
        text = font.render(f"{i}...", True, WHITE)
        screen.blit(text, (WIDTH//2 - 30, HEIGHT//2))
        pygame.display.flip()
        systime.sleep(1)
    ignite = font.render("IGNITION!", True, ORANGE)
    screen.fill(BLACK)
    screen.blit(ignite, (WIDTH//2 - 100, HEIGHT//2))
    pygame.display.flip()
    systime.sleep(1)

# === Explosion Particles ===
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(-math.pi, 0)
        self.speed = random.uniform(3, 9)
        self.radius = random.randint(3, 8)
        self.life = random.randint(40, 70)
        self.color = random.choice([ORANGE, YELLOW, RED, WHITE])
        self.gravity = 0.15
        self.dy = 0
        self.angle = angle

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle) + self.dy
        self.dy += self.gravity
        self.life -= 1

    def draw(self, surface, offset_y):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y - offset_y)), self.radius)
        elif self.life > -30:
            pygame.draw.circle(surface, GRAY, (int(self.x), int(self.y - offset_y)), self.radius)

    def is_alive(self):
        return self.life > -30

# === Begin Simulation ===
countdown()
rocket_width, rocket_height = 24, 50
rocket_x = WIDTH // 2 - rocket_width // 2
flame_height = 22

time = 0
velocity = 0
altitude = 0
mass = m0

positions, velocities, accelerations = [], [], []

running = True
while altitude >= 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    positions.append(altitude)
    velocities.append(velocity)

    if time < burn_time:
        F_thrust = thrust
        mass -= mass_loss_rate * dt
    else:
        F_thrust = 0

    rho = air_density(altitude)
    F_gravity = mass * g
    F_drag = rho * base_drag_coef * velocity**2 if velocity > 0 else 0
    F_net = F_thrust - F_gravity - F_drag
    acceleration = F_net / mass
    accelerations.append(acceleration)

    velocity += acceleration * dt
    altitude += velocity * dt
    time += dt

    # === Draw Frame ===
    screen.fill(BLACK)
    rocket_y_screen = HEIGHT // 2
    ground_y_world = 0
    offset_y = altitude * 3.28084 - rocket_y_screen  # rocket centered on screen

    pygame.draw.rect(screen, RED, (rocket_x, rocket_y_screen, rocket_width, rocket_height))

    if time < burn_time:
        flicker = random.randint(-4, 4)
        pygame.draw.polygon(screen, ORANGE, [
            (rocket_x, rocket_y_screen + rocket_height),
            (rocket_x + 6, rocket_y_screen + rocket_height),
            (rocket_x + 3, rocket_y_screen + rocket_height + flame_height + flicker)
        ])
        pygame.draw.polygon(screen, ORANGE, [
            (rocket_x + rocket_width - 6, rocket_y_screen + rocket_height),
            (rocket_x + rocket_width, rocket_y_screen + rocket_height),
            (rocket_x + rocket_width - 3, rocket_y_screen + rocket_height + flame_height + flicker)
        ])
        pygame.draw.polygon(screen, YELLOW, [
            (rocket_x + 1, rocket_y_screen + rocket_height),
            (rocket_x + 5, rocket_y_screen + rocket_height),
            (rocket_x + 3, rocket_y_screen + rocket_height + 10 + flicker)
        ])
        pygame.draw.polygon(screen, YELLOW, [
            (rocket_x + rocket_width - 5, rocket_y_screen + rocket_height),
            (rocket_x + rocket_width - 1, rocket_y_screen + rocket_height),
            (rocket_x + rocket_width - 3, rocket_y_screen + rocket_height + 10 + flicker)
        ])

    hud_lines = [
        f"ALT: {altitude * 3.28084:.1f} ft",
        f"VEL: {velocity * 3.28084:.1f} ft/s",
        f"ACC: {acceleration * 3.28084:.1f} ft/s²",
        f"THRUST: {F_thrust:.1f} N",
        f"MASS: {mass:.2f} kg",
        f"AIR: {rho:.3f} kg/m³",
        f"TIME: {time:.2f} s"
    ]
    for i, line in enumerate(hud_lines):
        text = font.render(line, True, CYAN)
        screen.blit(text, (WIDTH - 300, 40 + i * 30))

    pygame.display.flip()
    clock.tick(30)

# === Explosion ===
if explosion_sound:
    explosion_sound.play()
particles = [Particle(WIDTH // 2, HEIGHT - 20 + offset_y) for _ in range(120)]
while any(p.is_alive() for p in particles):
    screen.fill(BLACK)
    for p in particles:
        p.update()
        p.draw(screen, offset_y)
    pygame.display.flip()
    clock.tick(60)

# === Mission Summary ===
screen.fill(BLACK)
max_alt = max(positions)
impact_velocity = velocities[-1]
total_time = time
summary = [
    f"Max Altitude: {max_alt * 3.28084:.2f} ft",
    f"Impact Velocity: {impact_velocity * 3.28084:.2f} ft/s",
    f"Flight Duration: {total_time:.2f} s",
    "Click to Exit"
]
for i, line in enumerate(summary):
    text = font.render(line, True, WHITE)
    screen.blit(text, (WIDTH//2 - 220, HEIGHT//2 + i * 30))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            waiting = False

pygame.quit()
