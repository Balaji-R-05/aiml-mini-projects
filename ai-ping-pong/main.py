import pygame   # Game development library
import random   # Random number generation library
import time     # Time library for sleep function

# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Game constants
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Winning score
WINNING_SCORE = 5



class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PADDLE_SPEED

    def ai_move(self, ball):
        """ AI moves the paddle to follow the ball """
        if ball.rect.centery < self.rect.centery:
            self.move_up()
        elif ball.rect.centery > self.rect.centery:
            self.move_down()

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_WHITE, self.rect)



class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2,
                                SCREEN_HEIGHT//2 - BALL_SIZE//2,
                                BALL_SIZE, BALL_SIZE)
        self.reset()

    def reset(self):
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

    def bounce(self):
        self.speed_x *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, COLOR_WHITE, self.rect)


def draw_center_line(screen):
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, COLOR_WHITE, (SCREEN_WIDTH//2 - 2, y, 4, 20))


def main():
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ping Pong")

    # Set up fonts
    font = pygame.font.SysFont(None, 60)
    winner_font = pygame.font.SysFont(None, 80)

    # Create paddles and ball
    left_paddle = Paddle(50, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2)
    right_paddle = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2)
    ball = Ball()

    clock = pygame.time.Clock()

    left_score = 0
    right_score = 0

    paused = False


    running = True
    while running:
        clock.tick(60)
        screen.fill(COLOR_BLACK)
        draw_center_line(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pause toggle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        keys = pygame.key.get_pressed()
        if not paused:
            # Left paddle control (AI-controlled)
            left_paddle.ai_move(ball)

            # Right paddle control (player-controlled)
            if keys[pygame.K_UP]:
                right_paddle.move_up()
            if keys[pygame.K_DOWN]:
                right_paddle.move_down()

            # Ball movement
            ball.move()

            # Collision with paddles
            if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
                ball.bounce()

            # Scoring
            if ball.rect.left <= 0:
                right_score += 1
                ball.reset()
            elif ball.rect.right >= SCREEN_WIDTH:
                left_score += 1
                ball.reset()


        # Winning logic
        if left_score == WINNING_SCORE:
            winner_text = winner_font.render("AI Wins!", True, COLOR_WHITE)
            screen.blit(winner_text, (SCREEN_WIDTH//2 - winner_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
            pygame.display.flip()
            time.sleep(3)
            left_score, right_score = 0, 0
            ball.reset()
            paused = True

        elif right_score == WINNING_SCORE:
            winner_text = winner_font.render("Player Wins!", True, COLOR_WHITE)
            screen.blit(winner_text, (SCREEN_WIDTH//2 - winner_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
            pygame.display.flip()
            time.sleep(3)
            left_score, right_score = 0, 0
            ball.reset()
            paused = True

        # Draw everything
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        # Draw score
        left_text = font.render(str(left_score), True, COLOR_WHITE)
        right_text = font.render(str(right_score), True, COLOR_WHITE)
        screen.blit(left_text, (SCREEN_WIDTH//4, 20))
        screen.blit(right_text, (SCREEN_WIDTH*3//4, 20))

        # Draw outer border
        pygame.draw.rect(screen, COLOR_WHITE, screen.get_rect(), 4)

        # Draw pause text
        if paused:
            pause_text = font.render("PAUSED", True, COLOR_WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - 100))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()