import pygame

#GAME WINDOW
SCREEN_WIDTH=800
SCREEN_HEIGHT=432

#define game variables
ROWS=8
MAX_COLS=24
TILE_SIZE=SCREEN_HEIGHT//ROWS
TILE_TYPES=13

#load images
#store tiles in a list
img_list=[]
for x in range(TILE_TYPES):
  img=pygame.image.load(f'Level_Editor/{x}.png')
  img=pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
  img_list.append(img)
  
class World():
  def __init__(self):
    self.obstacle_list=[]

  def process_data(self,data):
    #iterate through each value in level data file
    for y, row in enumerate(data):
      for x, tile in enumerate(row):
        if tile>=0:
          img=img_list[tile]
          img_rect=img.get_rect()
          img_rect.x=x*TILE_SIZE
          img_rect.y=y*TILE_SIZE
          tile_data=(img,img_rect)
          if tile>=0 and tile<=2 or tile>=8 and tile<=10:
            self.obstacle_list.append(tile_data)
          elif tile==11:
            pass#water
          elif tile >=4 and tile<=5 or tile==12:
            pass#decoration
          elif tile == 5:
            

          