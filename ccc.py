import streamlit as st
import pygame
import time

# Initialize pygame
pygame.init()

# Set screen size
size = (800, 600)
screen = pygame.display.set_mode(size)

# Window title
pygame.display.set_caption("Dino Game")


def play_game():
    done = False
    clock = pygame.time.Clock()

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Dino position
    dino_x = 50
    dino_y = 250

    # Cactus position
    cactus_x = 800
    cactus_y = 300

    # Jump variables
    jump_speed = 0
    gravity = 0.5
    is_jumping = False

    score = 0
    game_over = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                    jump_speed = -10
                    is_jumping = True

                if event.key == pygame.K_SPACE and game_over:
                    dino_y = 250
                    cactus_x = 800
                    score = 0
                    game_over = False

        if not game_over:

            cactus_x -= 7
            if cactus_x < -50:
                cactus_x = 800
                score += 1

            jump_speed += gravity
            dino_y += jump_speed

            if dino_y >= 250:
                dino_y = 250
                is_jumping = False

            dino_rect = pygame.Rect(dino_x, dino_y, 50, 50)
            cactus_rect = pygame.Rect(cactus_x, cactus_y, 50, 50)

            if dino_rect.colliderect(cactus_rect):
                game_over = True

        screen.fill(white)

        pygame.draw.rect(screen, black, (dino_x, dino_y, 50, 50))
        pygame.draw.rect(screen, black, (cactus_x, cactus_y, 50, 50))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, black)
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("Game Over! Press SPACE to restart", True, black)
            screen.blit(over_text, (200, 200))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return score


score = play_game()

st.write(f"Your final score is: {score}")

time.sleep(2)