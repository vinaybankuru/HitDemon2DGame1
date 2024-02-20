import pygame
import random
import math
pygame.init()
screen = pygame.display.set_mode((800, 600))
title = "Devil Hunter"
icon = pygame.image.load('data/murder.png')
pygame.display.set_caption(title)
pygame.display.set_icon(icon)
bg = pygame.image.load('data/background.png')
pygame.mixer.music.load('data/moose.mp3')
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound('data/GUNSHOT.wav')
explosion_sound = pygame.mixer.Sound('data/explosion3.wav')
player_img = pygame.image.load('data/jet.png')
playerX = 368
playerY = 516
playerX_change = 0
num_of_enemies = 5
enemies_img = []
enemiesX = []
enemiesY = []
enemiesX_change = []
enemiesY_change = []
for i in range(num_of_enemies):
    enemies_img.append(pygame.image.load('data/ghost.png'))
    enemiesX.append(random.randint(0, 736))
    enemiesY.append(random.randint(20, 120))
    enemiesX_change.append(5)
    enemiesY_change.append(50)
bullet_img = pygame.image.load('data/bomb.png')
bulletX = 0
bulletY = 516
bulletY_change = -10
bullet_state = 'ready'
score = 0
score_font = pygame.font.Font('data/orangejuice.ttf', 32)
scoreX = 10
scoreY = 10
gameover_font = pygame.font.Font('data/orangejuice.ttf', 64)
gameoverX = 200
gameoverY = 200
restart_font = pygame.font.Font('data/orangejuice.ttf', 32)
restartX = 180
restartY = 300
game_status = 'running'


def show_restart(x, y):
    restart_img = restart_font.render('TO RESTART THE GAME PRESSS R', True, (0, 255, 0))
    screen.blit(restart_img, (x, y))


def show_gameover(x, y):
    global game_status
    gameover_img = gameover_font.render('GAMEOVER', True, (255, 255, 255))
    screen.blit(gameover_img, (x, y))
    pygame.mixer.music.stop()
    game_status = 'end'


def show_score(x, y):
    score_img = score_font.render('score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_img, (x, y))


def iscollosion(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < 25:
        return True
    else:
        return False


def bullet(x, y):
    screen.blit(bullet_img, (x + 16, y + 10))


def enemies(x, y, i):
    screen.blit(enemies_img[i], (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


game_on = True
while game_on:
    screen.fill((45, 51, 71))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_state = 'fire'
                    bulletX = playerX
                    bullet(bulletX, bulletY)
                    bullet_sound.play()
            if event.key == pygame.K_r:
                if game_status == 'end':
                    game_status = 'runing'
                    score = 0
                    playerX = 368
                    pygame.mixer.music.play(-1)
                    for i in range(num_of_enemies):
                        enemiesX[i] = random.randint(0, 736)
                        enemiesY[i] = random.randint(20, 120)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    if bullet_state == 'fire':
        if bulletY < 10:
            bulletY = 516
            bullet_state = 'ready'
        bulletY += bulletY_change
        bullet(bulletX, bulletY)
    for i in range(num_of_enemies):
        if enemiesY[i] > 466:
            show_gameover(gameoverX, gameoverY)
            show_restart(restartX, restartY)
            for j in range(num_of_enemies):
                enemiesY[j] = 1400
        enemiesX[i] += enemiesX_change[i]
        if enemiesX[i] <= 0:
            enemiesX[i] = 0
            enemiesX_change[i] = 3
            enemiesY[i] += enemiesY_change[i]
        elif enemiesX[i] >= 736:
            enemiesX[i] = 736
            enemiesX_change[i] = -3
            enemiesY[i] += enemiesY_change[i]
        enemies(enemiesX[i], enemiesY[i], i)
        collosion = iscollosion(enemiesX[i], enemiesY[i], bulletX, bulletY)
        if collosion:
            bulletY = 516
            bullet_state = 'ready'
            enemiesX[i] = random.randint(0, 736)
            enemiesY[i] = random.randint(20, 120)
            score += 1
            explosion_sound.play()
    show_score(scoreX, scoreY)
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    player(playerX, playerY)
    pygame.display.update()
