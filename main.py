#Name:Yaryna
#Date:Oct 18
#Fox adventure
#Create a kids scroller game

#import lybraries
import pygame
import csv
import Animals as a
import Button as b
import Items as e
import HealthAndFood as h

pygame.init()

#set framerate
clock = pygame.time.Clock()
FPS = 60


#define colors
BLACK=((0,0,0))
WHITE=((240,255,240))

#define font
font = pygame.font.SysFont('Futura', 30)

#define player action variables
game_paused = False
game_menu = True
menu_state = "main"
moving_left = False
moving_right = False
start_game=False

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fox")

#define game variables
GRAVITY = 0.4
scroll = 0
SCROLL_THRESH=200
ROWS=8
COLS=24
TILE_SIZE=SCREEN_HEIGHT//ROWS
level=1
screen_scroll=0

TILE_TYPES=13

#load button images
start_img = pygame.image.load('Images/Buttons/button_start.png')
exit_img = pygame.image.load('Images/Buttons/button_exit.png')
pause_img = pygame.image.load('Images/Buttons/button_pause.png')
resume_img = pygame.image.load("Images/Buttons/button_resume.png")
options_img = pygame.image.load("Images/Buttons/button_options.png")
quit_img = pygame.image.load("Images/Buttons/button_quit.png")
video_img = pygame.image.load('Images/Buttons/button_video.png')
audio_img = pygame.image.load('Images/Buttons/button_audio.png')
keys_img = pygame.image.load('Images/Buttons/button_keys.png')
back_img = pygame.image.load('Images/Buttons/button_back.png')

#create button instances
start_button = b.Button(100, 50, start_img, 2)
exit_button = b.Button(100, 200, exit_img, 0.8)
pause_button = b.Button(SCREEN_WIDTH-50, 10, pause_img, 0.7)
resume_button = b.Button(100, 50, resume_img, 1)
options_button = b.Button(100, 150, options_img, 1)
quit_button = b.Button(100, 250, quit_img, 1)
video_button = b.Button(427, 25, video_img, 1)
audio_button = b.Button(425, 125, audio_img, 1)
keys_button = b.Button(467, 225, keys_img, 1)
back_button = b.Button(640, 325, back_img, 1)

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
            water=Water(img, x*TILE_SIZE, y*TILE_SIZE)
            water_group.add(water)
          elif tile >=4 and tile<=5 or tile==12:
            decoration=Decoration(img, x*TILE_SIZE, y*TILE_SIZE)
            decoration_group.add(decoration)
          elif tile == 5:
            item=e.Item('Mulberry', x*TILE_SIZE, y*TILE_SIZE)
            items_group.add(item)
          elif tile == 6:
            item=e.Item('Peanuts', x*TILE_SIZE, y*TILE_SIZE)
            items_group.add(item)
          elif tile==7:
            item=e.Item('Raspberry', x*TILE_SIZE, y*TILE_SIZE)
            items_group.add(item)
          elif tile==4:#create exit
            exit=Exit(img, x*TILE_SIZE, y*TILE_SIZE)
            exit_group.add(exit)

  def draw(self):
    for tile in self.obstacle_list:
      tile[1][0]+=screen_scroll
      screen.blit(tile[0], tile[1])

  

class Decoration(pygame.sprite.Sprite):
  def __init__(self,img,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image=img
    self.rect=self.image.get_rect()
    self.rect.midtop=(x*TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))

  def update(self):
    self.rect.x+=screen_scroll

class Water(pygame.sprite.Sprite):
  def __init__(self,img,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image=img
    self.rect=self.image.get_rect()
    self.rect.midtop=(x*TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))

  def update(self):
    self.rect.x+=screen_scroll

class Exit(pygame.sprite.Sprite):
  def __init__(self,img,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image=img
    self.rect=self.image.get_rect()
    self.rect.midtop=(x*TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))

  def update(self):
    self.rect.x+=screen_scroll
      
            
#load background images
ground_image = pygame.image.load("Images/Parallax/ground.png")
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"Images/Parallax/plx-{i}.png")
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


#drawing background      
def draw_bg():
    for x in range(5):
        speed = 0.5
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2

#drawing ground
def draw_ground():
    for x in range(15):
        screen.blit(
            ground_image,
            ((x * ground_width) - scroll * 2, SCREEN_HEIGHT - ground_height))



def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


      
#creating sprite groups
items_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


fox = a.Animals('Fox', 200, 200, 0.55, 7)
health_bar = h.Bar(10, 10, fox.health, fox.health)
food_bar = h.Bar(10,40,fox.food, fox.max_food)

#create empty tile_list
world_data=[]
for row in range(ROWS):
  r=[-1]*COLS
  world_data.append(r)

#load in level data and create world
with open (f'level{level}_data.csv', newline='') as csvfile:
  reader=csv.reader(csvfile,delimiter=',')
  for x, row in enumerate(reader):
    for y, tile in enumerate(row):
      world_data[x][y]=int(tile)
world=World()
world.process_data(world_data)


#game loop
run = True
while run:
            
        clock.tick(FPS)
        
        #draw world
        draw_bg()
        #draw world map
        world.draw()
        
        #draw_ground()
        #show player health
        health_bar.draw(fox.health, screen)
        food_bar.draw(fox.food,screen)
        
        #show bars
        draw_text('Health',font,BLACK,25,11)
        draw_text('Food ', font, BLACK, 25, 41)
      
        if pause_button.draw(screen):
            game_paused = True
        #check if game is paused
      
        fox.update_animation()
        fox.draw(screen)
        fox.move(moving_left, moving_right, SCREEN_HEIGHT,SCREEN_WIDTH,world,SCROLL_THRESH)

          
        #update and draw groups
        decoration_group.update()
        water_group.update()
        exit_group.update()
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
        items_group.update(fox, screen_scroll)
        items_group.draw(screen)
      
        #update player actions
        if fox.alive:
          if fox.in_air:
            fox.update_action(2)#2: jump
          elif fox.attack:
            fox.update_action(5)#5: attack
          elif fox.crouch:
            if moving_left or moving_right:
              fox.update_action(3)#3: crouch
            else:
              fox.update_action(4)#4: crouch idle
          elif not fox.crouch:
            if moving_left or moving_right:
              fox.update_action(1)#1: run
            else:
              fox.update_action(0)#0: idle
          screen_scroll=fox.move(moving_left, moving_right, SCREEN_HEIGHT,SCREEN_WIDTH,world,SCROLL_THRESH)

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and scroll > 0:
            scroll -= 5
        if key[pygame.K_RIGHT] and scroll < 2000:
            scroll += 5
            

        #event handlers
        for event in pygame.event.get():
          
    		#quit game
          if event.type == pygame.QUIT:
            run = False
            
    		#keyboard presses
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
              moving_left = True
            if event.key == pygame.K_RIGHT:
              moving_right = True
            if event.key == pygame.K_DOWN:
              fox.crouch = True
            if event.key == pygame.K_UP:
              fox.crouch = False
            if event.key == pygame.K_RCTRL:
              fox.attack = True
            if event.key == pygame.K_SPACE and fox.alive:
              fox.jump = True
            if event.key == pygame.K_ESCAPE:
              run = False
            
    
    
    		#keyboard button released
          if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
              moving_left = False
            if event.key == pygame.K_RIGHT:
              moving_right = False

        pygame.display.update()

pygame.quit()