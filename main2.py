import pygame
import random
import pygame_gui

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
round_choice = None

font = pygame.font.Font(None, 36)  # Загрузка стандартного шрифта размером 36

def spawn_target(num_targets):
    targets = []
    for _ in range(num_targets):
        target_x = random.randint(0, SCREEN_WIDTH - target_width)
        target_y = random.randint(0, SCREEN_HEIGHT - target_height)
        targets.append((target_x, target_y))
    return targets

def start_round(num_targets):
    global round_targets
    round_targets = spawn_target(num_targets)

def draw_targets(targets):
    for target in targets:
        screen.blit(target_img, target)

def handle_click(target, mouse_pos):
    mouse_x, mouse_y = mouse_pos
    target_x, target_y = target
    if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
        return True
    return False

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

start_round_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (200, 50)),
                                                  text='Round 1 (1 target)',
                                                  manager=manager)
start_round_button_2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 120), (200, 50)),
                                                  text='Round 2 (2 targets)',
                                                  manager=manager)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_round_button:
                    start_round(1)
                    round_choice = 1
                    game_over = False
                elif event.ui_element == start_round_button_2:
                    start_round(2)
                    round_choice = 2
                    game_over = False

        manager.process_events(event)

    manager.update(time_delta)

    screen.fill(color)

    if round_choice is not None and not game_over:
        draw_targets(round_targets)
        mouse_pos = pygame.mouse.get_pos()
        for target in round_targets:
            if handle_click(target, mouse_pos):
                score += 1
                round_targets.remove(target)
                last_hit_time = pygame.time.get_ticks()

        if not round_targets:
            game_over = True

    manager.draw_ui(screen)
    if game_over:
        end_text = font.render("Игра завершена. Ваш счет: " + str(score), True, (255, 255, 255))
        text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(end_text, text_rect)

    pygame.display.update()

pygame.quit()