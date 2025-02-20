import pygame
import sys



pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('image/interfacecombat1.png')
font = pygame.font.Font(None , 60)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


font_text = pygame.font.Font(None,40)

def rect():
    button= pygame.draw.rect(screen,(255, 255, 255),(720,700, 280,50),)
    button = pygame.draw.rect(screen,(0, 0, 0),(720,700, 280,50), 2)
    newgames= screen.blit(font_text.render('Pokemon', True, (0, 0, 0)),(800,710,100,100))
    button2 = pygame.draw.rect(screen,(255, 255, 255),(1000,700, 280,50))
    button2 = pygame.draw.rect(screen,(0, 0, 0),(1000,700, 280,50), 2)
    newgames= screen.blit(font_text.render('Run', True, (0, 0, 0)),(1120,710,100,100))
    button3 = pygame.draw.rect(screen,(255, 255, 255),(1000,650, 280,50))
    button3 = pygame.draw.rect(screen,(0, 0, 0),(1000,650, 280,50), 2)
    newgames= screen.blit(font_text.render('Bag', True, (0, 0, 0)),(1120,660,100,100))
    button4 = pygame.draw.rect(screen,(255, 255, 255),(720,650, 280,50))
    button4 = pygame.draw.rect(screen,(0, 0, 0),(720,650, 280,50), 2)
    newgames= screen.blit(font_text.render('Attack', True, (0, 0, 0)),(810,660,100,100))
    chatbutton = pygame.draw.rect(screen,(57, 58, 58),(0,650, 720,100))
    chatbutton = pygame.draw.rect(screen,(255, 255, 255),(0,650, 720,100), 4)
         
            
    pygame_instance = pygame

pygame.display.update()
keepGameRunning = True

while keepGameRunning:
    for event in pygame.event.get():
          screen.blit(background, (0, 0))
          rect()
          
          pygame.display.update()
          pygame.display.flip()
          
          
          if event.type == pygame.QUIT:
                keepGameRunning = False
                
                if event.type == pygame.KEYDOWN:
                     

                    pygame.quit()
            
    

# pygame.display()
sys.exit()