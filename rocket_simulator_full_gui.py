import pygame
import random
import math
import time as systime

# === Pygame Setup ===
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Calculus Rocket Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

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
GRAY = (120, 120, 120)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)

# === Rocket Parameters ===
m0 = 2.5       # initial mass (kg)
mf = 1.0       # final mass after fuel burn (kg)
thrust = 220.0 # Newtons
burn_time = 10 # seconds
drag_coef = 0.05
mass_loss_rate = (m0 - mf) / burn_time
g = 9.81
dt = 0.033
max_display_alt = 1500  # meters

# === Simulation State ===
time = 0
velocity = 0
altitude = 0
mass = m0
positions = []
times = []
velocities = []
accelerations = []

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

# === Particle for Explosion ===
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(-3 * math.pi / 4, -math.pi / 4)
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

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        elif self.life > -30:
            pygame.draw.circle(surface, GRAY, (int(self.x), int(self.y)), self.radius)

    def is_alive(self):
        return self.life > -30

# === Run Countdown ===
countdown()

# === Simulate Flight with Visuals ===
rocket_width, rocket_height = 12, 35
flame_height = 20

running = True
exploded = False

while altitude >= 0:
    times.append(time)
    positions.append(altitude)
    velocities.append(velocity)

    if time < burn_time:
        F_thrust = thrust
        mass -= mass_loss_rate * dt
    else:
        F_thrust = 0

    F_gravity = mass * g
    F_drag = drag_coef * velocity**2 if velocity > 0 else 0
    F_net = F_thrust - F_gravity - F_drag

    acceleration = F_net / mass
    accelerations.append(acceleration)

    velocity += acceleration * dt
    altitude += velocity * dt
    time += dt

    # === Draw ===
    screen.fill(BLACK)

    # Draw vertical ruler
    for a in range(0, max_display_alt + 1, 100):
        y = HEIGHT - int((a / max_display_alt) * (HEIGHT - 100))
        pygame.draw.line(screen, GRAY, (50, y), (60, y), 2)
        text = font.render(f"{a}m", True, WHITE)
        screen.blit(text, (10, y - 10))

    # Rocket position
    norm_alt = min(1.0, altitude / max_display_alt)
    rocket_x = WIDTH // 2
    rocket_y = HEIGHT - int(norm_alt * (HEIGHT - 100)) - rocket_height
    pygame.draw.rect(screen, RED, (rocket_x, rocket_y, rocket_width, rocket_height))

    # Flame
    if time < burn_time:
        flicker = random.randint(-3, 3)
        pygame.draw.polygon(screen, ORANGE, [
            (rocket_x, rocket_y + rocket_height),
            (rocket_x + rocket_width, rocket_y + rocket_height),
            (rocket_x + rocket_width // 2, rocket_y + rocket_height + flame_height + flicker)
        ])
        pygame.draw.polygon(screen, YELLOW, [
            (rocket_x + 2, rocket_y + rocket_height),
            (rocket_x + rocket_width - 2, rocket_y + rocket_height),
            (rocket_x + rocket_width // 2, rocket_y + rocket_height + 10 + flicker)
        ])

    # Speedometer
    speed_text = font.render(f"Speed: {velocity:.1f} m/s", True, CYAN)
    screen.blit(speed_text, (WIDTH - 250, 30))

    pygame.display.flip()
    clock.tick(30)

# === Explosion ===
if explosion_sound:
    explosion_sound.play()

particles = [Particle(WIDTH//2, HEIGHT - 20) for _ in range(120)]
while any(p.is_alive() for p in particles):
    screen.fill(BLACK)
    for p in particles:
        p.update()
        p.draw(screen)
    pygame.display.flip()
    clock.tick(60)

# === Show Stats ===
max_alt = max(positions)
impact_velocity = velocities[-1]
total_time = times[-1]

screen.fill(BLACK)
stats = [
    f"Max Altitude: {max_alt:.2f} m",
    f"Impact Velocity: {impact_velocity:.2f} m/s",
    f"Flight Duration: {total_time:.2f} s",
    "Click to Exit"
]
for i, line in enumerate(stats):
    text = font.render(line, True, WHITE)
    screen.blit(text, (WIDTH//2 - 200, HEIGHT//2 + i * 30))
pygame.display.flip()

# === Wait for Exit ===
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            waiting = False

pygame.quit()
