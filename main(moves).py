import pygame
import sys
import random
import time
from fight import main_fight
from menu import *

# Initializing Pygame
pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('pokemon')

# Load images
map_image = pygame.image.load('images/map.png')
collision_image = pygame.image.load('images/collisions.png')  # The invisible image for collisions

# Load character animation sprites (4 directions, 3 frames per direction)
character_images = {
    'down': [pygame.image.load('images/sheet/tile0.png'), pygame.image.load('images/sheet/tile1.png'), pygame.image.load('images/sheet/tile2.png')],
    'up': [pygame.image.load('images/sheet/tile3.png'), pygame.image.load('images/sheet/tile4.png'), pygame.image.load('images/sheet/tile5.png')],
    'right': [pygame.image.load('images/sheet/tile6.png'), pygame.image.load('images/sheet/tile7.png'), pygame.image.load('images/sheet/tile8.png')],
    'left': [pygame.image.load('images/sheet/tile9.png'), pygame.image.load('images/sheet/tile10.png'), pygame.image.load('images/sheet/tile11.png')]
}

# Map dimensions
map_width, map_height = map_image.get_size()

# Initial position of the player
x, y = 3455, 3530

# Movement speed
speed = 16

# Camera position
camera_x, camera_y = 0, 0

# Zoom factor
zoom = 3.0

"""-----VARIABLE DE TRANSITION-----"""
clock = pygame.time.Clock()

# Loading images
image1 = pygame.image.load("images/map.png")
image2 = pygame.image.load("images/noir.png")
battle_scene = pygame.image.load("images/battle_grass-resize (2).png")
grass = pygame.image.load("images/grass.png")
image1 = pygame.transform.scale(image1, (WIDTH, HEIGHT))
image2 = pygame.transform.scale(image2, (WIDTH, HEIGHT))
battle_scene = pygame.transform.scale(battle_scene, (WIDTH, HEIGHT))
grass = pygame.transform.scale(grass, (WIDTH, HEIGHT))

def capture_screen(): 
    screen.blit(zoomed_map, (-camera_x, -camera_y))
    image = pygame.Surface((1280, 750))  # Create an appropriately sized image area
    image.blit(screen, (0, 0))  #  Copy screen to this surface
    pygame.image.save(image, "screenshot.jpeg")  # Save image to disk
    return image  # Return captured surface

def slide_transition(screen, black_scene, battle_scene, grass):
    # Start animation
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

# Function to apply zoom on images
def zoom_image(image, factor):
    size = (int(image.get_width() * factor), int(image.get_height() * factor))
    return pygame.transform.scale(image, size)

# Function to check for collisions with invisible image
# Collision zone size
collision_width = 30  # Collision zone width
collision_height = 30  # Height of collision zone

# Collision offsets (centered by default)
collision_offset_x = 0  # Horizontal offset of the collision zone
collision_offset_y = 20  # Vertical offset of the collision zone

def check_collisions(dx=0, dy=0):
    """ Vérifie la couleur dans la zone de collision centrée autour du joueur. """
    future_x = x + dx
    future_y = y + dy

    # Calculate the center of the collision zone
    center_x = future_x + zoomed_character.get_width() // 2
    center_y = future_y + zoomed_character.get_height() // 2

    # Set the coordinates of the upper left corner of the collision zone
    collision_rect_x = center_x - collision_width // 2 + collision_offset_x
    collision_rect_y = center_y - collision_height // 2 + collision_offset_y

    # Check all pixels in collision area
    for i in range(collision_width):
        for j in range(collision_height):
            pixel_color = zoomed_collision.get_at((collision_rect_x + i, collision_rect_y + j))

            if pixel_color == (0, 0, 0, 255):  
                return False  # Prevents movement
            
            if pixel_color == (0, 255, 0, 255):
                # Draw a random number between 0 and 1000000
                if random.randint(0, 1000000) == 1000000 and moving:
                    # If the number drawn is above than the probability, a fight begins
                    slide_transition(screen, image2, battle_scene, grass)
                    return True

            if pixel_color == (0, 0, 255, 255):
                return False  # Prevents movement

            if pixel_color == (0, 255, 255, 255):
                if dy > 0:
                    return True  # Downward movement allowed
                else:
                    return False  # Blocks upward movement

            if pixel_color == (255, 255, 0, 255):
                if dx < 0:
                    return True  # Left movement allowed
                else:
                    return False  # Blocks moving to the right

            if pixel_color == (255, 0, 255, 255):
                if dx > 0:
                    return True  # Right movement allowed
                else:
                    return False  # Blocks moving to the left

    return True  # No collision



# Variables for animation
current_animation_frame = 0
current_direction = 'down'
animation_speed = 2  # Number of frames before changing frames
frame_toggle = True  # Toggle between two animation frames
animation_counter = 0  # Counter to alternate animation frames

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key management to move the player
    keys = pygame.key.get_pressed()

    # Movement and animation: switch between frames while the player moves
    if keys[pygame.K_LEFT]:
        # Moving to the left, check in small steps if movement is possible
        for i in range(speed):
            if not check_collisions(-1, 0):  # If collision, stop moving
                break
            x -= 1
        current_direction = 'left'
        moving = True
    elif keys[pygame.K_RIGHT]:
        # Moving to the right, check in small steps if movement is possible
        for i in range(speed):
            if not check_collisions(1, 0):  # If collision, stop moving
                break
            x += 1
        current_direction = 'right'
        moving = True
    elif keys[pygame.K_UP]:
        # Moving upwards, check in small steps if movement is possible
        for i in range(speed):
            if not check_collisions(0, -1):  # If collision, stop moving
                break
            y -= 1
        current_direction = 'up'
        moving = True
    elif keys[pygame.K_DOWN]:
        # Moving downwards, check in small steps if movement is possible
        for i in range(speed):
            if not check_collisions(0, 1):  # If collision, stop moving
                break
            y += 1
        current_direction = 'down'
        moving = True
    else:
        moving = False

    # If the player moves, manage the animation
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        animation_counter += 1

        # If the counter reaches the animation speed, alternate the animation
        if animation_counter >= animation_speed:
            animation_counter = 0  # Counter reset
            # Switch between animation frames
            current_animation_frame = (current_animation_frame + 1) % 3  # Cycle between 0, 1, 2 for animation

    # If the player does not move, keep the initial image of the direction
    elif not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
        if current_direction == 'down':
            current_animation_frame = 0
        elif current_direction == 'up':
            current_animation_frame = 0
        elif current_direction == 'right':
            current_animation_frame = 0
        elif current_direction == 'left':
            current_animation_frame = 0

    # Apply zoom to images
    zoomed_collision = zoom_image(collision_image, zoom)
    zoomed_map = zoom_image(map_image, zoom)
    zoomed_character = zoom_image(character_images[current_direction][current_animation_frame], zoom)

    zoomed_map_width, zoomed_map_height = zoomed_map.get_size()

    max_x = zoomed_map_width - character_images[current_direction][0].get_width()
    max_y = zoomed_map_height - character_images[current_direction][0].get_height()

    # Limit the player's position so that he does not leave the map
    x = max(0, min(x, max_x))
    y = max(0, min(y, max_y))

    # Camera position to center the player
    camera_x = max(0, min(x - WIDTH // 2, zoomed_map_width - WIDTH))
    camera_y = max(0, min(y - HEIGHT // 2, zoomed_map_height - HEIGHT))
    zoomed_collision.set_alpha(128)

    # Draw the map and the character
    screen.blit(zoomed_map, (-camera_x, -camera_y))
    screen.blit(zoomed_character, (x - camera_x, y - camera_y))

    pygame.display.update()

    pygame.time.Clock().tick(60)

pygame.quit()

pygame.quit()
sys.exit()