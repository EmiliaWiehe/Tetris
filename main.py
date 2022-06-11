import pygame
from Tetris import Tetris
from Tetrominoes import Tetrominoes
pygame.init()

screen = pygame.display.set_mode((750, 670))
pygame.display.set_caption("Tetris")

done = False
fps = 15
clock = pygame.time.Clock()
counter = 0
zoom = 30

WHITE = (255,255,255)
GRAY = (128,128,128)
BLACK = (0,0,0)

game = Tetris(20, 10)
pressing_down = False
pressing_left = False
pressing_right = False
paused = False
old_level = 0
counter_frames = 0
z = 7
# game loop
while not done:
    # constant going down
    counter_frames += 1
    if game.state == "start" and (counter_frames % z == 0):
        game.go_down()
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
                pause()
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
        

    # draw the game board and tetrominoes
    screen.fill(WHITE)
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = GRAY
                just_border = 1
            else:
                color = Tetrominoes.colors[game.field[i][j]]
                just_border = 0
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


    def pause():
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            screen.fill(WHITE)
            pause_font = pygame.font.SysFont("Calibri", 65, False, False)
            pause2_font = pygame.font.SysFont("Calibri", 20, False, False)
            text_pause = pause_font.render("Pause", True, (0, 0, 0))
            text_pause2 = pause2_font.render("Press C to continue or Q to quit", True, (0, 0, 0))
            screen.blit(text_pause, [300,250])
            screen.blit(text_pause2, [250,330])
            pygame.display.update()
            clock.tick(5)

    # display the message game over
    gameover_font = pygame.font.SysFont("Calibri", 65, True, False)
    text_gameover = gameover_font.render("Game Over!", True, (255, 0, 245))
    if game.state == "gameover":
        screen.blit(text_gameover, [230, 250])

    # display the score
    score_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_score = score_font.render("Score: " + str(game.score), True, (0, 0, 0))
    screen.blit(text_score, [20,40])

    # display the current level
    level_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_level = level_font.render("Level: " + str(game.level), True, (0, 0, 0))
    screen.blit(text_level, [20,80])

    # display the function hold
    hold_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_hold = hold_font.render("Hold ", True, (0, 0, 0))
    screen.blit(text_hold, [20, 350])

    # display the function next
    next_font = pygame.font.SysFont("Calibri", 30, False, False)
    text_next = next_font.render("Next ", True, (0, 0, 0))
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
    # display pause
    pause_font = pygame.font.SysFont("Calibri", 20, False, False)
    text_pause = pause_font.render("Press P to pause", True, (0, 0, 0))
    screen.blit(text_pause, [550,350])

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()