import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BALLOON_COLORS = [RED, GREEN, BLUE, YELLOW]
TARGET_COLOR = RED  # Target color to tap

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Tapping Game")

# Fonts
font = pygame.font.SysFont("Arial", 30)

def display_message(text, x, y, color=BLACK):
    """Display text on the screen"""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, 50, 70])
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y -= self.speed  # Move balloon up
        if self.rect.bottom < 0:  # Reset balloon when it moves off screen
            self.rect.y = HEIGHT + random.randint(10, 100)
            self.rect.x = random.randint(50, WIDTH - 50)
            self.color = random.choice(BALLOON_COLORS)

# Initialize sprite groups
balloon_group = pygame.sprite.Group()

# Create balloons
for _ in range(10):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(HEIGHT // 2, HEIGHT)
    color = random.choice(BALLOON_COLORS)
    balloon = Balloon(x, y, color)
    balloon_group.add(balloon)

def main():
    clock = pygame.time.Clock()
    score = 0
    running = True

    # Determine target color name
    target_color_name = "RED" if TARGET_COLOR == RED else "UNKNOWN"

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for balloon in balloon_group:
                    if balloon.rect.collidepoint(pos):
                        if balloon.color == TARGET_COLOR:
                            score += 1  # Correct balloon tapped
                        else:
                            score -= 1  # Incorrect balloon tapped
                        # Reset balloon position
                        balloon.rect.y = HEIGHT + random.randint(10, 100)
                        balloon.rect.x = random.randint(50, WIDTH - 50)

        # Update
        balloon_group.update()

        # Draw
        balloon_group.draw(screen)
        display_message(f"Score: {score}", 10, 10)
        display_message(f"Tap {target_color_name} balloons!", 10, 50, TARGET_COLOR)

        # Refresh screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
