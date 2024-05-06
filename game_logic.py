import pygame, sys, os, random
from pygame.math import Vector2
from entities import COIN, GOBLIN #Imports classes
from utilities import draw_menu, draw_game_over, save_score, load_score, display_leaderboard, get_user_input
from constants import cell_size, cell_number, goblin_image, trophy_image, coin_image, screen, GAME_STATE, clock, screen

pygame.init()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
game_font = pygame.font.Font(None,25) #Creates a game font

class MAIN:
    def __init__(self):
        self.goblin = GOBLIN() 
        self.coin = COIN() #Creates an instance of coin and goblin

    def update(self, GAME_STATE):
        self.goblin.move_goblin() #Updates position of goblin
        self.check_collision() #Checks for collision
        GAME_STATE = self.check_fail(GAME_STATE) #Checks if the game should fail
        return GAME_STATE

    def draw_elements(self): #Draws grass, coin, goblin, and current score
        self.draw_grass() 
        self.coin.draw_coin()
        self.goblin.draw_goblin()
        self.draw_score()

    def check_collision(self):
        if self.coin.pos == self.goblin.body[0]: #Check if the first goblin gets the coin
            self.coin.randomize() #Repositions the coin
            self.goblin.add_block() #increases the goblin chain
        for block in self.goblin.body[1:]: #checks if any part of goblin collides with coin
            if block == self.coin.pos:
                self.coin.randomize()


    def check_fail(self, GAME_STATE):
        if not 0 <= self.goblin.body[0].x < cell_number or not 0 <= self.goblin.body[0].y < cell_number:
            GAME_STATE = self.game_over(GAME_STATE) #Game over if goblin goes out of bounds
        for block in self.goblin.body[1:]:
            if block == self.goblin.body[0]:
                GAME_STATE = self.game_over(GAME_STATE) #Game over if golbin collides with itself
        return GAME_STATE
                

    def game_over(self, GAME_STATE):
        GAME_STATE = 'POST GAME' #Transitions game state
        return GAME_STATE


    def draw_grass(self):
        grass_color = (91,235,115) #Defines the grass colour
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect= pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect) #This code itereates only half of the board to create a checkered pattern of two different shades fo green for the grass
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.goblin.body) - 3) #Calculates current score based off goblins length (-3 for initiallength)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        coin_rect = coin_image.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(coin_rect.left,coin_rect.top,coin_rect.width + score_rect.width + 7,coin_rect.height)

        pygame.draw.rect(screen,(167,209,21),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(coin_image, coin_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2) #The above code draws out the current score at the bottom right of the screen with a little coin image aswell


def game_state_menu(GAME_STATE, event):
    global main_game
    screen.fill((0,0,0)) #Clears the screen
    play_rect, quit_rect, leaderboard_rect = draw_menu() #Draws the menu
    pygame.display.update() #updates the display to show the menu
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Check if mouse button is pressed
         mouse_pos = event.pos
         if play_rect.collidepoint(mouse_pos): #If button press is over play button, transitions to game
             GAME_STATE = 'RUNNING'
             main_game = MAIN()
         elif quit_rect.collidepoint(mouse_pos): #If button press is over quit button, exits the game
             pygame.quit()
             sys.exit()
         elif leaderboard_rect.collidepoint(mouse_pos): #If button press over leaderboard, displays the leaderboard screen
             GAME_STATE = 'LEADERBOARD'
    return GAME_STATE



def game_state_running(GAME_STATE, event):
    global main_game
    if event.type == SCREEN_UPDATE:
        GAME_STATE = main_game.update(GAME_STATE) #Updates the main game, and possibly changes game state if game over
    if event.type == pygame.KEYDOWN: #checks if key is pressed
        if event.key == pygame.K_UP: #If up arrow pressed,makes the goblin move up
            if main_game.goblin.direction.y != 1:
                main_game.goblin.direction = Vector2(0,-1)
        if event.key == pygame.K_DOWN: #If down arrow pressed,makes the goblin move down
            if main_game.goblin.direction.y != -1:
                main_game.goblin.direction = Vector2(0,1)
        if event.key == pygame.K_RIGHT: #If right arrow pressed,makes the goblin move right
            if main_game.goblin.direction.x != -1:
                main_game.goblin.direction = Vector2(1,0)
        if event.key == pygame.K_LEFT: #If left arrow pressed,makes the goblin move left
            if main_game.goblin.direction.x != 1:
                main_game.goblin.direction = Vector2(-1,0)
    screen.fill((73,188,92)) #Fills screen with other shade of green to create that checkboard effect.
    main_game.draw_elements() #Draws the main screen
    pygame.display.update() #Updates display to show maingame
    clock.tick(120) #Sets frame rate to 120FPS
    return GAME_STATE #Updates game state


def game_state_leaderboard(GAME_STATE, event):
    pygame.display.update() #Updates display
    screen.fill((0,0,0)) #Clears the screen to black
    top_scores = load_score() #Loads the top 5 scores from the leaderboard
    menu_rect, quit_rect = display_leaderboard(screen, top_scores) #Displays the leaderboard
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = event.pos
        if quit_rect.collidepoint(mouse_pos): #If mouse presses quit button, exits the game
            pygame.quit()
            sys.exit()
        elif menu_rect.collidepoint(mouse_pos): #If mouse presses menu button, goes back to main screen
            GAME_STATE = 'MENU'
    return GAME_STATE

def game_state_gameover(GAME_STATE, event):
    screen.fill((0,0,0)) #Clears screen to black
    play_again_rect, game_over_rect, quit_rect, leaderboard_rect = draw_game_over() #Draws the game over screen
    pygame.display.update() #Updates to display it
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = event.pos
        if play_again_rect.collidepoint(mouse_pos): #If mouse presses play again button, game starts again
            GAME_STATE = 'RUNNING'
            main_game = MAIN()
        elif quit_rect.collidepoint(mouse_pos): #If mouse presses quit button, exits the game
            pygame.quit()
            sys.exit()
        elif leaderboard_rect.collidepoint(mouse_pos): #If mouse presses leaderboard button, displays the leaderboard
            screen.fill((0,0,0))
            GAME_STATE = 'LEADERBOARD'
            pygame.display.update()
    return GAME_STATE

def game_state_postgame (GAME_STATE, event):
    screen.fill((0,0,0)) #Clears screen
    score = str(len(main_game.goblin.body) - 3) #Stores the score of the player
    username = get_user_input(screen, "Enter Username: ") #Prompts the user to enter their username in the textbox
    save_score(score, username) #Saves score and username
    load_score() #loads score into leaderboard
    GAME_STATE = 'GAME OVER' #Transtitions game state
    return GAME_STATE 
