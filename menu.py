"""if start_game==False and game_menu:
        #draw world
        screen.fill((160, 255, 255))
        screen.blit(foxy.get_image(0, 170, 270, 1.5, BLACK), (500, 70))
        if exit_button.draw(screen):
            run = False
        if start_button.draw(screen):
            game_menu = False
            start_game=True
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
            menu_state = "main""""