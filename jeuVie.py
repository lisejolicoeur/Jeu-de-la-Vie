import pygame
import math
import time
import sys

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE = (0,0,255)

TOUR = 0
voisins = 0

width  = 20
height = 20
screen_w = 1200
screen_h = 600
margin = 40

pygame.init()
pygame.font.init()
pygame.display.set_caption('Jeu de la vie')

##Texte##
init = pygame.font.Font(None, 30)
textRectGo = init.render('Go !', False, BLACK)
textRectStop = init.render('Stop', False, BLACK)
textRectClear = init.render('Clear', False, BLACK)
tours = init.render(str(TOUR), False, RED)

##Fenetre##
size = [screen_w, screen_h+margin] #margin for the button
screen = pygame.display.set_mode(size)
screen.fill(WHITE)

##GRID##
grid = [[0 for i in range(0,int(screen_h/height))] for j in range(0,int(screen_w/width))]

#dessins ------------------------------
for i in range(0,screen_w,width):
   pygame.draw.line(screen,BLACK, (i,0),(i,screen_h),1)
for j in range(0,screen_h,height):
   pygame.draw.line(screen,BLACK, (0,j),(screen_w,j),1) 

#boutons
pygame.draw.rect(screen, GREEN, (screen_w/4, screen_h+margin/4,80,margin/2))
pygame.draw.rect(screen, RED, (screen_w/2, screen_h+margin/4,80,margin/2))
pygame.draw.rect(screen, BLUE, (10, screen_h+margin/4,80,margin/2))

#texte sur les boutons
screen.blit(textRectGo, (screen_w/4+20, screen_h+margin/4))
screen.blit(textRectStop, (screen_w/2+20, screen_h+margin/4))
screen.blit(textRectClear, (25, screen_h+margin/4))
screen.blit(tours, (screen_w - 80, screen_h+margin/4))

pygame.display.update()

#--------------------------------------------------------------------------
#enlever les cellules vivantes existantes
def clear():
   for i in range(0,int(screen_w/width)):
      for j in range(0,int(screen_h/height)):
         grid[i][j] = 0
   pygame.draw.rect(screen, WHITE, (screen_w-80,screen_h+margin/4,80,margin/2))
   tours = init.render(str(TOUR), False, RED)
   screen.blit(tours, (screen_w - 80, screen_h+margin/4))
   pygame.display.update()
   
#processus d'évolution de la population
def lancer_evolution():
   global TOUR, voisins,grid
   print("Evolution en cours...")
   over = False
   while(not over):
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
           pos = pygame.mouse.get_pos()
           if(screen_w/2 < pos[0] < screen_w/2 + 80 and screen_h+margin/4 < pos[1] < screen_h+3*margin/4):
               over = True
               TOUR = 0
               break
      if(over):
         continue
	  #update cellules	
      newgrid = [[0 for i in range(0,int(screen_h/height))] for j in range(0,int(screen_w/width))]
      for i in range(0,int(screen_w/width)):
         for j in range(0,int(screen_h/height)):
            voisins = 0
            if(j<screen_h/height-1):
               voisins += 1 if grid[i][j+1] == 1 else 0
            if(j>0):
               voisins += 1 if grid[i][j-1] == 1 else 0
            if(i>0):
               voisins += 1 if grid[i-1][j] == 1 else 0
               if(j<screen_h/height-1):
                  voisins += 1 if grid[i-1][j+1] == 1 else 0
               if(j>0):	  
                  voisins += 1 if grid[i-1][j-1] == 1 else 0
            if(i<screen_w/width-1):
               voisins += 1 if grid[i+1][j] == 1 else 0
               if(j<screen_h/height-1):
                  voisins += 1 if grid[i+1][j+1] == 1 else 0
               if(j>0):
                  voisins += 1 if grid[i+1][j-1] == 1 else 0
            
            if(grid[i][j] == 0 and voisins==3):
               newgrid[i][j] = 1
            else:
               newgrid[i][j] = 0
            if(grid[i][j] == 1):
               if(voisins<2 or voisins>3):
                  newgrid[i][j] = 0
               else:
                  newgrid[i][j] = 1

      grid = newgrid.copy()	   
	  #redessiner la grille pour ajouter les cases noires qui sont notées "1"
      for i in range(0,int(screen_w/width)):
         for j in range(0,int(screen_h/height)):
            if(grid[i][j] == 1):
               pygame.draw.rect(screen, BLACK, (20*i+1,20*j+1,19,19))
            else :
               pygame.draw.rect(screen, WHITE, (20*i+1,20*j+1,19,19))
      TOUR += 1
      pygame.draw.rect(screen, WHITE, (screen_w-80,screen_h+margin/4,80,margin/2))
      tours = init.render(str(TOUR), False, RED)
      screen.blit(tours, (screen_w - 80, screen_h+margin/4))
      #time.sleep(1)
      pygame.display.update()

#initialisation du jeu et fonction principale du jeu
def initialisation():
   global TOUR, grid
   print("#####Initialisation#####")
   print("Vous pouvez maintenant placez des cellules, les enlever et lancer l'évolution. ")
   while(True):
      for event in pygame.event.get():
         if (event.type == pygame.QUIT):
            sys.exit()
         if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if(screen_w/4 < pos[0] < screen_w/4 +80 and screen_h+margin/4 < pos[1] < screen_h+3*margin/4):
               lancer_evolution()
               print("#####Initialisation#####")
               print("Vous pouvez maintenant placez des cellules, les enlever et lancer l'évolution. ")
            if(10 < pos[0] < 80 and screen_h+margin/4 < pos[1] < screen_h+3*margin/4):
               clear()
            if(TOUR == 0 and 0 < pos[1] < screen_h):
               x = 	math.floor((pos[0]/20))
               y = 	math.floor((pos[1]/20))
               grid[x][y] = 1		
     
	  
	  #redessiner la grille pour ajouter les cases noires qui sont notées "1"
      for i in range(0,int(screen_w/width)):
         for j in range(0,int(screen_h/height)):
            if(grid[i][j] == 1):
               pygame.draw.rect(screen, BLACK, (20*i+1,20*j+1,19,19))
            else :
              pygame.draw.rect(screen, WHITE, (20*i+1,20*j+1,19,19))
				
      pygame.display.update()
	  
# lancer le jeu
print("######Jeu de la vie######")
print("Placez des cellules vivantes en cliquant sur les cases de la grille et lancez ensuite le processus d'évolution ! ")
initialisation()
pygame.quit()