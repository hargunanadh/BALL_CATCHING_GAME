import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 500
FPS = 60

# Colors (Catppuccin theme)
BG_COLOR = (30, 30, 46)
PADDLE_COLOR = (137, 180, 250)
TEXT_COLOR = (205, 214, 244)
ACCENT_PINK = (243, 139, 168)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Catching Game - Python")
clock = pygame.time.Clock()

def create_ball():
    return {
        "x": random.randint(15, WIDTH - 15),
        "y": random.randint(-200, -20),
        "radius": 12,
        "speed_y": random.uniform(3, 5.5),
        "color": (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    }

def main():
    score = 0
    lives = 3
    game_over = False

    # Paddle settings
    paddle_width = 100
    paddle_height = 15
    paddle_x = WIDTH // 2 - paddle_width // 2
    paddle_y = HEIGHT - 30
    paddle_speed = 8

    # Balls settings (Multi-ball variant)
    max_balls = 5
    balls = [create_ball() for _ in range(max_balls)]

    font = pygame.font.SysFont(None, 24)
    game_over_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(BG_COLOR)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over and (event.key == pygame.K_r or event.key == pygame.K_SPACE):
                    # Restart game
                    score = 0
                    lives = 3
                    game_over = False
                    balls = [create_ball() for _ in range(max_balls)]

        if not game_over:
            # Keyboard controls (Left/Right arrows)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle_x -= paddle_speed
            if keys[pygame.K_RIGHT]:
                paddle_x += paddle_speed

            # Mouse controls (smooth follow)
            mouse_x, _ = pygame.mouse.get_pos()
            paddle_x = mouse_x - paddle_width // 2

            # Keep paddle inside screen bounds
            if paddle_x < 0:
                paddle_x = 0
            if paddle_x > WIDTH - paddle_width:
                paddle_x = WIDTH - paddle_width

            # Update all balls
            for b in balls:
                b["y"] += b["speed_y"]

                # Paddle collision check
                if b["y"] + b["radius"] >= paddle_y and paddle_x <= b["x"] <= paddle_x + paddle_width:
                    score += 10
                    b.update(create_ball())

                # Check if ball hits the bottom (missed)
                if b["y"] - b["radius"] > HEIGHT:
                    lives -= 1
                    b.update(create_ball())
                    if lives <= 0:
                        game_over = True

        # Draw paddle
        pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, paddle_y, paddle_width, paddle_height), border_radius=4)

        # Draw balls
        for b in balls:
            pygame.draw.circle(screen, b["color"], (int(b["x"]), int(b["y"])), b["radius"])

        # Draw UI (Score & Lives)
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
        screen.blit(score_text, (15, 15))
        screen.blit(lives_text, (WIDTH - 90, 15))

        # Game Over Screen overlay
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            go_text = game_over_font.render("GAME OVER", True, ACCENT_PINK)
            restart_text = font.render("Press R or Space to Restart", True, TEXT_COLOR)

            screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()