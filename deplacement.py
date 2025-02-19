import pygame
import sys
import random
import time
from fight import main_fight
from menu import *

# Initialisation de Pygame
pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Déplacement avec caméra et zoom')

# Charger les images
map_image = pygame.image.load('images/map.png')
collision_image = pygame.image.load('images/collisions.png')  # L'image invisible pour les collisions

# Charger les sprites de l'animation du personnage (4 directions, 3 images par direction)
character_images = {
    'down': [pygame.image.load('images/sheet/tile0.png'), pygame.image.load('images/sheet/tile1.png'), pygame.image.load('images/sheet/tile2.png')],
    'up': [pygame.image.load('images/sheet/tile3.png'), pygame.image.load('images/sheet/tile4.png'), pygame.image.load('images/sheet/tile5.png')],
    'right': [pygame.image.load('images/sheet/tile6.png'), pygame.image.load('images/sheet/tile7.png'), pygame.image.load('images/sheet/tile8.png')],
    'left': [pygame.image.load('images/sheet/tile9.png'), pygame.image.load('images/sheet/tile10.png'), pygame.image.load('images/sheet/tile11.png')]
}

# Dimensions de la carte
map_width, map_height = map_image.get_size()

# Position initiale du joueur
x, y = 3455, 3530

# Vitesse de déplacement
speed = 16

# Position de la caméra
camera_x, camera_y = 0, 0

# Facteur de zoom
zoom = 3.0

"""-----VARIABLE DE TRANSITION-----"""
clock = pygame.time.Clock()

# Chargement des images
image1 = pygame.image.load("images/map.png")
image2 = pygame.image.load("images/noir.png")
battle_scene = pygame.image.load("images/battle_grass-resize (2).png")
grass = pygame.image.load("images/grass.png")
image1 = pygame.transform.scale(image1, (WIDTH, HEIGHT))
image2 = pygame.transform.scale(image2, (WIDTH, HEIGHT))
battle_scene = pygame.transform.scale(battle_scene, (WIDTH, HEIGHT))
grass = pygame.transform.scale(grass, (WIDTH, HEIGHT))


def capture_screen(): # (pygame Surface, String, tuple, tuple)def capture_screen():  # (pygame Surface)
    screen.blit(zoomed_map, (-camera_x, -camera_y))
    image = pygame.Surface((1280, 750))  # Créer une surface d'image de taille appropriée
    image.blit(screen, (0, 0))  # Copier l'écran sur cette surface
    pygame.image.save(image, "screenshot.jpeg")  # Sauvegarder l'image sur disque
    return image  # Renvoyer la surface capturée



def slide_transition(screen, black_scene, battle_scene, grass):
    """Effectue la transition complète en 3 étapes."""
    old_scene = capture_screen()
    for _ in range(3):
        for alpha in range(255, -1, -5):
            screen.blit(old_scene, (0, 0))
            screen.blit(zoomed_character, (x - camera_x, y - camera_y))
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((70, 70, 70))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))
            pygame.display.update()
    y_split = HEIGHT // 100
    x_old_top, x_old_bottom = 0, 0
    x_new_top, x_new_bottom = WIDTH, -WIDTH
    current_loop = 0
    running = True
    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))
        x_old_top -= 20
        x_old_bottom += 20
        x_new_top -= 20
        x_new_bottom += 20
        zoomed_character_alpha = zoomed_character.copy()
        opacity = 255 * (1 - (current_loop / 63))
        current_loop += 1
        zoomed_character_alpha.set_alpha(opacity)
        if x_old_top <= -WIDTH:
            x_old_top, x_old_bottom = -WIDTH, WIDTH
            x_new_top, x_new_bottom = 0, 0
            running = False
        for i in range(0, 110, 2):
            screen.blit(old_scene, (x_old_top, y_split * i), (0, y_split * i, WIDTH, y_split))
            screen.blit(black_scene, (x_new_top, y_split * i), (0, y_split * i, WIDTH, y_split))
            screen.blit(old_scene, (x_old_bottom, y_split + y_split * i), (0, y_split + y_split * i, WIDTH, y_split))
            screen.blit(black_scene, (x_new_bottom, y_split + y_split * i), (0, y_split + y_split * i, WIDTH, y_split))
        screen.blit(zoomed_character_alpha, (x - camera_x, y - camera_y))
        pygame.display.update()
    main_fight()













# Fonction pour appliquer le zoom sur les images
def zoom_image(image, factor):
    size = (int(image.get_width() * factor), int(image.get_height() * factor))
    return pygame.transform.scale(image, size)

# Fonction pour vérifier les collisions avec l'image invisible
# Taille de la zone de collision
collision_width = 30  # Largeur de la zone de collision
collision_height = 30  # Hauteur de la zone de collision

# Décalages de la collision (centrée par défaut)
collision_offset_x = 0  # Décalage horizontal de la zone de collision
collision_offset_y = 20  # Décalage vertical de la zone de collision

def check_collisions(dx=0, dy=0):
    """ Vérifie la couleur dans la zone de collision centrée autour du joueur. """
    future_x = x + dx
    future_y = y + dy

    # Calculer le centre de la zone de collision
    center_x = future_x + zoomed_character.get_width() // 2
    center_y = future_y + zoomed_character.get_height() // 2

    # Définir les coordonnées du coin supérieur gauche de la zone de collision
    collision_rect_x = center_x - collision_width // 2 + collision_offset_x
    collision_rect_y = center_y - collision_height // 2 + collision_offset_y

    # Vérifier tous les pixels dans la zone de collision
    for i in range(collision_width):
        for j in range(collision_height):
            pixel_color = zoomed_collision.get_at((collision_rect_x + i, collision_rect_y + j))

            # MUR - Noir (0, 0, 0)
            if pixel_color == (0, 0, 0, 255):  
                return False  # Empêche le déplacement
            
            # Tu vérifies toujours si tu marches sur un pixel vert
            if pixel_color == (0, 255, 0, 255):
                # Tirer un nombre aléatoire entre 0 et 1
                if random.randint(0, 1000000) == 1000000 and moving:
                    # Si le nombre tiré est inférieur à la probabilité, un combat commence
                    slide_transition(screen, image2, battle_scene, grass)
                    return True

            # Combat aquatique - Bleu (0, 0, 255) : Lance une fonction de combat aquatique
            if pixel_color == (0, 0, 255, 255):
                # start_water_combat()
                return True

            # Déplacement vers le bas - Cyan (0, 255, 255) : Permet le déplacement vers le bas
            if pixel_color == (0, 255, 255, 255):
                if dy > 0:
                    return True  # Déplacement vers le bas autorisé
                else:
                    return False  # Bloque le déplacement vers le haut

            # Déplacement vers la gauche - Jaune (255, 255, 0) : Permet le déplacement vers la gauche
            if pixel_color == (255, 255, 0, 255):
                if dx < 0:
                    return True  # Déplacement vers la gauche autorisé
                else:
                    return False  # Bloque le déplacement vers la droite

            # Déplacement vers la droite - Magenta (255, 0, 255) : Permet le déplacement vers la droite
            if pixel_color == (255, 0, 255, 255):
                if dx > 0:
                    return True  # Déplacement vers la droite autorisé
                else:
                    return False  # Bloque le déplacement vers la gauche

    return True  # Aucune collision



# Variables pour l'animation
current_animation_frame = 0
current_direction = 'down'
animation_speed = 2  # Nombre de frames avant de changer de frame (ajustez pour fluidité)
frame_toggle = True  # Toggle entre deux images d'animation
animation_counter = 0  # Compteur pour alterner les frames d'animation

# Boucle principale
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches pour déplacer le joueur
    keys = pygame.key.get_pressed()

    # Déplacement et animation : basculer entre les images pendant que le joueur se déplace
    if keys[pygame.K_LEFT]:
        # Déplacement vers la gauche, vérifier par petits pas si le mouvement est possible
        for i in range(speed):
            if not check_collisions(-1, 0):  # Si collision, arrêter le déplacement
                break
            x -= 1
        current_direction = 'left'
        moving = True
    elif keys[pygame.K_RIGHT]:
        # Déplacement vers la droite, vérifier par petits pas si le mouvement est possible
        for i in range(speed):
            if not check_collisions(1, 0):  # Si collision, arrêter le déplacement
                break
            x += 1
        current_direction = 'right'
        moving = True
    elif keys[pygame.K_UP]:
        # Déplacement vers le haut, vérifier par petits pas si le mouvement est possible
        for i in range(speed):
            if not check_collisions(0, -1):  # Si collision, arrêter le déplacement
                break
            y -= 1
        current_direction = 'up'
        moving = True
    elif keys[pygame.K_DOWN]:
        # Déplacement vers le bas, vérifier par petits pas si le mouvement est possible
        for i in range(speed):
            if not check_collisions(0, 1):  # Si collision, arrêter le déplacement
                break
            y += 1
        current_direction = 'down'
        moving = True
    else:
        moving = False

    # Si le joueur se déplace, gérer l'animation
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        animation_counter += 1

        # Si le compteur atteint la vitesse d'animation, alterner l'animation
        if animation_counter >= animation_speed:
            animation_counter = 0  # Reset du compteur
            # Alterner entre les images de l'animation
            current_animation_frame = (current_animation_frame + 1) % 3  # Cycle entre 0, 1, 2 pour l'animation

    # Si le joueur ne bouge pas, garder l'image initiale de la direction
    elif not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
        if current_direction == 'down':
            current_animation_frame = 0
        elif current_direction == 'up':
            current_animation_frame = 0
        elif current_direction == 'right':
            current_animation_frame = 0
        elif current_direction == 'left':
            current_animation_frame = 0

    # Appliquer le zoom aux images
    zoomed_collision = zoom_image(collision_image, zoom)
    zoomed_map = zoom_image(map_image, zoom)
    zoomed_character = zoom_image(character_images[current_direction][current_animation_frame], zoom)

    zoomed_map_width, zoomed_map_height = zoomed_map.get_size()

    max_x = zoomed_map_width - character_images[current_direction][0].get_width()
    max_y = zoomed_map_height - character_images[current_direction][0].get_height()

    # Limiter la position du joueur pour qu'il ne sorte pas de la carte
    x = max(0, min(x, max_x))
    y = max(0, min(y, max_y))

    # Position de la caméra pour centrer le joueur
    camera_x = max(0, min(x - WIDTH // 2, zoomed_map_width - WIDTH))
    camera_y = max(0, min(y - HEIGHT // 2, zoomed_map_height - HEIGHT))
    zoomed_collision.set_alpha(128)

    # Dessiner la carte et le personnage
    screen.blit(zoomed_map, (-camera_x, -camera_y))
    # screen.blit(zoomed_collision, (-camera_x, -camera_y))
    screen.blit(zoomed_character, (x - camera_x, y - camera_y))

    pygame.display.update()

    pygame.time.Clock().tick(60)

pygame.quit()

pygame.quit()
sys.exit()