import pygame
import os
pygame.init()

def file_path(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path

FPS = 40
WIN_WIDTH = 700
WIN_HEIGHT = 500

fon = pygame.image.load(file_path("galaxy.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(file_path("main.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (wigth, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

game = True
play = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.blit(fon, (0, 0))


    clock.tick(FPS)        
    pygame.display.update()