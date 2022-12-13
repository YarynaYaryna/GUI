#Name:Yaryna
#Date:Oct 18
#Fox adventure
#Create a kids scroller game

#import lybraries
import pygame
import time
from player import spritesheet as s
from buttons import button as b

global count
pygame.init()

clock = pygame.time.Clock()
FPS = 60
game_paused = False
game_menu = True
left=False
menu_state = "main"

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432

#define colors
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fox")
fox_image = pygame.image.load('player/fox_sprite.png')
fox = s.SpriteSheet(fox_image)
foxy_image = pygame.image.load('foxy.png')
foxy = s.SpriteSheet(foxy_image)

#load button images
start_img = pygame.image.load('buttons/start_btn.png')
exit_img = pygame.image.load('buttons/exit_btn.png')
pause_img = pygame.image.load('buttons/pause_btn.png')
#resume_img = pygame.image.load('buttons/resume_btn.png')
resume_img = pygame.image.load("buttons/button_resume.png")
options_img = pygame.image.load("buttons/button_options.png")
quit_img = pygame.image.load("buttons/button_quit.png")
video_img = pygame.image.load('buttons/button_video.png')
audio_img = pygame.image.load('buttons/button_audio.png')
keys_img = pygame.image.load('buttons/button_keys.png')
back_img = pygame.image.load('buttons/button_back.png')

#create button instances
start_button = b.Button(100, 50, start_img, 0.8)
exit_button = b.Button(100, 200, exit_img, 0.8)
pause_button = b.Button(5, 5, pause_img, 0.25)
#resume_button = b.Button(220, 125, resume_img, 1)
resume_button = b.Button(100, 50, resume_img, 1)
options_button = b.Button(100, 150, options_img, 1)
quit_button = b.Button(100, 250, quit_img, 1)
video_button = b.Button(327, 25, video_img, 1)
audio_button = b.Button(325, 125, audio_img, 1)
keys_button = b.Button(367, 225, keys_img, 1)
back_button = b.Button(540, 325, back_img, 1)

#create animation list
animation_list = []
animation_steps = [4, 9, 6, 4, 4, 9, 6, 4]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 55
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(fox.get_image(step_counter, 280, 167, 0.8, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

#define game variables
scroll = 0

ground_image = pygame.image.load("parallax/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"parallax/plx-{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


def draw_bg():
    for x in range(5):
        speed = 0.5
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2


def draw_ground():
    for x in range(15):
        screen.blit(
            ground_image,
            ((x * ground_width) - scroll * 2, SCREEN_HEIGHT - ground_height))


count = 0

#game loop
run = True
while run:
    if count == 0 and game_menu:
        #draw world
        screen.fill((160, 255, 255))
        screen.blit(foxy.get_image(0, 170, 242, 1.5, BLACK), (500, 70))
        #foxy.draw(screen)
        if exit_button.draw(screen):
            run = False
        if start_button.draw(screen):
            count += 1
            game_menu = False
    #check if game is paused
    elif game_paused == True:
        screen.fill((160, 255, 255))
        #if resume_button.draw(screen):
            #game_paused = False
        #check menu state
        if menu_state == "main":
          #draw pause screen buttons
          if resume_button.draw(screen):
            game_paused = False
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
    else:
        clock.tick(FPS)
        #draw world
        draw_bg()
        draw_ground()

        if pause_button.draw(screen):
            game_paused = True

        #update animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list[action]):
                frame = 0

        #show frame image
        screen.blit(animation_list[action][frame], (0, 270))

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and scroll > 0:
            left=True
            scroll -= 5
            if action == 4 or action == 5:
                action = 5
            elif action == 6 or action == 7:
                action = 6
        if key[pygame.K_RIGHT] and scroll < 2000:
            left=False
            scroll += 5
            if action == 0 or action == 1:
                action = 1
            elif action == 2 or action == 3:
                action = 2

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not game_paused and not game_menu and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
              if action==2 or action ==3 or action==6 or action==7:
                action=2
                frame=0
              else:
                action=0
                frame=0
            if event.key == pygame.K_LEFT:
              if action==2 or action ==3 or action==6 or action==7:
                action=6
                frame=0
              else:
                action=4
                frame=0
            if event.key == pygame.K_DOWN:
              if not left:
                action = 3
                frame = 0
              if left:
                action = 7
                frame = 0
            if event.key == pygame.K_UP:
              if not left:
                action = 0
                frame = 0
              if left:
                action=4
                frame=0
            if event.key == pygame.K_ESCAPE:
                game_paused = True

    pygame.display.update()

pygame.quit()