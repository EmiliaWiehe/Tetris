import pygame
from pygame import mixer
from Tetris import Tetris
from Tetrominoes import Tetrominoes

pygame.init()

screen = pygame.display.set_mode((750, 670))
pygame.display.set_caption("Tetris")

# Music
mixer.init()
mixer.music.load("sounds\Tetris_music.wav")
mixer.music.play(-1)
game_over_sound = mixer.Sound("sounds\game_over_2.0.wav")

# Background
background = pygame.image.load("images\space_background.jpg")
background = pygame.transform.scale(background, (750, 670))

# all variables
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
BLACK = (0,0,0)


# game loop
while not done:
    counter_frames += 1
    game.level_up()
    if game.state == "start" and (counter_frames % z == 0):
        game.move_down()

    if game.state == "gameover":
        pygame.mixer.music.stop()  
        game_over_sound.play() 
        game.game_over(screen, mixer)
    
    # increase pace with level up
    if old_level < game.level:
        z -= 1
        old_level = game.level

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN and not game.state == "gameover":
            # rotate to the right
            if event.key == pygame.K_UP:
                game.rotate_right()
            if event.key == pygame.K_p:
                game.pause(screen)
            #rotate to the left
            if event.key == pygame.K_z:
                game.rotate_left()
            # hard drop
            if event.key == pygame.K_SPACE:
                game.hard_drop()
            # hold
            if event.key == pygame.K_c:
                game.hold()
            # soft drop
            if event.key == pygame.K_DOWN:
                pressing_down = True
            # moves to the left
            if event.key == pygame.K_LEFT:
                pressing_left = True
            # moves to the right
            if event.key == pygame.K_RIGHT:
                pressing_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False
            
    if pressing_down:
        game.soft_drop()
    if pressing_left:
        game.left()
    if pressing_right:
        game.right()
        

    # draw the background 
    screen.blit(background, (0,0))

    # draw the tetrominoes 
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] > 0:
                color = Tetrominoes.colors[game.field[i][j]]
                just_border = 0
                pygame.draw.rect(
                    screen,
                    color,
                    [225 + j * zoom, 30 + i * zoom, zoom, zoom],
                    just_border,
                )
                color = GRAY
                just_border = 1
                pygame.draw.rect(
                    screen,
                    color,
                    [225 + j * zoom, 30 + i * zoom, zoom, zoom],
                    just_border,
                )
            
    if game.Tetrominoes is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.Tetrominoes.image():
                    pygame.draw.rect(
                        screen,
                        game.Tetrominoes.color,
                        [
                            225 + (j + game.Tetrominoes.x) * zoom,
                            30 + (i + game.Tetrominoes.y) * zoom,
                            zoom,
                            zoom,
                        ], 
                    )
                    color = GRAY
                    just_border = 1
                    pygame.draw.rect(
                        screen,
                        color,
                        [
                            225 + (j + game.Tetrominoes.x) * zoom,
                            30 + (i + game.Tetrominoes.y) * zoom,
                            zoom,
                            zoom,
                        ],
                        just_border,
                    )

                    # draw the shadow
                    color = WHITE
                    just_border = 1
                    pygame.draw.rect(
                        screen,
                        color,
                        [225 + (j + game.Tetrominoes.x) * zoom,
                        30 + (i + game.new_shadow()) * zoom, zoom, zoom],
                        just_border,
                    )

    # display the score
    score_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_score = score_font.render("Score: " + str(game.score), True, WHITE)
    screen.blit(text_score, [20,40])

    # display the current level
    level_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_level = level_font.render("Level: " + str(game.level), True, WHITE)
    screen.blit(text_level, [20,80])

    # display the function hold
    hold_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_hold = hold_font.render("Hold ", True, WHITE)
    screen.blit(text_hold, [20, 350])
    if game.hold_draw:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.hold_figure.image():
                    pygame.draw.rect(
                        screen,
                        game.hold_figure.color,
                            [
                                20 + j * zoom,
                                400 + i * zoom,
                                zoom,
                                zoom,
                            ],
                        )
                    color = GRAY
                    just_border = 1
                    pygame.draw.rect(
                        screen,
                        color,
                        [20 + j * zoom, 400 + i * zoom, zoom, zoom],
                        just_border,
                    )

    # display the function next
    next_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_next = next_font.render("Next ", True, WHITE)
    screen.blit(text_next, [550,40])
    for i in range(4):
        for j in range(4):
            p = i * 4 + j
            if p in game.next_figure.image():
                pygame.draw.rect(
                    screen,
                    game.next_figure.color,
                        [
                            475 + (j + game.next_figure.x) * zoom,
                            100 + (i + game.next_figure.y) * zoom,
                            zoom,
                            zoom,
                        ],
                    )
                color = GRAY
                just_border = 1
                pygame.draw.rect(
                    screen,
                    color,
                    [
                            475 + (j + game.next_figure.x) * zoom,
                            100 + (i + game.next_figure.y) * zoom,
                            zoom,
                            zoom,
                    ],
                    just_border,
                )

    # display pause
    pause_font = pygame.font.SysFont("Calibri", 20, False, False)
    text_pause = pause_font.render("Press P to pause", True, WHITE)
    screen.blit(text_pause, [550,350])

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()