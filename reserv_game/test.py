import pygame
from random import randint as ri
import sys
from pygame import draw

pygame.init()
time = pygame.time.Clock()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Reserv_game")
icon = pygame.image.load('images/icon.png')
fon = pygame.image.load('images/menuu.jpg')
fon = pygame.transform.scale(fon, (800, 600))
arial_50 = pygame.font.SysFont('arial', 50)

rigth = False
left = False
animcount = 0
player = pygame.image.load('images/1.png')
walk_left = [
    pygame.image.load('images/move_left/1.png'),
    pygame.image.load('images/move_left/2.png'),
    pygame.image.load('images/move_left/3.png'),
    pygame.image.load('images/move_left/4.png')
]
walk_right = [
    pygame.image.load('images/move_right/1.png'),
    pygame.image.load('images/move_right/2.png'),
    pygame.image.load('images/move_right/3.png'),
    pygame.image.load('images/move_right/4.png')
]

enemy_rigth = [
    pygame.transform.scale(pygame.image.load('images/rigth_player/r1.png').convert_alpha(), (100, 100)),
    pygame.transform.scale(pygame.image.load('images/rigth_player/r2.png').convert_alpha(), (100, 100)),
    pygame.transform.scale(pygame.image.load('images/rigth_player/r3.png').convert_alpha(), (100, 100)),
    pygame.transform.scale(pygame.image.load('images/rigth_player/r4.png').convert_alpha(), (100, 100))
]
enemy_anim_count = 0
enemy_list = []
enemy_rect_x = -101
enemy_speed = 4

move_fire = "rigth"

player_x = 100
player_y = 245
player_speed = 10
player_anim_count = 0
is_jump = False
jump_count = 12


class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def draw_window():
    global animcount

    if animcount + 1 >= 20:
        animcount = 0

    if left:
        screen.blit(walk_left[animcount // 5], (player_x, player_y))
        animcount += 1
    elif rigth:
        screen.blit(walk_right[animcount // 5], (player_x, player_y))
        animcount += 1
    else:
        screen.blit(player, (player_x, player_y))

    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.update()


def check_collisions():
    global bullets, zombi_list, enemy_list, points
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, 2 * bullet.radius,
                                  2 * bullet.radius)

        for zombi in zombi_list[:]:
            zombi_rect = pygame.Rect(zombi.x, zombi.y, 100, 100)
            if bullet_rect.colliderect(zombi_rect):
                bullets.remove(bullet)
                zombi_list.remove(zombi)
                break

        for enemy in enemy_list[:]:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, 100, 100)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemy_list.remove(enemy)
                break


zombi = [
    pygame.image.load('images/zombi/1.png'),
    pygame.image.load('images/zombi/2.png'),
    pygame.image.load('images/zombi/3.png'),
    pygame.image.load('images/zombi/4.png'),
    pygame.image.load('images/zombi/5.png'),
    pygame.image.load('images/zombi/6.png'),
    pygame.image.load('images/zombi/7.png'),
    pygame.image.load('images/zombi/8.png'),
    pygame.image.load('images/zombi/9.png'),
    pygame.image.load('images/zombi/10.png'),
    pygame.image.load('images/zombi/11.png'),
    pygame.image.load('images/zombi/12.png'),
    pygame.image.load('images/zombi/13.png'),
    pygame.image.load('images/zombi/14.png'),
    pygame.image.load('images/zombi/15.png'),
    pygame.image.load('images/zombi/16.png'),
    pygame.image.load('images/zombi/17.png'),
    pygame.image.load('images/zombi/18.png'),
]
zombi_anim_count = 0
zombi_list = []
zombi_rect_x = 801
zombi_speed = 4
bullets = []

money = [
    pygame.image.load('images/money/1.png'),
    pygame.image.load('images/money/2.png'),
    pygame.image.load('images/money/3.png'),
    pygame.image.load('images/money/4.png'),
    pygame.image.load('images/money/5.png'),
    pygame.image.load('images/money/6.png')
]
money_list = []
money_anim_count = 0
money_speed = 10
money_count = 30

bg = pygame.image.load('images/bgg.jpg')
bg_x = 0
bg_lose = pygame.image.load('images/bg_lose.png')
labal_font = pygame.font.Font('font/Old-Soviet.otf', 40)
labal_lose = labal_font.render('Вы проиграли!', False, (193, 196, 199))
heart = [
    pygame.image.load('images/heart/1.png'),
    pygame.image.load('images/heart/1.png'),
    pygame.image.load('images/heart/1.png'),
    pygame.image.load('images/heart/1.png'),
    pygame.image.load('images/heart/1.png'),
    pygame.image.load('images/heart/2.png'),
    pygame.image.load('images/heart/3.png'),
    pygame.image.load('images/heart/2.png'),
    pygame.image.load('images/heart/3.png'),

]
heart_anim_count = 0

pygame.display.set_icon(icon)


class Menu:
    def __init__(self, screen, items, font):
        self.screen = screen
        self.items = items
        self.font = font
        self.current_option_index = 0

    def draw(self):
        self.screen.blit(fon, (0, 0))
        for index, item in enumerate(self.items):
            label = self.font.render(item[0], True,
                                     (255, 255, 255) if index == self.current_option_index else (100, 100, 100))
            label_rect = label.get_rect(center=(400, 150 + index * 50))
            self.screen.blit(label, label_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.current_option_index = (self.current_option_index + 1) % len(self.items)
            elif event.key == pygame.K_UP:
                self.current_option_index = (self.current_option_index - 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                self.items[self.current_option_index][1]()


def start_game():
    print("Game is starting...")
    global running
    running = True
    global player_life
    player_life = 3
    global points
    points = 0


def quit_game():
    pygame.quit()
    sys.exit()


menu_items = [
    ("Play Game", start_game),
    ("Quit", quit_game)
]
menu = Menu(screen, menu_items, arial_50)

running = False




def show_menu():
    screen.fill((0, 0, 0))
    menu.draw()
    pygame.display.update()


show_menu()
while True:
    if (running == False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            menu.handle_event(event)
            screen.fill((0, 0, 0))
            menu.draw()
            pygame.display.update()
    else:
        labal_life = labal_font.render(str(player_life), False, (193, 196, 199))
        labal_points = labal_font.render(str(points) + '', False, (193, 196, 199))

        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 800, 0))
        screen.blit(bg, (bg_x - 800, 0))
        screen.blit(labal_life, (80, 10))
        screen.blit(heart[heart_anim_count], (10, 10))
        screen.blit(labal_points, (600, 10))

        for bullet in bullets:
            if bullet.x < 800 and bullet.x > 0:
                bullet.x += bullet.vel

            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            if move_fire == "rigth":
                facing = 1
            else:
                facing = -1

            if len(bullets) < 3:
                bullets.append(snaryad(round(player_x + 70 // 2), round(player_y + 80 // 2), 8, (255, 0, 0), facing))

        if player_life <= 0:
            screen.blit(bg_lose, (0, 0))
            screen.blit(labal_lose, (200, 200))
            running = False
            show_menu()
            pygame.display.update()
            continue
        player_rect = player.get_rect(topleft=(player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 5:
            player_x -= player_speed
            left = True
            rigth = False
            move_fire = "left"
            bg_x += player_speed
        elif keys[pygame.K_RIGHT] and player_x < 800 - 70 - 5:
            player_x += player_speed
            left = False
            rigth = True
            move_fire = "rigth"
            bg_x -=player_speed
        else:
            left = False
            rigth = False
            animcount = 0

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -12:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 2
            else:
                is_jump = False
                jump_count = 12

        if enemy_anim_count == 3:
            enemy_anim_count = 0
        else:
            enemy_anim_count += 1

        check_enemy = ri(0, 60)
        if check_enemy == 2:
            enemy_list.append(enemy_rigth[enemy_anim_count].get_rect(topleft=(enemy_rect_x, 230)))
            enemy_rect_x += enemy_speed

        if enemy_list:
            for enemy_rect in enemy_list:
                screen.blit(enemy_rigth[enemy_anim_count], enemy_rect)
                enemy_rect.x += enemy_speed
                if player_rect.colliderect(enemy_rect):
                    player_life -= 1
                    player_x = 100
                    enemy_list.pop(0)

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        if zombi_anim_count == 17:
            zombi_anim_count = 0
        else:
            zombi_anim_count += 1

        if heart_anim_count == 8:
            heart_anim_count = 0
        else:
            heart_anim_count += 1

        if money_anim_count == 5:
            money_anim_count = 0
        else:
            money_anim_count += 1

        check = ri(0, 60)
        if check == 2:
            zombi_list.append(zombi[zombi_anim_count].get_rect(topleft=(zombi_rect_x, 230)))
            zombi_rect_x -= 4

        if zombi_list:
            for i in zombi_list:
                screen.blit(zombi[zombi_anim_count], i)
                i.x -= zombi_speed
                if player_rect.colliderect(i):
                    player_life -= 1
                    player_x = 100
                    zombi_list.pop(0)

        check_money = ri(10, 750)
        check_time = ri(0, 100)
        if money_count > 0:
            if check_time == 5:
                money_list.append(money[money_anim_count].get_rect(topleft=(check_money, 0)))
                money_count -= 1
        if money_list:
            for (i, money_idx) in enumerate(money_list):
                screen.blit(money[money_anim_count], money_idx)
                if money_idx.y <= 230:
                    money_idx.y += money_speed
                if money_idx.colliderect(player_rect):
                    money_list.pop(i)
                    points += 1
        check_collisions()

        draw_window()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        time.tick(15)
