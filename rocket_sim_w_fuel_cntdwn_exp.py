import pygame
import random
import math
import time as systime

# === Pygame Setup ===
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Calculus Rocket Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)

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

# === Rocket Parameters ===
m0 = 2.5       # initial mass
mf = 1.0       # final mass after fuel burn
thrust = 250.0  # Newtons
drag_coef = 0.05
burn_time = 7
mass_loss_rate = (m0 - mf) / burn_time
g = 9.81
dt = 0.033

# === Simulation State ===
time = 0
velocity = 0
altitude = 0
mass = m0
positions = []
times = []
velocities = []

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

# === Particle Explosion ===
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(-math.pi, 0)
        self.speed = random.uniform(2, 7)
        self.radius = random.randint(3, 7)
        self.life = random.randint(40, 70)
        self.color = random.choice([ORANGE, YELLOW, RED, WHITE])
        self.gravity = 0.1
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

# === Rocket Setup ===
rocket_width = 14
rocket_height = 40
rocket_x = WIDTH // 2 - rocket_width // 2
smoke_trail = []

# === Main Simulation Loop ===
running = True
exploded = False
max_display_alt = 1000  # meters for altitude scaling

while running and altitude >= 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    times.append(time)
    positions.append(altitude)
    velocities.append(velocity)

    # Physics Calculations
    if time < burn_time:
        F_thrust = thrust
        mass -= mass_loss_rate * dt
    else:
        F_thrust = 0

    F_gravity = mass * g
    F_drag = drag_coef * velocity**2 if velocity > 0 else 0
    F_net = F_thrust - F_gravity - F_drag
    acceleration = F_net / mass
    velocity += acceleration * dt
    altitude += velocity * dt
    time += dt

    # === Drawing ===
    screen.fill(BLACK)
    
    # Altitude bar
    bar_height = 400
    alt_bar_x = 30
    pygame.draw.rect(screen, WHITE, (alt_bar_x, 100, 10, bar_height))
    alt_marker_y = 100 + int(bar_height * (1 - min(altitude / max_display_alt, 1)))
    pygame.draw.rect(screen, GREEN, (alt_bar_x - 3, alt_marker_y - 5, 16, 10))
    label = font.render(f"{int(altitude)}m", True, GREEN)
    screen.blit(label, (alt_bar_x + 20, alt_marker_y - 10))

    # Rocket Position
    norm_alt = min(1.0, altitude / max_display_alt)
    rocket_y = HEIGHT - int(norm_alt * (HEIGHT - 100)) - rocket_height

    # Smoke Trail
    if velocity > 1:
        smoke_trail.append((rocket_x + rocket_width // 2, rocket_y + rocket_height, random.randint(4, 7)))
    smoke_trail = smoke_trail[-80:]  # keep last N smoke puffs
    for sx, sy, r in smoke_trail:
        pygame.draw.circle(screen, GRAY, (sx + random.randint(-3, 3), sy + random.randint(0, 3)), r)

    # Rocket Body
    pygame.draw.rect(screen, RED, (rocket_x, rocket_y, rocket_width, rocket_height))

    # Flame
    if F_thrust > 0:
        flicker = random.randint(-3, 3)
        pygame.draw.polygon(screen, ORANGE, [
            (rocket_x, rocket_y + rocket_height),
            (rocket_x + rocket_width, rocket_y + rocket_height),
            (rocket_x + rocket_width // 2, rocket_y + rocket_height + 18 + flicker)
        ])
        pygame.draw.polygon(screen, YELLOW, [
            (rocket_x + 2, rocket_y + rocket_height),
            (rocket_x + rocket_width - 2, rocket_y + rocket_height),
            (rocket_x + rocket_width // 2, rocket_y + rocket_height + 10 + flicker)
        ])

    pygame.display.flip()
    clock.tick(30)

# === Explosion ===
if explosion_sound:
    explosion_sound.play()
particles = [Particle(WIDTH // 2, HEIGHT - 20) for _ in range(120)]
while particles:
    screen.fill(BLACK)
    for p in particles:
        p.update()
        p.draw(screen)
    particles = [p for p in particles if p.is_alive()]
    pygame.display.flip()
    clock.tick(60)

# === Stats ===
max_alt = max(positions)
impact_velocity = velocities[-1]
total_time = times[-1]

screen.fill(BLACK)
lines = [
    f"Max Altitude: {max_alt:.2f} m",
    f"Impact Velocity: {impact_velocity:.2f} m/s",
    f"Flight Duration: {total_time:.2f} s",
    "Click to Exit"
]
for i, line in enumerate(lines):
    text = font.render(line, True, WHITE)
    screen.blit(text, (WIDTH // 2 - 160, HEIGHT // 2 + i * 30))
pygame.display.flip()

# === Wait for Exit ===
wait = True
while wait:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            wait = False
pygame.quit()
