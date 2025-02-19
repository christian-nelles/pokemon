import pygame
pygame.init()
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
image1 = pygame.image.load("images/map.png")
image2 = pygame.image.load("images/noir.png")
battle_scene = pygame.image.load("images/battle_grass-resize (2).png")
grass = pygame.image.load("images/grass.png")
image1 = pygame.transform.scale(image1, (WIDTH, HEIGHT))
image2 = pygame.transform.scale(image2, (WIDTH, HEIGHT))
battle_scene = pygame.transform.scale(battle_scene, (WIDTH, HEIGHT))
grass = pygame.transform.scale(grass, (WIDTH, HEIGHT))
def slide_transition(screen, old_scene, black_scene, battle_scene, grass):
    """Effectue la transition complète en 3 étapes."""
    y_split = HEIGHT // 100
    x_old_top, x_old_bottom = 0, 0
    x_new_top, x_new_bottom = WIDTH, -WIDTH
    running = True
    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))
        x_old_top -= 60
        x_old_bottom += 60
        x_new_top -= 60
        x_new_bottom += 60
        if x_old_top <= -WIDTH:
            x_old_top, x_old_bottom = -WIDTH, WIDTH
            x_new_top, x_new_bottom = 0, 0
            running = False
        for i in range(0, 110, 2):
            screen.blit(old_scene, (x_old_top, y_split * i), (0, y_split * i, WIDTH, y_split))
            screen.blit(black_scene, (x_new_top, y_split * i), (0, y_split * i, WIDTH, y_split))
            screen.blit(old_scene, (x_old_bottom, y_split + y_split * i), (0, y_split + y_split * i, WIDTH, y_split))
            screen.blit(black_scene, (x_new_bottom, y_split + y_split * i), (0, y_split + y_split * i, WIDTH, y_split))
        pygame.display.update()
    y_top, y_bottom = 0, HEIGHT // 2
    grass_x, grass_y = 0, 250
    running = True
    while running:
        clock.tick(60)
        screen.blit(battle_scene, (0, 0))
        grass_x -= 75
        screen.blit(grass, (grass_x, grass_y))
        screen.blit(grass, (grass_x + WIDTH, grass_y))
        y_top -= 30
        y_bottom += 30
        if y_top <= -HEIGHT // 2:
            running = False
        screen.blit(black_scene, (0, y_top), (0, 0, WIDTH, HEIGHT // 2))
        screen.blit(black_scene, (0, y_bottom), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        pygame.display.update()
    grass_x, grass_y = 0, 250
    x_exp, y_exp = 75, 1
    running = True
    while running:
        clock.tick(60)
        screen.blit(battle_scene, (0, 0))
        grass_x -= x_exp
        x_exp -= 0.5
        grass_y += y_exp
        y_exp *= 1.035
        if grass_x <= -WIDTH:
            grass_x = 0
        screen.blit(grass, (grass_x, grass_y))
        screen.blit(grass, (grass_x + WIDTH, grass_y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
running = True
scene_active = image1
next_scene = image2
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            slide_transition(screen, scene_active, next_scene, battle_scene, grass)
            scene_active, next_scene = next_scene, scene_active
    screen.blit(scene_active, (0, 0))
    pygame.display.update()
    clock.tick(60)
pygame.quit()