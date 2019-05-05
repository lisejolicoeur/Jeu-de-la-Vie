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

carre = 10
screen_w = 1200
screen_h = 600
margin = 40
nb_lignes = int(screen_h/carre)
nb_col = int(screen_w/carre)

pygame.init()
pygame.font.init()
pygame.display.set_caption('Jeu de la vie')

##Texte##
init = pygame.font.Font(None, 30)
textRectGo = init.render('Lancer !', False, BLACK)
textRectStop = init.render('Stop', False, BLACK)
textRectClear = init.render('Clear', False, BLACK)
tours = init.render(str(TOUR), False, RED)

##Fenetre##
size = [screen_w, screen_h+margin] #margin for the button
screen = pygame.display.set_mode(size)
screen.fill(WHITE)

##GRID##
grid = [[0 for i in range(0,nb_lignes)] for j in range(0,nb_col)]

#dessins ------------------------------
for i in range(0,screen_w,carre):
   pygame.draw.line(screen,BLACK, (i,0),(i,screen_h),1)
for j in range(0,screen_h,carre):
   pygame.draw.line(screen,BLACK, (0,j),(screen_w,j),1) 

#boutons
pygame.draw.rect(screen, GREEN, (screen_w/4, screen_h+margin/4,100,margin/2))
pygame.draw.rect(screen, RED, (screen_w/2, screen_h+margin/4,80,margin/2))
pygame.draw.rect(screen, BLUE, (10, screen_h+margin/4,80,margin/2))

#texte sur les boutons
screen.blit(textRectGo, (screen_w/4+5, screen_h+margin/4))
screen.blit(textRectStop, (screen_w/2+20, screen_h+margin/4))
screen.blit(textRectClear, (25, screen_h+margin/4))
screen.blit(tours, (screen_w - 80, screen_h+margin/4))

pygame.display.update()

#--------------------------------------------------------------------------
#enlever les cellules vivantes existantes
def clear():
   for i in range(0,nb_col):
      for j in range(0,nb_lignes):
         grid[i][j] = 0
   pygame.draw.rect(screen, WHITE, (screen_w-80,screen_h+margin/4,80,margin/2))
   tours = init.render(str(TOUR), False, RED)
   screen.blit(tours, (screen_w - 80, screen_h+margin/4))
   pygame.display.update()
   
###fonction pour trouver le nombre de voisins en vie d'une cellule passée en paramètres
def nombre_voisins(i,j):
   global grid
   voisins = 0
   if(j<nb_lignes-1):
      voisins += 1 if grid[i][j+1] == 1 else 0
   if(j>0):
      voisins += 1 if grid[i][j-1] == 1 else 0
   if(i>0):
      voisins += 1 if grid[i-1][j] == 1 else 0
      if(j<nb_lignes-1):
         voisins += 1 if grid[i-1][j+1] == 1 else 0
      if(j>0):	  
         voisins += 1 if grid[i-1][j-1] == 1 else 0
   if(i<nb_col-1):
      voisins += 1 if grid[i+1][j] == 1 else 0
      if(j<nb_lignes-1):
         voisins += 1 if grid[i+1][j+1] == 1 else 0
      if(j>0):
         voisins += 1 if grid[i+1][j-1] == 1 else 0
   return voisins

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
		 
	  ##Une étape de l'évolution##----------------------
      newgrid = [[0 for i in range(0,nb_lignes)] for j in range(0,nb_col)]
	  
	  #mettre à jour la nouvelle grille
      for i in range(0,nb_col):
         for j in range(0,nb_lignes):
            voisins = nombre_voisins(i,j)
            if(grid[i][j] == 0 and voisins==3):
               newgrid[i][j] = 1
            else:
               newgrid[i][j] = 0
			 
            if(grid[i][j] == 1):
               if(voisins<2 or voisins>3):
                  newgrid[i][j] = 0
               else:
                  newgrid[i][j] = 1
      
	  #utiliser la nouvelle grille
      grid = newgrid.copy()	   
	  #redessiner la grille pour ajouter les cases noires qui sont notées "1"
      for i in range(0,nb_col):
         for j in range(0,nb_lignes):
            if(grid[i][j] == 1):
               pygame.draw.rect(screen, BLACK, (carre*i+1,carre*j+1,carre-1,carre-1))
            else :
               pygame.draw.rect(screen, WHITE, (carre*i+1,carre*j+1,carre-1,carre-1))
      
      TOUR += 1
	  #mettre à jour le nombre de tours
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
			#action d'ajouter une cellule vivante sur la grille
            if(0 < pos[1] < screen_h):
               x = 	math.floor((pos[0]/carre))
               y = 	math.floor((pos[1]/carre))
               grid[x][y] = (grid[x][y] + 1)%2	
	  #redessiner la grille pour ajouter les cases noires qui sont notées "1"
      for i in range(0,nb_col):
         for j in range(0,nb_lignes):
            if(grid[i][j] == 1):
               pygame.draw.rect(screen, BLACK, (carre*i+1,carre*j+1,carre-1,carre-1))
            else :
              pygame.draw.rect(screen, WHITE, (carre*i+1,carre*j+1,carre-1,carre-1))
				
      pygame.display.update()
	  
# lancer le jeu
print("######Jeu de la vie######")
print("Placez des cellules vivantes en cliquant sur les cases de la grille et lancez ensuite le processus d'évolution ! ")
initialisation()
pygame.quit()