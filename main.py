import pygame
from pygame import mixer
from Tetris import Tetris
    
pygame.init()

# screen
screen = pygame.display.set_mode((750, 670))
pygame.display.set_caption("Tetris")

# music
mixer.init()
mixer.music.load("sounds\Tetris_music.wav")
mixer.music.play(-1)
game_over_sound = mixer.Sound("sounds\game_over_2.0.wav")

# background
background = pygame.image.load("images\space_background.jpg")
background = pygame.transform.scale(background, (750, 670))

# initializing variables
done = False
fps = 12
clock = pygame.time.Clock()
zoom = 30
game = Tetris(20, 10)
pressing_down = False
pressing_left = False
pressing_right = False
paused = False
old_level = 0
counter_frames = 0
z = 7

# basic colors
WHITE = (255,255,255)
GRAY = (128,128,128)

# game loop
while not done:
    counter_frames += 1
    # check if level up is possible
    game.level_up()

    # moving Tetromino constantly down
    if game.state == "start" and (counter_frames % z == 0):
        game.move_down()
    
    # gameover state 
    if game.state == "gameover":
        pygame.mixer.music.stop()  
        game_over_sound.play() 
        game.game_over(screen)
    
    # increase pace with higher level
    if old_level < game.level and z > 0:
        z -= 1
        old_level = game.level
    
    # event states
    for event in pygame.event.get():
        # quit statve
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN and not game.state == "gameover":
            # rotate right
            if event.key == pygame.K_UP:
                game.rotate_right()
            
            # rotate left
            if event.key == pygame.K_z:
                game.rotate_left()
            
            # pause
            if event.key == pygame.K_p:
                game.pause(screen)
                
            # hold
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                game.hold()
                
            # hard drop
            if event.key == pygame.K_SPACE:
                game.hard_drop()
            
            # soft drop
            if event.key == pygame.K_DOWN:
                pressing_down = True
            
            # moves to left
            if event.key == pygame.K_LEFT:
                pressing_left = True
                
            # moves to right
            if event.key == pygame.K_RIGHT:
                pressing_right = True
        
        # only rotate once even if key is pressed longer
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False
    
    # holding key -> action performed over and over
    if pressing_down:
        game.soft_drop()
    if pressing_left:
        game.left()
    if pressing_right:
        game.right()
        
    # draw the background 
    game.draw_background(screen, background, zoom)
    
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()