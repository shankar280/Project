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
GRAY = (200, 200, 200)

BALLOON_COLORS = [RED, GREEN, BLUE, YELLOW]
TARGET_COLOR = RED  # Target color to tap

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Tapping Game")

# Fonts
font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 20)

# Global Variables
game_running = False
in_menu = True
game_speed = 60

def display_message(text, x, y, color=BLACK):
    """Display text on the screen"""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def button(text, x, y, w, h, inactive_color, active_color, action=None):
    """Create an interactive button"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = active_color if x + w > mouse[0] > x and y + h > mouse[1] > y else inactive_color
    pygame.draw.rect(screen, color, (x, y, w, h))
    text_surf = small_font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)
    if click[0] == 1 and x + w > mouse[0] > x and y + h > mouse[1] > y and action is not None:
        action()
        pygame.time.wait(200)  # Prevent multiple clicks

def game_menu():
    """Game menu interface"""
    global game_speed, in_menu, game_running
    in_menu = True
    while in_menu:
        screen.fill(WHITE)
        display_message("Balloon Tapping Game - Menu", WIDTH // 2 - 200, HEIGHT // 4)

        button("Play", WIDTH // 2 - 75, HEIGHT // 2 - 60, 150, 50, GRAY, GREEN, start_game)
        button("Speed: Slow", WIDTH // 2 - 75, HEIGHT // 2, 150, 50, GRAY, BLUE, set_speed_slow)
        button("Speed: Normal", WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50, GRAY, BLUE, set_speed_normal)
        button("Speed: Fast", WIDTH // 2 - 75, HEIGHT // 2 + 120, 150, 50, GRAY, BLUE, set_speed_fast)
        button("Quit", WIDTH // 2 - 75, HEIGHT // 2 + 180, 150, 50, GRAY, RED, quit_game)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def set_speed_slow():
    global game_speed
    game_speed = 30

def set_speed_normal():
    global game_speed
    game_speed = 60

def set_speed_fast():
    global game_speed
    game_speed = 90

def start_game():
    global in_menu, game_running
    game_running = True
    in_menu = False  # Exit the menu

def quit_game():
    pygame.quit()
    sys.exit()

class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, 50, 70])
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color  # Keep track of balloon color
        self.speed = random.randint(2, 5)

    def update(self):
        if game_running:  # Only move balloons if game is running
            self.rect.y -= self.speed  # Move balloon up
            if self.rect.bottom < 0:  # Reset balloon when it moves off screen
                self.reset_balloon()

    def reset_balloon(self):
        """Reset balloon position and color."""
        self.rect.y = HEIGHT + random.randint(10, 100)
        self.rect.x = random.randint(50, WIDTH - 50)
        self.color = random.choice(BALLOON_COLORS)
        self.image.fill((0, 0, 0, 0))  # Clear previous drawing
        pygame.draw.ellipse(self.image, self.color, [0, 0, 50, 70])

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
    global game_speed, game_running, in_menu
    clock = pygame.time.Clock()
    score = 0
    game_speed = 60  # Default speed

    # Determine target color name
    target_color_name = "RED" if TARGET_COLOR == RED else "UNKNOWN"

    while True:
        if in_menu:
            game_menu()  # Show menu before the game starts

        while game_running:
            screen.fill(WHITE)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for balloon in balloon_group:
                        if balloon.rect.collidepoint(pos):
                            if balloon.color == TARGET_COLOR:
                                score += 1  # Correct balloon tapped
                            else:
                                score -= 1  # Incorrect balloon tapped
                            balloon.reset_balloon()  # Reset balloon position and color

            # Update
            balloon_group.update()

            # Draw
            balloon_group.draw(screen)
            display_message(f"Score: {score}", 10, 10)
            display_message(f"Tap {target_color_name} balloons!", 10, 50, TARGET_COLOR)
            button("Pause", WIDTH - 160, 10, 150, 50, GRAY, YELLOW, pause_game)

            # Refresh screen
            pygame.display.flip()
            clock.tick(game_speed)

        while not game_running:  # Pause state
            screen.fill(WHITE)
            display_message("Game Paused", WIDTH // 2 - 100, HEIGHT // 2 - 50)
            button("Resume", WIDTH // 2 - 75, HEIGHT // 2, 150, 50, GRAY, GREEN, resume_game)
            button("Quit", WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50, GRAY, RED, quit_game)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

def pause_game():
    global game_running
    game_running = False

def resume_game():
    global game_running
    game_running = True

if __name__ == "__main__":
    main()
