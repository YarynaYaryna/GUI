import pygame, os
import random

GRAVITY=0.6
RED=((255, 66, 79))
TILE_SIZE=40

class Animals(pygame.sprite.Sprite):
  def __init__(self, char_type, x, y, scale, speed):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.health = 100
    self.max_health = self.health
    self.food=0
    self.max_food = 100
    self.char_type = char_type
    self.speed = speed
    self.direction = 1
    self.vel_y = 0
    self.jump = False
    self.in_air = True
    self.crouch = False
    self.attack = False
    self.flip = False
    self.animation_list = []
    self.frame_index = 0
    self.action = 0
    self.update_time = pygame.time.get_ticks()
    #ai specific variables
    self.move_counter=0
    self.vision=pygame.Rect(0,0,150,20)
    self.idling=False
    self.idle_counter=0
    
    
    #load all images for the players
    animation_types = ['Idle', 'Run', 'Jump', 'Crouch', 'Crouch_idle', 'Attack','Death']
    for animation in animation_types:
  		#reset temporary list of images
      temp_list = []
  		#count number of files in the folder
      num_of_frames = len(os.listdir(f'Images/{self.char_type}/{animation}'))
      for i in range(num_of_frames):
        img = pygame.image.load(f'Images/{self.char_type}/{animation}/{i}.png')
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        temp_list.append(img)
      self.animation_list.append(temp_list)
  
    self.image = self.animation_list[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.width=self.image.get_width()
    self.height=self.image.get_height()

  def update(self):
    self.update_animation()
    self.check_alive()

  def move(self, moving_left, moving_right, SCREEN_HEIGHT, SCREEN_WIDTH, world, SCROLL_THRESH):
		#reset movement variables
    screen_scroll=0
    dx=0
    dy=0

		#assign movement variables if moving left or right
    if moving_left:
      dx = -self.speed
      self.flip = True
      self.direction = -1
    if moving_right:
      dx = self.speed
      self.flip = False
      self.direction = 1

    #attack
      if self.attack:
        self.attack=False
        
		#jump
    if self.jump == True and self.in_air == False:
      self.vel_y = -11
      self.jump = False
      self.in_air = True

		#apply gravity
    self.vel_y += GRAVITY
    if self.vel_y > 10:
      self.vel_y
    dy += self.vel_y

		#check for collision
    for tile in world.obstacle_list:
      #check collision in x direction
      if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
        dx=0
      #check collision in y direction
      if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
        #check if below the ground
        if self.vel_y<0:
          self.vel_y=0
          dy=tile[1].bottom-self.rect.top
          self.in_air=False
        #check if above the ground
        elif self.vel_y>=0:
          self.vel_y=0
          dy=tile[1].top-self.rect.bottom
          self.in_air=False
          

		#update rectangle position
    self.rect.x += dx
    self.rect.y += dy

    #update scroll based on player position
    if self.char_type=='Fox':
      if self.rect.right>SCREEN_WIDTH-SCROLL_THRESH or self.rect.left<SCROLL_THRESH:
        self.rect.x-=dx
        screen_scroll=-dx

    return screen_scroll

  def ai(self, player, SCREEN_HEIGHT):
    if self.alive and player.alive:

      if self.idling == False and random.randint(1,200)==1:
        self.update_action(4)#0: idle
        self.idling=True
        self.idle_counter=50
        #check if the ai in near the player
      if self.vision.colliderect(player.rect):
        #stop running and face the player
        self.update_action(4)#0:idle
      if self.idling ==False:
        if self.direction==1:
          ai_moving_right = True
        else:
          ai_moving_right = False
        ai_moving_left = not ai_moving_right
        self.move(ai_moving_left, ai_moving_right, SCREEN_HEIGHT)
        self.update_action(1)#1 run
        self.move_counter+=1
        #update ai vision as the enemy moves
        self.vision.center=(self.rect.centerx+75*self.direction,self.rect.centery)
        if self.move_counter>TILE_SIZE:
          self.direction*=-1
          self.move_counter*=-1
      else:
        self.idle_counter-=1
        if self.idle_counter<=0:
          self.idling=False

      
  def update_animation(self):
		#update animation
    ANIMATION_COOLDOWN = 55
		#update image depending on current frame
    self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1
		#if the animation has run out the reset back to the start
    if self.frame_index >= len(self.animation_list[self.action]):
      self.frame_index = 0


  def update_action(self, new_action):
		#check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
			#update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def check_alive(self):
    if self.health <= 0:
      self.health = 0
      self.speed = 0
      self.alive = False
      self.update_action(6)

  def draw(self,screen):
    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    