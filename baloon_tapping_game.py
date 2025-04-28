import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

BALLOON_COLORS = [RED, GREEN, BLUE, YELLOW]
TARGET_COLOR = RED  


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Tapping Game")


font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 20)


game_running = False
in_menu = True
game_speed = 60
time_limit = 30  
time_left = time_limit  
paused = False  
correct_taps = 0
total_target_color_balloons = 0
score = 0
start_ticks = None

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
        pygame.time.wait(200)

def game_menu():
    """Game menu interface"""
    global game_speed, in_menu, game_running, TARGET_COLOR
    in_menu = True
    while in_menu:
        screen.fill(WHITE)
        display_message("Balloon Tapping Game - Menu", WIDTH // 2 - 200, HEIGHT // 4)

        button("Play", WIDTH // 2 - 75, HEIGHT // 2 - 120, 150, 50, GRAY, GREEN, start_game)
        button("Speed: Slow", WIDTH // 2 - 75, HEIGHT // 2 - 60, 150, 50, GRAY, BLUE, set_speed_slow)
        button("Speed: Normal", WIDTH // 2 - 75, HEIGHT // 2, 150, 50, GRAY, BLUE, set_speed_normal)
        button("Speed: Fast", WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50, GRAY, BLUE, set_speed_fast)
        button("Quit", WIDTH // 2 - 75, HEIGHT // 2 + 120, 150, 50, GRAY, RED, quit_game)

        
        button("Target: Red", WIDTH // 2 - 75, HEIGHT // 2 + 180, 150, 50, RED, RED, set_target_red)
        button("Target: Green", WIDTH // 2 - 75, HEIGHT // 2 + 240, 150, 50, GREEN, GREEN, set_target_green)
        button("Target: Blue", WIDTH // 2 - 75, HEIGHT // 2 + 300, 150, 50, BLUE, BLUE, set_target_blue)
        button("Target: Yellow", WIDTH // 2 - 75, HEIGHT // 2 + 360, 150, 50, YELLOW, YELLOW, set_target_yellow)

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

def set_target_red():
    global TARGET_COLOR
    TARGET_COLOR = RED

def set_target_green():
    global TARGET_COLOR
    TARGET_COLOR = GREEN

def set_target_blue():
    global TARGET_COLOR
    TARGET_COLOR = BLUE

def set_target_yellow():
    global TARGET_COLOR
    TARGET_COLOR = YELLOW

def start_game():
    global in_menu, game_running, time_left, paused, correct_taps, total_target_color_balloons, score, start_ticks
    game_running = True
    in_menu = False
    time_left = time_limit
    paused = False
    correct_taps = 0
    total_target_color_balloons = 0
    score = 0
    start_ticks = pygame.time.get_ticks()

def quit_game():
    pygame.quit()
    sys.exit()

class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, 50, 70])
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.speed = random.randint(2, 5)

    def update(self):
        if game_running and not paused:
            self.rect.y -= self.speed  
            if self.rect.bottom < 0:  
                self.reset_balloon()

    def reset_balloon(self):
        """Reset balloon position and color."""
        self.rect.y = HEIGHT + random.randint(10, 100)
        self.rect.x = random.randint(50, WIDTH - 50)
        self.color = random.choice(BALLOON_COLORS)
        if self.color == TARGET_COLOR: 
            global total_target_color_balloons
            total_target_color_balloons += 1 
        self.image.fill((0, 0, 0, 0))  
        pygame.draw.ellipse(self.image, self.color, [0, 0, 50, 70])


balloon_group = pygame.sprite.Group()


for _ in range(10):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(HEIGHT // 2, HEIGHT)
    color = random.choice(BALLOON_COLORS)
    balloon = Balloon(x, y, color)
    balloon_group.add(balloon)

def main():
    global game_speed, game_running, in_menu, time_left, paused, TARGET_COLOR, correct_taps, total_target_color_balloons, score, start_ticks
    clock = pygame.time.Clock()
    game_speed = 60  

    
    target_color_name = "RED" if TARGET_COLOR == RED else "UNKNOWN"
    if TARGET_COLOR == GREEN:
        target_color_name = "GREEN"
    elif TARGET_COLOR == BLUE:
        target_color_name = "BLUE"
    elif TARGET_COLOR == YELLOW:
        target_color_name = "YELLOW"

    while True:
        if in_menu:
            game_menu()  

        while game_running:
            screen.fill(WHITE)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for balloon in balloon_group:
                        if balloon.rect.collidepoint(pos):
                            if balloon.color == TARGET_COLOR:
                                score += 1  
                                correct_taps += 1  
                            else:
                                score -= 1  
                            balloon.reset_balloon() 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  
                        if not paused:
                            pause_game()
                        else:
                            resume_game()

            
            balloon_group.update()

            
            if not paused:
                seconds = (pygame.time.get_ticks() - start_ticks) // 1000
                time_left = max(0, time_limit - seconds)

            
            display_message(f"Time Left: {time_left}s", 20, 20, BLACK)
            display_message(f"Score: {score}", WIDTH - 150, 20, BLACK)
            display_message(f"Target Color: {target_color_name}", 20, HEIGHT - 40, BLACK)
            display_message(f"Correct Taps: {correct_taps}", WIDTH // 2 - 100, HEIGHT // 2 - 30, BLACK)
            display_message(f"Total Target Color Balloons: {total_target_color_balloons}", WIDTH // 2 - 150, HEIGHT // 2, BLACK)

            
            balloon_group.draw(screen)

            pygame.display.update()
            clock.tick(game_speed)

def pause_game():
    global paused
    paused = True
    display_message("Game Paused", WIDTH // 2 - 100, HEIGHT // 3, RED)
    display_message("Press 'R' to resume", WIDTH // 2 - 150, HEIGHT // 3 + 50, BLACK)
    pygame.display.update()

def resume_game():
    global paused
    paused = False
    global start_ticks
    start_ticks = pygame.time.get_ticks() - (time_limit - time_left) * 1000  # Update start_ticks to continue from where it left off


if __name__ == "__main__":
    main()
