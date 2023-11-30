import pygame
import sys
import random

HEIGHT = 600
WIDTH = 900


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 64)

    def move(self, direction):
        if direction == "up" and self.rect.top > 0:
            self.rect.y -= 8

        if direction == "down" and self.rect.bottom < HEIGHT:
            self.rect.y += 8


class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed_x = 5 * random.choice((1, -1))
        self.speed_y = 5 * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collisions with walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.speed_x *= random.choice((1, -1))
        self.speed_y *= random.choice((1, -1))


class PingPongGame:
    def __init__(self):
        # Initialize Pygame, Pygame mixer, font
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()  # Initialize the font module
        pygame.display.set_caption("Ping Pong")  # Screen Title

        # Initialize Sound Files
        self.waiting_to_start = pygame.mixer.Sound("waiting_to_start.wav")
        self.game_start = pygame.mixer.Sound("game_start.wav")
        self.collision_sound = pygame.mixer.Sound("ball_hit.wav")
        self.score_sound = pygame.mixer.Sound("score_sound.wav")

        # Window Properties
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.GAME_COLORS = [(0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 255, 0)]

        # Initialize scores
        self.left_score = 0
        self.right_score = 0

        self.left_paddle = Paddle(0, (self.HEIGHT - 60) // 2)
        self.right_paddle = Paddle(self.WIDTH - 10, (self.HEIGHT - 60) // 2)
        self.ball = Ball(self.WIDTH // 2, self.HEIGHT // 2)

        # Set up game state
        self.game_started = False

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def start_menu(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Press Okay to Start the game", True, self.GAME_COLORS[3])
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        self.SCREEN.fill(self.GAME_COLORS[0])
        self.SCREEN.blit(text, text_rect)

        pygame.display.flip()

        waiting_to_start = True
        while waiting_to_start:
            self.waiting_to_start.play()  # Start the start sound
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.waiting_to_start.stop()  # Stop waiting to start sound
                    waiting_to_start = False
                    self.game_started = True  # Set game to start
                    self.game_start.play()  # Play game start sound

    def continue_menu(self):

        font = pygame.font.Font(None, 36)
        text = font.render("Press C to continue or Q to quit", True, self.GAME_COLORS[3])
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        self.SCREEN.fill(self.GAME_COLORS[0])
        self.SCREEN.blit(text, text_rect)
        pygame.display.flip()

        waiting_for_continue = True
        while waiting_for_continue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        waiting_for_continue = False
                        self.game_start.play()  # Play the start sound
                        self.reset_game()  # Reset game
                        self.game_started = True  # Set game to restart
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def reset_game(self):
        self.left_score = 0
        self.right_score = 0
        self.ball.reset()

    def draw(self):
        self.SCREEN.fill(self.GAME_COLORS[0])  # Black background

        # Draw Paddles and ball
        pygame.draw.rect(self.SCREEN, self.GAME_COLORS[1], self.left_paddle.rect)
        pygame.draw.rect(self.SCREEN, self.GAME_COLORS[1], self.right_paddle.rect)
        pygame.draw.ellipse(self.SCREEN, self.GAME_COLORS[2], self.ball.rect)

        # Draw center line
        dashed_line_width = 3
        dashed_line_height = 10
        dashed_line_spacing = 20
        for i in range(0, self.HEIGHT, dashed_line_spacing):
            pygame.draw.rect(self.SCREEN, self.GAME_COLORS[3],
                             pygame.Rect((self.WIDTH // 2 - dashed_line_width // 2), i,
                                         dashed_line_width, dashed_line_height))

        # Draw score board
        font = pygame.font.Font(None, 36)
        left_score_text = font.render(str(self.left_score), True, self.GAME_COLORS[2])
        right_score_text = font.render(str(self.right_score), True, self.GAME_COLORS[2])

        player_side = font.render("You", True, self.GAME_COLORS[1])
        opponent_side = font.render("Opponent", True, self.GAME_COLORS[1])

        self.SCREEN.blit(left_score_text, (self.WIDTH // 2 - left_score_text.get_width() * 3, 20))
        self.SCREEN.blit(right_score_text, (self.WIDTH // 2 + right_score_text.get_width() * 2, 20))

        self.SCREEN.blit(player_side, (self.WIDTH // 2.8, 20))
        self.SCREEN.blit(opponent_side, (self.WIDTH // 1.7, 20))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        self.start_menu()

        while True:
            self.handle_events()
            keys = pygame.key.get_pressed()

            if self.game_started:
                self.draw()
                self.update(keys)
                # Checks if game over
                if self.left_score == 5 or self.right_score == 5:
                    self.continue_menu()
            else:
                self.draw()

            # Control the game speed
            clock.tick(60)

    def update(self, keys):
        # Move the left paddle based on user input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.left_paddle.move("up")
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.left_paddle.move("down")

        # Move the right paddle to follow the ball
        if self.ball.speed_x > 0:
            if self.right_paddle.rect.centery < self.ball.rect.centery and self.right_paddle.rect.bottom > 0:
                self.right_paddle.move("down")
            elif self.right_paddle.rect.centery > self.ball.rect.centery and self.right_paddle.rect.top > 0:
                self.right_paddle.move("up")

        # Move ball
        self.ball.move()

        # Ball collisions with paddles
        if self.ball.rect.colliderect(self.left_paddle.rect) or self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.speed_x *= -1
            self.collision_sound.play()  # Play collision sound

        # Scoring
        if self.ball.rect.left <= 0:
            self.right_score += 1
            if self.right_score == 5:
                self.ball.reset()
            else:
                self.ball.reset()
                self.score_sound.play()  # Play the score sound

        elif self.ball.rect.right >= self.WIDTH:
            self.left_score += 1
            if self.left_score == 5:
                self.ball.reset()
            else:
                self.ball.reset()
                self.score_sound.play()  # Play the score sound


if __name__ == "__main__":
    game = PingPongGame()
    game.run()
