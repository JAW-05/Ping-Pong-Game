import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants and Variables
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

# Font Sizes
START_FONT_SIZE = 20  
SCOREBOARD_FONT_SIZE = 40  
WINNING_FONT_SIZE = 30  

# Load the retro font with error handling
FONT_PATH = 'PressStart2P-Regular.ttf'  

try:
    start_font = pygame.font.Font(FONT_PATH, START_FONT_SIZE)
    scoreboard_font = pygame.font.Font(FONT_PATH, SCOREBOARD_FONT_SIZE)
    winning_font = pygame.font.Font(FONT_PATH, WINNING_FONT_SIZE)
except FileNotFoundError:
    print(f"Font not found at {FONT_PATH}, using default font.")
    start_font = pygame.font.Font(None, START_FONT_SIZE)
    scoreboard_font = pygame.font.Font(None, SCOREBOARD_FONT_SIZE)
    winning_font = pygame.font.Font(None, WINNING_FONT_SIZE)

# Load sounds
pygame.mixer.music.load('8bit.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

BOUNCEFX = pygame.mixer.Sound('bounce.mp3')
WINFX = pygame.mixer.Sound('score.mp3')

# Winning score
WINNING_SCORE = 10

# Opening Screen Function
def show_opening_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                intro = False  # Exit the intro loop on any key press
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

        WIN.fill(BLACK)  

        # Render text for the opening screen
        title_text = start_font.render("Ping Pong", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        WIN.blit(title_text, title_rect)
        
        instruction_text1 = start_font.render("Player 1: W/S keys", True, WHITE)
        instruction_rect1 = instruction_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        WIN.blit(instruction_text1, instruction_rect1)
        
        instruction_text2 = start_font.render("Player 2: Up/Down keys", True, WHITE)
        instruction_rect2 = instruction_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
        WIN.blit(instruction_text2, instruction_rect2)
        
        quit_instruction = start_font.render("Q - Quit", True, WHITE)
        quit_rect = quit_instruction.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        WIN.blit(quit_instruction, quit_rect)

        start_text = start_font.render("Click any key to start :)", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        WIN.blit(start_text, start_rect)
        
        pygame.display.update()

# Paddle Class
class Paddle:
    COLOR = BLUE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# Ball Class
class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

# Function to draw game elements
def draw_game(win, left_paddle, right_paddle, ball, left_score, right_score):
    win.fill(BLACK)  

    # Draw midline
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, RED, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    # Draw paddles and ball
    left_paddle.draw(win)
    right_paddle.draw(win)
    ball.draw(win)

    # Draw scores
    left_score_text = scoreboard_font.render(f"{left_score}", True, WHITE)
    right_score_text = scoreboard_font.render(f"{right_score}", True, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    pygame.display.update()

# Function to handle collisions
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

                pygame.mixer.Sound.play(BOUNCEFX)  

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

                pygame.mixer.Sound.play(BOUNCEFX)  

# Function to handle paddle movement
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

# Function to update game logic
def update_game(left_paddle, right_paddle, ball, left_score, right_score):
    ball.move()
    handle_collision(ball, left_paddle, right_paddle)

    # Check if the ball goes out of bounds (scoring)
    if ball.x < 0:
        right_score += 1
        ball.reset()
        pygame.mixer.Sound.play(WINFX)  

    elif ball.x > WIDTH:
        left_score += 1
        ball.reset()
        pygame.mixer.Sound.play(WINFX)  
    # Check if a player has won
    if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
        return True, left_score, right_score  # Game over

    return False, left_score, right_score  # Game continues

# Function to show game over screen with centered text and buttons
def show_game_over_screen(win_text):
    button_font = pygame.font.Font(FONT_PATH, 20)
    retry_button = pygame.Rect(0, 0, 200, 50)
    quit_button = pygame.Rect(0, 0, 200, 50)
    
    retry_button.center = (WIDTH // 2, HEIGHT // 2 + 40)
    quit_button.center = (WIDTH // 2, HEIGHT // 2 + 100)

    while True:
        WIN.fill(BLACK)
        
        text = winning_font.render(win_text, True, WHITE)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 60))

        pygame.draw.rect(WIN, BLUE, retry_button)
        pygame.draw.rect(WIN, RED, quit_button)
        
        retry_text = button_font.render("Retry", True, WHITE)
        WIN.blit(retry_text, (retry_button.x + (retry_button.width - retry_text.get_width()) // 2, retry_button.y + (retry_button.height - retry_text.get_height()) // 2))

        quit_text = button_font.render("Quit", True, WHITE)
        WIN.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2, quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return "retry"
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main function
def main():
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    show_opening_screen()  

    while True:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            game_over, left_score, right_score = update_game(left_paddle, right_paddle, ball, left_score, right_score)
            if game_over:
                if left_score >= WINNING_SCORE:
                    result = show_game_over_screen("Left Player Won!")
                elif right_score >= WINNING_SCORE:
                    result = show_game_over_screen("Right Player Won!")
                
                if result == "retry":
                    left_score = 0
                    right_score = 0
                    left_paddle.reset()
                    right_paddle.reset()
                    break  # Exit the inner game loop and restart
                else:
                    pygame.quit()
                    sys.exit()
    
            draw_game(WIN, left_paddle, right_paddle, ball, left_score, right_score)

            clock.tick(FPS)

if __name__ == '__main__':
    main()
