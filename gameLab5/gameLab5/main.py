import pygame
from random import randint as ri

time = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((800, 400)) #flags=pygame.NOFRAME
pygame.display.set_caption("Marathon")
icon = pygame.image.load('images/icon.png')

runnner_life = pygame.image.load('images/1.png')
runner_walk_left = [
    pygame.image.load('images/move_left/1.png'),
    pygame.image.load('images/move_left/2.png'),
    pygame.image.load('images/move_left/3.png'),
    pygame.image.load('images/move_left/4.png')
]
runner_walk_right = [
    pygame.image.load('images/move_right/1.png'),
    pygame.image.load('images/move_right/2.png'),
    pygame.image.load('images/move_right/3.png'),
    pygame.image.load('images/move_right/4.png')
]

agai_life = pygame.image.load('images/Arnur/1.png')
agai_walk_left = [
    pygame.image.load('images/Arnur/move_left/left1.png'),
    pygame.image.load('images/Arnur/move_left/left2.png'),
    pygame.image.load('images/Arnur/move_left/left3.png'),
    pygame.image.load('images/Arnur/move_left/left4.png')
]
agai_walk_right = [
    pygame.image.load('images/Arnur/move_right/right1.png'),
    pygame.image.load('images/Arnur/move_right/right2.png'),
    pygame.image.load('images/Arnur/move_right/right3.png'),
    pygame.image.load('images/Arnur/move_right/right4.png')
]
agai_life_x = 100
agai_life_y = 245
agai_life_speed = 10
agai_life_anim_count = 0
is_jump = False
jump_count = 12
agai_life_life = 3
runner_life_x = 50  # Initial horizontal position for runner
runner_life_y = 245  # Same vertical position as Agai to align on the path
runner_life_speed = agai_life_speed // 6  # Runner's speed is 3 times slower than Agai
runner_overtaken = False  # Flag to check if runner has overtaken Agai

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
zombi_speed = 10

fire = [
    pygame.image.load('images/fire/1.png'),
    pygame.image.load('images/fire/2.png'),
    pygame.image.load('images/fire/3.png'),
    pygame.image.load('images/fire/4.png'),
    pygame.image.load('images/fire/5.png'),
    pygame.image.load('images/fire/6.png'),
    pygame.image.load('images/fire/7.png'),
    pygame.image.load('images/fire/8.png'),
]
fire_list = []
fire_anim_count = 0
fire_speed = 12

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
points = 0


bg = pygame.image.load('images/bg.jpg')
bg_width = bg.get_width()  # Assuming all backgrounds are the same width
bg_x = 0  # Starting position of the first background
bg_x2 = bg_width
bg_lose = pygame.image.load('images/bg_lose.png')
labal_font = pygame.font.Font('font/Old-Soviet.otf', 40)
labal_lose = labal_font.render('You are too slow!', False, (193, 196, 199))
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

timer = 0

pygame.display.set_icon(icon)

running = True
bg_sound = pygame.mixer.Sound('sounds/bg.mp3')
bg_sound.play()
while running:
    labal_life = labal_font.render(str(agai_life_life), False, (193, 196, 199))
    labal_points = labal_font.render(str(points) + '(30)', False, (193, 196, 199))

    if bg_x < -bg_width:
        bg_x = bg_width  # Reset the first background to the right of the second
    if bg_x2 < -bg_width:
        bg_x2 = bg_width

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x2, 0))
    screen.blit(bg, (bg_x + 800, 0))
    screen.blit(bg, (bg_x - 800, 0))
    screen.blit(labal_life, (80, 10))
    screen.blit(heart[heart_anim_count], (10, 10))
    screen.blit(labal_points, (600, 10))

    if agai_life_life <= 0:
        screen.blit(bg_lose, (0, 0))
        screen.blit(labal_lose, (200, 200))

    # if agai_life_x + bg_x >= 223:
    #     screen.blit(bg_lose, (0, 0))
    #     screen.blit(labal_font.render('You win', False, (193, 196, 199)), (200, 200))
    #     running = False
    if agai_life_x + bg_x >= 223:
        if timer == 0:  # timer for ending game
            timer = 4 * 5
        screen.blit(bg_lose, (0, 0))
        screen.blit(labal_font.render('You win', False, (193, 196, 199)), (200, 200))

    # Timer countdown logic
    if timer > 0:
        timer -= 1  # Decrement the timer each frame
        if timer == 0:
            running = False

    agai_life_rect = agai_life.get_rect(topleft=(agai_life_x, agai_life_y))

    keys = pygame.key.get_pressed()

    # Add the runner's movement based on Agai's movement
    if agai_life_x > 100:  # Runner starts moving once Agai has moved
        runner_life_x += runner_life_speed
        screen.blit(runner_walk_right[agai_life_anim_count % 4], (runner_life_x, runner_life_y))  # Using Agai's animation frame count for simplicity

    # Check if the runner has overtaken Agai
    if runner_life_x > agai_life_x:
        runner_overtaken = True  # Set the overtaken flag to True

    if keys[pygame.K_a] and agai_life_x > 50:
        screen.blit(agai_walk_left[agai_life_anim_count], (agai_life_x, agai_life_y))
        agai_life_x -= agai_life_speed
        bg_x += agai_life_speed - 2
        if bg_x == 800:
            bg_x = 0

    # Check if the runner has overtaken Agai
    if runner_life_x > agai_life_x:
        runner_overtaken = True  # Set the overtaken flag to True

    # End the game if runner overtakes Agai
    if runner_overtaken:
        pygame.display.set_caption("Game Over: Runner has overtaken Agai!")
        screen.blit(bg_lose, (0, 0))
        screen.blit(labal_font.render('Game Over: you lose!', False, (193, 196, 199)), (200, 200))
        if timer == 0:  # timer for ending game
            timer = 4 * 5
        # running = False

    elif keys[pygame.K_d] and agai_life_x < 720:
        screen.blit(agai_walk_right[agai_life_anim_count], (agai_life_x, agai_life_y))
        agai_life_x += agai_life_speed
        bg_x -= agai_life_speed - 2
        bg_x2 -= agai_life_speed - 2
        if bg_x == -800:
            bg_x = 0
    else:
        screen.blit(agai_life, (agai_life_x, agai_life_y))

    if keys[pygame.K_e]:
        fire_list.append(fire[fire_anim_count].get_rect(topleft=(agai_life_x + 30, agai_life_y)))

    if fire_list:
        for (i, fire_idx) in enumerate(fire_list):
            screen.blit(fire[fire_anim_count], fire_idx)
            fire_idx.x += fire_speed

            if zombi_list:
                for (i2, zombi_idx) in enumerate(zombi_list):
                    if fire_idx.colliderect(zombi_idx):
                        fire_list.pop(i)
                        zombi_list.pop(i2)


    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -12:
            if jump_count > 0:
                agai_life_y -= (jump_count ** 2) / 2
            else:
                agai_life_y += (jump_count ** 2) / 2
            jump_count -= 2
        else:
            is_jump = False
            jump_count = 12



    if agai_life_anim_count == 3:
        agai_life_anim_count = 0
    else:
        agai_life_anim_count += 1

    if zombi_anim_count == 17:
        zombi_anim_count = 0
    else:
        zombi_anim_count +=1

    if heart_anim_count == 8:
        heart_anim_count = 0
    else:
        heart_anim_count +=1
    if fire_anim_count == 7:
        fire_anim_count = 0
    else:
        fire_anim_count += 1
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
            if agai_life_rect.colliderect(i):
                agai_life_life -= 1
                agai_life_x = 100
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
            if money_idx.colliderect(agai_life_rect):
                money_list.pop(i)
                points += 1


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    time.tick(15)