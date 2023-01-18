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

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432
LOWER_MARGIN=100
SIDE_MARGIN=300

screen=pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption("Fox")

#define game variables
GRAVITY = 0.4
scroll = 0
SCROLL_THRESH=100
ROWS=8
COLS=24
MAX_COLS=24
TILE_SIZE=SCREEN_HEIGHT//ROWS
scroll_speed=1
current_tile=0
level=1
screen_scroll=0
level_editor=False
TILE_TYPES=13

#define player action variables
game_paused = False
game_menu = True
menu_state = "main"
moving_left = False
moving_right = False
start_game=False

#define colors
BLACK=((0,0,0))
WHITE=((240,255,240))
GREEN=((107,255,185))
RED=((200, 25, 25))


#define font
font = pygame.font.SysFont('Futura', 30)
font1 = pygame.font.SysFont('Futura',70)

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
level_editor_img = pygame.image.load('Images/Buttons/button_level-editor.png')
save_img=pygame.image.load("Images/Buttons/save.png")
load_img=pygame.image.load("Images/Buttons/load.png")
back_lvl_img=pygame.image.load("Images/Buttons/back.png")
main_menu_img=pygame.image.load("Images/Buttons/button_main-menu.png")

#store tiles in a list
img_list=[]
for x in range(TILE_TYPES):
  img=pygame.image.load(f'Images/Level_Editor/{x}.png')
  img=pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
  img_list.append(img)


#create button instances
start_button = b.Button(100, 50, start_img, 1)
exit_button = b.Button(100, 350, exit_img, 1)
pause_button = b.Button(SCREEN_WIDTH+SIDE_MARGIN-50, 10, pause_img, 0.7)
resume_button = b.Button(100, 50, resume_img, 1)
options_button = b.Button(100, 150, options_img, 1)
quit_button = b.Button(100, 250, quit_img, 1)
video_button = b.Button(427, 25, video_img, 1)
audio_button = b.Button(420, 125, audio_img, 1)
keys_button = b.Button(450, 225, keys_img, 1)
back_button = b.Button(560, 325, back_img, 1)
level_editor_button = b.Button(100, 250, level_editor_img, 1)
save_button=b.Button(SCREEN_WIDTH//2, SCREEN_HEIGHT+LOWER_MARGIN-90, save_img,1.5)
load_button=b.Button(SCREEN_WIDTH//2+200, SCREEN_HEIGHT+LOWER_MARGIN-90, load_img,1.5)
back_lvl_button=b.Button(SCREEN_WIDTH//2+400, SCREEN_HEIGHT+LOWER_MARGIN-90, back_lvl_img,1.5)
main_menu_button=b.Button(330, 50, main_menu_img, 1)

#make a button list
button_list=[]
button_col=0
button_row=0
for i in range(len(img_list)):
  tile_button=b.Button(SCREEN_WIDTH+(75*button_col)+50,75*button_row+50,img_list[i],1)
  button_list.append(tile_button)
  button_col+=1
  if button_col == 3:
    button_row+=1
    button_col=0

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
def draw_bg(color):
    screen.fill(color)
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

#draw grid
def draw_grid():
  #vertical lines
  for c in range(MAX_COLS+1):
    pygame.draw.line(screen,WHITE,(c*TILE_SIZE-scroll,0),(c*TILE_SIZE-scroll, SCREEN_HEIGHT))
  #horizontal lines
  for c in range(ROWS+1):
    pygame.draw.line(screen,WHITE,(0,c*TILE_SIZE),(SCREEN_WIDTH, c*TILE_SIZE))
      
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

#create ground
for tile in range (0,MAX_COLS):
  world_data[ROWS-1][tile]=0


#function for drawing the world tiles
def draw_world():
  for y, row in enumerate(world_data):
    for x, tile in enumerate(row):
      if tile>=0:
        screen.blit(img_list[tile],(x*TILE_SIZE-scroll,y* TILE_SIZE))

        
#load in level data and create world
def load():
  with open (f'level{level}_data.csv', newline='') as csvfile:
    reader=csv.reader(csvfile,delimiter=',')
    for x, row in enumerate(reader):
      for y, tile in enumerate(row):
        world_data[x][y]=int(tile)

#save level data
def save():
  with open(f'level{level}_data.csv','w', newline='') as csvfile:
    writer=csv.writer(csvfile, delimiter=',')
    for row in world_data:
      writer.writerow(row)

load()
world=World()
world.process_data(world_data)


#game loop
run = True
while run:
  clock.tick(FPS)
  if not start_game and not level_editor:
      screen.fill((202, 241, 202))
      if start_button.draw(screen):
  	 	  start_game=True
      if level_editor_button.draw(screen):
        level_editor=True
      if options_button.draw(screen):
        game_paused=True
        menu_state = "options"
      if exit_button.draw(screen):
        run=False
  if level_editor:
    draw_bg(GREEN)
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, BLACK, 10, SCREEN_HEIGHT+LOWER_MARGIN-90)
    draw_text('Press UP or DOWN to change level', font, BLACK, 10, SCREEN_HEIGHT+LOWER_MARGIN-60)

    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
      level += 1
    if key[pygame.K_DOWN] and level>1:
      level -= 1

    #save and load data
    if save_button.draw(screen):
      save()

    if load_button.draw(screen):
    #load in level data
    #reset scroll back to the start of the level
      scroll=0
      load()
        
    if back_lvl_button.draw(screen):
      level_editor=False
      start_game=False

    #draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH,0,SIDE_MARGIN,SCREEN_HEIGHT))

     #choose a tile_button
    button_count=0
    for button_count, i in enumerate(button_list):
      if i.draw(screen):
        current_tile=button_count

    #highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    #get keypresses
    #key = pygame.key.get_pressed()
   # scroll_speed=1
   # if key[pygame.K_LEFT] and scroll > 0:
   #   scroll -= 5*scroll_speed
    #if key[pygame.K_RIGHT] and scroll < (MAX_COLS*TILE_SIZE)-SCREEN_WIDTH:
    #  scroll += 5*scroll_speed
    

      #add new tiles to the screen
    #get mouse position
    pos=pygame.mouse.get_pos()
    x=(pos[0]+scroll)//TILE_SIZE
    y=pos[1]//TILE_SIZE
  
    #check that the coordinates are within the tile area
    if pos[0]<SCREEN_WIDTH and pos[1]<SCREEN_HEIGHT:
      #update tile value
      if pygame.mouse.get_pressed()[0]==1:
        if world_data[y][x]!= current_tile:
          world_data[y][x] = current_tile
      if pygame.mouse.get_pressed()[2]==1:
          world_data[y][x] = -1
  
    #check if game is paused
  if game_paused:
        screen.fill((160, 255, 255))
        #check menu state
        if menu_state == "main":
          #draw pause screen buttons
          if resume_button.draw(screen):
            game_paused = False
            start_game=True
          if options_button.draw(screen):
            menu_state = "options"
          if main_menu_button.draw(screen):
            game_paused=False
            start_game=False
          if quit_button.draw(screen):
            run = False
        #check if the options menu is open
        if menu_state == "options":
          #draw the different options buttons
          if video_button.draw(screen):
            menu_state='video'
          if audio_button.draw(screen):
            menu_state='audio'
          if keys_button.draw(screen):
            menu_state='keys'
          if back_button.draw(screen):
            menu_state = "main"
        if menu_state=='video':
          draw_text("Video Settings",font1,BLACK,SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2-50)
          if back_button.draw(screen):
            menu_state = "options"
        if menu_state=='audio':
          draw_text("Audio Settings",font1,BLACK,SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2-50)
          if back_button.draw(screen):
            menu_state = "options"
        if menu_state=='keys':
          draw_text("Change Key Bindings",font1,BLACK,SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2-50)
          if back_button.draw(screen):
            menu_state = "options"
  elif start_game and not game_paused:
        
        #draw world
        draw_bg(BLACK)
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
        if key[pygame.K_RIGHT] and scroll < (MAX_COLS*TILE_SIZE)-SCREEN_WIDTH:
            scroll += 5
            

        #event handlers
  for event in pygame.event.get():
          
    		#quit game
          if event.type == pygame.QUIT:
            run = False
            
    		#keyboard presses
          if event.type == pygame.KEYDOWN and not game_paused and start_game or event.type==pygame.KEYDOWN and level_editor:
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
              game_paused=True
            
    
    
    		#keyboard button released
          if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
              moving_left = False
            if event.key == pygame.K_RIGHT:
              moving_right = False

  pygame.display.update()

pygame.quit()