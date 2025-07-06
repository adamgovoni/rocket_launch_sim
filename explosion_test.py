import pygame
import random
import time as systime
import math

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Epic Explosion Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 36)

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
GRAY = (150, 150, 150)

# === Rocket ===
rocket_width = 12
rocket_height = 35
rocket_x = WIDTH // 2 - rocket_width // 2
rocket_y = HEIGHT - rocket_height - 20

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

# === Particle Class ===
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Bias the explosion more upward (reduce downward angle weight)
        angle_range = (-3 * math.pi / 4, -math.pi / 4)
        self.angle = random.uniform(*angle_range)
        self.speed = random.uniform(3, 9)
        self.radius = random.randint(3, 8)
        self.life = random.randint(40, 70)
        self.color = random.choice([ORANGE, YELLOW, RED, WHITE])
        self.gravity = 0.15
        self.dy = 0

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

# === Main ===
countdown()

# Draw rocket on pad
screen.fill(BLACK)
pygame.draw.rect(screen, RED, (rocket_x, rocket_y, rocket_width, rocket_height))
pygame.display.flip()
systime.sleep(1.5)

# === Explosion ===
if explosion_sound:
    explosion_sound.play()

particles = [Particle(rocket_x + rocket_width // 2, rocket_y + rocket_height // 2) for _ in range(100)]
exploding = True

while exploding:
    screen.fill(BLACK)
    for p in particles:
        p.update()
        p.draw(screen)
    particles = [p for p in particles if p.is_alive()]

    pygame.display.flip()
    clock.tick(60)

    if not particles:
        exploding = False

# === Wait for Click to Exit ===
exit_text = font.render("Click to Exit", True, WHITE)
screen.blit(exit_text, (WIDTH//2 - 140, HEIGHT//2))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            waiting = False

pygame.quit()
