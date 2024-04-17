# Add your imports here
import pygame
from pygame import draw
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width,height = 400,600
screen = pygame.display.set_mode((width, height))
fon = pygame.image.load('Image/fon.png')
fon = pygame.transform.scale(fon, (400, 600))
arial_50 = pygame.font.SysFont('arial', 50)

pygame.display.set_caption("Game menu")

# Add your fonts and Menu class here
class Menu:
    def __init__(self):
        self.option_surfaces = []
        self.callbacks = []
        self.current_option_index = 0

    def append_option(self, option, callback):
        self.option_surfaces.append(arial_50.render(option, True, (0, 0, 0)))
        self.callbacks.append(callback)

    def switch(self, direction):
        self.current_option_index = max(0, min(self.current_option_index + direction, len(self.option_surfaces) - 1))

    def select(self):
        self.callbacks[self.current_option_index]()

    def draw(self, surf, x, y, option_y):
        for i, option in enumerate(self.option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y)
            if i == self.current_option_index:
                draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

# Initialize the menu
menu = Menu()
menu.append_option("Play game", lambda: start_game())
menu.append_option("Options", lambda: print("options"))
menu.append_option('Quit', quit)

# Initialize game variables
running = False
W, H = 400, 600
FPS = 60
# Add your game setup code here

# Function to start the game
def start_game():
    global running
    running = True

# Main game loop
while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                menu.switch(-1)
            elif event.key == pygame.K_s:
                menu.switch(1)
            elif event.key == pygame.K_SPACE:
                menu.select()

    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))
    menu.draw(screen, 100, 75, 100)
    pygame.display.flip()
W, H = 400, 600
FPS = 60
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Марафон")
clock = pygame.time.Clock()


# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Изображения

player_img = pygame.image.load("game_jam_materials/11_1.png")
player_rect = player_img.get_rect()
player_rect.center = (W // 2, H - 50)
pygame.mixer.music.load("game_jam_materials/go.mp3")
pygame.mixer.music.play(0)
time.sleep(1)  # Задержка на 1 секунду

pygame.mixer.music.load("game_jam_materials/fans.mp3")
pygame.mixer.music.play(-1)  # Непрерывное проигрывание

obstacle_imgs = [pygame.Surface((50, 50)) for _ in range(3)]
for img in obstacle_imgs:
    img.fill(RED)

road_img = pygame.image.load("game_jam_materials/bg.png")
road_img = pygame.transform.scale(road_img, (W, H))

# Параметры игры
speed = 5
score = 0
font = pygame.font.SysFont(None, 36)
last_score_increase = pygame.time.get_ticks()  # Время последнего увеличения счета

# Список препятствий
obstacles = []
next_obstacle_time = 0

# Движение дороги
road_y1 = 0
road_y2 = -H




# Основной цикл игры
while True:
    screen.fill(BLACK)

    # Отображение дороги
    screen.blit(road_img, (0, road_y1))
    screen.blit(road_img, (0, road_y2))

    road_y1 += speed  # Движение первой дороги вниз
    road_y2 += speed  # Движение второй дороги вниз

    if road_y1 >= H:
        road_y1 = -H
    if road_y2 >= H:
        road_y2 = -H

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.move_ip(-speed, 0)
    if keys[pygame.K_RIGHT] and player_rect.right < W:
        player_rect.move_ip(speed, 0)
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.move_ip(0, -speed)
    if keys[pygame.K_DOWN] and player_rect.bottom < H:
        player_rect.move_ip(0, speed)

    # Проверка времени для увеличения счета
    current_time = pygame.time.get_ticks()
    if current_time - last_score_increase >= 1000:  # Проверяем каждую секунду
        score += 100
        last_score_increase = current_time

    # Генерация нового препятствия
    if current_time > next_obstacle_time:
        next_obstacle_time = current_time + 1000  # Новое препятствие каждую секунду
        new_obstacle = {
            "rect": obstacle_imgs[random.randint(0, 2)].get_rect(midbottom=(random.randint(0, W), 0)),
            "speed": speed  # Установка скорости препятствия
        }
        obstacles.append(new_obstacle)

    # Обновление и отрисовка препятствий
    for obstacle in obstacles:
        obstacle["rect"].move_ip(0, obstacle["speed"])
        if obstacle["rect"].top > H:
            obstacles.remove(obstacle)
            #score += 1
        if player_rect.colliderect(obstacle["rect"]):
            print("Game Over! Your score:", score)
            pygame.quit()
            sys.exit()
        screen.blit(obstacle_imgs[0], obstacle["rect"])

    # Отрисовка игрока
    screen.blit(player_img, player_rect)

    # Отображение счета
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)