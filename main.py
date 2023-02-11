import pygame
import os
from random import randint
pygame.init()

def file_path(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path

FPS = 40
WIN_WIDTH = 700
WIN_HEIGHT = 500
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

fon = pygame.image.load(file_path("galaxy.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(file_path("main.wav"))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed 


    def fire(self):
        bullet = Bullet(file_path("bullet.png"), self.rect.centerx, self.rect.top, 10, 10, 4)
        bullets.add(bullet)

class Bullet(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()



class Enemy(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)
    
    def update(self):
        global missed_enemies
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIN_WIDTH - self.rect.width)
            self.speed = randint(1, 3)
            missed_enemies += 1

player = Player("rocket.png", 300, 400, 100, 100, 7)
enemies = pygame.sprite.Group()

for i in range(5):
    enemy = Enemy(file_path("asteroid.png"), randint(0, WIN_WIDTH - 50), 0, 50, 50, randint(1, 4))
    enemies.add(enemy)

missed_enemies = 0
killed_enemies = 0
font = pygame.font.SysFont("arial", 35, 0, 0)
txt_missed = font.render("Пропущенно:" + str(missed_enemies), True, WHITE)
txt_killed = font.render("Збито:" + str(killed_enemies), True, WHITE)

bullets = pygame.sprite.Group()

game = True
play = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    window.blit(fon, (0, 0))

    txt_missed = font.render("Пропущенно:" + str(missed_enemies), True, WHITE)
    txt_killed = font.render("Збито:" + str(killed_enemies), True, WHITE)
    window.blit(txt_killed, (10, 10))
    window.blit(txt_missed, (10, 40))

    player.reset()
    player.update()

    enemies.draw(window)
    enemies.update()

    bullets.draw(window)
    bullets.update()

    collide_bullets = pygame.sprite.groupcollide(enemies, bullets, False, True)
    if collide_bullets:
        for enemy in collide_bullets:
            
            killed_enemies += 1 
            enemy.rect.bottom = 0
            enemy.rect.x = randint(0, WIN_WIDTH - enemy.rect.width)
            enemy.speed = randint(1, 3)

    if missed_enemies >= 10 or pygame.sprite.spritecollide(player, enemies, False):
            play = False
            font2 = pygame.font.SysFont("arial", 60, 1, 0)
            txt_lose = font2.render("YOU LOST!", True, RED)
            window.blit(txt_lose, (250, 200))

    if killed_enemies >= 10:
        play = True
        font2 = pygame.font.SysFont("arial", 60, 1, 0)
        txt_win = font2.render("YOU WON!", True, GREEN)
        window.blit(txt_win, (250, 200))

    clock.tick(FPS)        
    pygame.display.update()