import pygame, os

GRAVITY=0.6

class Animals(pygame.sprite.Sprite):
  def __init__(self, char_type, x, y, scale, speed):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.char_type = char_type
    self.speed = speed
    self.direction = 1
    self.vel_y = 0
    self.jump = False
    self.in_air = True
    self.crouch = False
    self.flip = False
    self.animation_list = []
    self.frame_index = 0
    self.action = 0
    self.update_time = pygame.time.get_ticks()

    #load all images for the players
    animation_types = ['Idle', 'Run', 'Jump', 'Crouch', 'Crouch_idle']
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

  def move(self, moving_left, moving_right, SCREEN_HEIGHT):
		#reset movement variables
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

		#check collision with floor
    if self.rect.bottom + dy > SCREEN_HEIGHT:
      dy = SCREEN_HEIGHT - self.rect.bottom
      self.in_air = False

		#update rectangle position
    self.rect.x += dx
    self.rect.y += dy


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


  def draw(self,screen):
    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)