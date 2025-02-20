# start pokedex add pokémon
import pygame
import sys



pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('image/background.png')
font = pygame.font.Font(None , 60)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


keepGameRunning = True
font_text = pygame.font.Font(None,40)
pygame.display.update()
def rect():
    rect1 = pygame.draw.rect(screen,(255, 255, 255), (350, 40, 300, 50), 2) 
    newgames= screen.blit(font_text.render('New Games', True, (255, 255, 255)),(430,50,100,100))
    rect2 = pygame.draw.rect(screen,(255, 255, 255), (350, 120, 300, 50), 2)
    quit= screen.blit(font_text.render('Quit', True, (255, 255, 255)),(470,130,100,100))
    rect3 = pygame.draw.rect(screen,(255, 255, 255), (350, 200, 300, 50), 2) 
    quit= screen.blit(font_text.render('Pokedex', True, (255, 255, 255)),(440,210,100,100))
while keepGameRunning:
        for event in pygame.event.get():
            screen.blit(background, (0,0))
            rect()
            pygame.display.update()
            pygame.display.flip()
            if event.type == pygame.QUIT:
                
                keepGameRunning = False
                pygame.quit()
sys.exit()
          