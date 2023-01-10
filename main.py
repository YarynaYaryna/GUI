#Name:Yaryna
#Date:Oct 18
#Fox adventure
#Create a kids scroller game

#import lybraries
import pygame
import Animals as a
import Button as b
import Items as e

pygame.init()

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.4
scroll = 0

#define colors
BLACK=((255,0,0))
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
pause_button = b.Button(5, 5, pause_img, 0.25)
resume_button = b.Button(100, 50, resume_img, 1)
options_button = b.Button(100, 150, options_img, 1)
quit_button = b.Button(100, 250, quit_img, 1)
video_button = b.Button(427, 25, video_img, 1)
audio_button = b.Button(425, 125, audio_img, 1)
keys_button = b.Button(467, 225, keys_img, 1)
back_button = b.Button(640, 325, back_img, 1)

#load images
mulberry_img = pygame.image.load("Images/Food/mulberry.png")

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

TILE_SIZE=40


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#load images
mulberry_img = pygame.image.load("Images/Food/mulberry.png")
peanuts_img = pygame.image.load("Images/Food/peanuts.png")
raspberry_img = pygame.image.load("Images/Food/raspberry.png")
item_boxes={
  'Mulberry'  : mulberry_img,
  'Peanuts'  : peanuts_img,
  'Raspberry' : raspberry_img
}

      
#create sprite groups
items_group = pygame.sprite.Group()

#temp..................
item=e.Item('Mulberry', 80, 380)
items_group.add(item)
item=e.Item('Peanuts', 400, 370)
items_group.add(item)
item=e.Item('Raspberry', 500, 360)
items_group.add(item)

fox = a.Animals('Fox', 200, 200, 0.65, 7, 0, 0, 0)
      
#game loop
run = True
while run:
            
        clock.tick(FPS)
        
        #draw world
        draw_bg()
        draw_ground()

        #show mulberry
        draw_text('Mulberry: ', font, WHITE, 10, 35)
        for x in range(fox.mulberry):
          screen.blit(mulberry_img, (110+(x*40), 25))
        if pause_button.draw(screen):
            game_paused = True
        #check if game is paused
        if game_paused:
          start_game=True
          screen.fill((160, 255, 255))
        #if resume_button.draw(screen):
            #game_paused = False
        #check menu state
          if menu_state == "main":
          #draw pause screen buttons
            if resume_button.draw(screen):
              game_paused = False
              start_game=False
            if options_button.draw(screen):
              menu_state = "options"
            if quit_button.draw(screen):
              run = False
        #check if the options menu is open
          if menu_state == "options":
          #draw the different options buttons
            if video_button.draw(screen):
              print("Video Settings")
            if audio_button.draw(screen):
              print("Audio Settings")
            if keys_button.draw(screen):
              print("Change Key Bindings")
            if back_button.draw(screen):
              menu_state = "main"
        

        fox.update_animation()
        fox.draw(screen)
        fox.move(moving_left, moving_right, SCREEN_HEIGHT)

        #update and draw groups
        items_group.update(fox)
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
          fox.move(moving_left, moving_right, SCREEN_HEIGHT)

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