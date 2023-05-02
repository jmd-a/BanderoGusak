import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

randint = random.randint
FPS = pygame.time.Clock()

# Window size
HEIGHT = 800
WIDTH = 1280

FONT = pygame.font.SysFont('Verdana', 40)

# Used colors
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)

main_display = pygame.display.set_mode((WIDTH,HEIGHT))

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

# Player characteristics
player_size = (30, 30)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect(center = (100, (HEIGHT/2)-15))
player_move_down = [0,8]
player_move_right = [8,0]
player_move_up = [0,-8]
player_move_left = [-8,0]

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)


def create_enemy():
    enemy_size = (200,70)
    enemy = pygame.transform.scale(pygame.image.load("enemy.png").convert_alpha(), (200, 70))
    enemy_rect = pygame.Rect(WIDTH, randint(100,HEIGHT-100), *enemy_size)
    enemy_move = [randint(-15, -8), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (100,200)
    bonus = pygame.transform.scale(pygame.image.load("bonus.png").convert_alpha(), (100, 200))
    bonus_rect = pygame.Rect(randint(100,WIDTH-100), -bonus.get_height(), *bonus_size)
    bonus_move = [0, randint(3,10)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 5000)
CHANGE_IMG= pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 200)

enemies = []
bonuses = []

score = 0

img_index = 0

# Ingame
playing = True
while playing:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[img_index]))
            img_index += 1
            if img_index >= len(PLAYER_IMAGES):
                img_index = 0
            

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()
    
    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1,0))
    main_display.blit(bg, (bg_x2,0))

    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False
            

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    
    main_display.blit(player, player_rect)

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))


    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))