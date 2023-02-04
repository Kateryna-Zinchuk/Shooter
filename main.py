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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

    def fire(self):
        pass

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

game = True
play = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.blit(fon, (0, 0))

    txt_missed = font.render("Пропущенно:" + str(missed_enemies), True, WHITE)
    txt_killed = font.render("Збито:" + str(killed_enemies), True, WHITE)
    window.blit(txt_killed, (10, 10))
    window.blit(txt_missed, (10, 40))

    player.reset()
    player.update()

    enemies.draw(window)
    enemies.update()

    clock.tick(FPS)        
    pygame.display.update()