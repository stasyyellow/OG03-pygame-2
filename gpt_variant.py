import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Игра ТИР')
icon = pygame.image.load('img/тир_icon.jpg')
pygame.display.set_icon(icon)

target_img = pygame.image.load('img/apple_target80.png')
target_width = 80
target_height = 80

color = (18, 37, 129)  # RGB

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
score = 0
last_hit_time = start_time
last_target_time = start_time
game_over = False
end_message_shown = False
end_message_time = 0

font = pygame.font.Font(None, 36)  # Загрузка стандартного шрифта размером 36

def spawn_target():
    global target_x, target_y
    target_x = random.randint(0, SCREEN_WIDTH - target_width)
    target_y = random.randint(0, SCREEN_HEIGHT - target_height)

spawn_target()

running = True

while running:
    screen.fill(color)
    current_time = pygame.time.get_ticks()
    if current_time - start_time > 120000:  # 2 minutes
        game_over = True

    if game_over:
        if not end_message_shown:
            end_message_time = current_time
            end_message_shown = True

    if end_message_shown and current_time - end_message_time > 10000:  # 10 seconds
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                score += 1
                spawn_target()
                last_hit_time = current_time

    if not game_over and current_time - last_target_time > 1500:
        spawn_target()
        last_target_time = current_time

    if not game_over:
        screen.blit(target_img, (target_x, target_y))

    # Отображение счетчика очков на экране
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_over:
        end_text = font.render("Игра длится не более 2 минут, надеюсь тебе понравилось!", True, (255, 255, 255))
        text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(end_text, text_rect)

    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()

print("Your score:", score)
sys.exit()
