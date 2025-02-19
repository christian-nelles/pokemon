import pygame
import sys

# Initialisation de Pygame
pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Deplacement avec caméra et zoom')

map_image = pygame.image.load('images/background/map.jpg')
character_image = pygame.image.load('images/perso.png')

map_width, map_height = map_image.get_size()

x, y = 100, 100

speed = 20

camera_x, camera_y = 0, 0

zoom = 3.0

def zoom_image(image, factor):
    size = (int(image.get_width() * factor), int(image.get_height() * factor))
    return pygame.transform.scale(image, size)

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    zoomed_map = zoom_image(map_image, zoom)
    zoomed_character = zoom_image(character_image, zoom)

    zoomed_map_width, zoomed_map_height = zoomed_map.get_size()

    max_x = zoomed_map_width - character_image.get_width()
    max_y = zoomed_map_height - character_image.get_height()

    x = max(0, min(x, max_x))
    y = max(0, min(y, max_y))

    camera_x = max(0, min(x - WIDTH // 2, zoomed_map_width - WIDTH))
    camera_y = max(0, min(y - HEIGHT // 2, zoomed_map_height - HEIGHT))

    screen.blit(zoomed_map, (-camera_x, -camera_y))

    screen.blit(zoomed_character, (x - camera_x, y - camera_y))

    pygame.display.update()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()