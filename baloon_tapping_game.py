import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Shooting Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load assets
font = pygame.font.Font(None, 36)

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, 40, 60])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 2
        if self.rect.bottom < 0:
            self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

# Groups
balloons = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Game variables
score = 0
spawn_timer = 0
running = True

# Main game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire bullet
            x, y = pygame.mouse.get_pos()
            bullet = Bullet(x, y)
            bullets.add(bullet)
            all_sprites.add(bullet)

    # Spawn balloons
    spawn_timer += 1
    if spawn_timer > 50:
        spawn_timer = 0
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = SCREEN_HEIGHT + 50
        color = random.choice([RED, GREEN, BLUE])
        balloon = Balloon(x, y, color)
        balloons.add(balloon)
        all_sprites.add(balloon)

    # Update
    all_sprites.update()

    # Check for collisions
    for bullet in bullets:
        hit_balloons = pygame.sprite.spritecollide(bullet, balloons, True)
        for balloon in hit_balloons:
            score += 1
            bullet.kill()

    # Draw
    all_sprites.draw(screen)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
