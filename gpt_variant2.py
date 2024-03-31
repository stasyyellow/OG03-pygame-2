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
lives = 3  # Количество жизней

font = pygame.font.Font(None, 36)  # Загрузка стандартного шрифта размером 36

def spawn_target():
    global target_x, target_y
    target_x = random.randint(0, SCREEN_WIDTH - target_width)
    target_y = random.randint(0, SCREEN_HEIGHT - target_height)

spawn_target()

def display_lives():
    heart_icon = pygame.image.load('img/heart_icon.png')
    heart_width = 30
    heart_height = 30
    x_offset = 10
    y_offset = 10
    for i in range(lives):
        screen.blit(heart_icon, (x_offset + i * (heart_width + 5), y_offset))

def game_over_message(message):
    end_text = font.render(message, True, (255, 255, 255))
    text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(end_text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)  # Подождать 3 секунды перед выходом
    sys.exit()

running = True

while running:
    screen.fill(color)
    current_time = pygame.time.get_ticks()
    if current_time - start_time > 120000:  # 2 minutes
        game_over_message("Игра длится не более 2 минут, надеюсь тебе понравилось!")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                score += 1
                spawn_target()
                last_hit_time = current_time
            else:
                lives -= 1
                if lives == 0:
                    game_over_message("Ты проиграл! Будь внимательней")

    if not game_over and current_time - last_target_time > 1500:
        spawn_target()
        last_target_time = current_time

    screen.blit(target_img, (target_x, target_y))

    # Отображение счетчика очков на экране
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 50))

    display_lives()

    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
sys.exit()
