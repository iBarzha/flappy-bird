import pygame
import random
import sys

# Pygame initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BACKGROUND_COLOR = (255, 255, 255)
FPS = 60
GRAVITY = 0.25
BIRD_JUMP = -4
PIPE_VELOCITY = -2
GAP_SIZE = 150

# Creating a game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Uploading images
bird_img = pygame.image.load("bird.png").convert_alpha()
pipe_img = pygame.image.load("pipe.png").convert_alpha()
background_img = pygame.image.load("background.png").convert()

# A class for bird
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.image = bird_img
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def flap(self):
        self.velocity = BIRD_JUMP

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, 400)
        self.top_pipe = pygame.transform.flip(pipe_img, False, True)
        self.bottom_pipe = pipe_img
        self.passed = False
        self.set_position()

    def set_position(self):
        gap_center = random.randint(150, HEIGHT - 150)
        self.top_rect = self.top_pipe.get_rect(midbottom=(self.x, gap_center - GAP_SIZE // 2))
        self.bottom_rect = self.bottom_pipe.get_rect(midtop=(self.x, gap_center + GAP_SIZE // 2))

    def move(self):
        self.x += PIPE_VELOCITY
        self.top_rect.centerx = self.x
        self.bottom_rect.centerx = self.x

    def draw(self):
        screen.blit(self.top_pipe, self.top_rect)
        screen.blit(self.bottom_pipe, self.bottom_rect)

# Function for creating a new pipe
def create_pipe():
    pipes.append(Pipe(WIDTH + 100))

# Function for checking collisions
def check_collision(bird, pipes):
    if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return True
    return False

# Function to display the score
def display_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

#Initializing the game
bird = Bird()
pipes = []
create_pipe()
clock = pygame.time.Clock()
score = 0
game_over = False

#The main game cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.flap()
            elif event.key == pygame.K_SPACE and game_over:
                bird = Bird()
                pipes = []
                create_pipe()
                score = 0
                game_over = False
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Update game objects
    if not game_over:
        bird.update()
        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.top_pipe.get_width() < bird.x and not pipe.passed:
                pipe.passed = True
                score += 1
            if pipe.x < -100:
                pipes.remove(pipe)
                create_pipe()
        if check_collision(bird, pipes):
            game_over = True

    # Display of game objects
    screen.blit(background_img, (0, 0))
    bird.draw()
    for pipe in pipes:
        pipe.draw()
    display_score(score)
    if game_over:
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        font = pygame.font.Font(None, 24)
        restart_text = font.render("Press SPACE to Restart", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + restart_text.get_height()))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

