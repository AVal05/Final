import pygame, sys, random, os
from pygame.math import Vector2

#Initializes pyagme nad sets up the display
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()

#Loads and scales images
coin_image = pygame.image.load('/home/alexv/ECE-160/FinalProject/coin.png').convert_alpha()
coin_image = pygame.transform.scale(coin_image, (cell_size,cell_size))
goblin_image1 = pygame.image.load('/home/alexv/ECE-160/FinalProject/goblin.png').convert_alpha()
goblin_image = pygame.transform.scale(goblin_image1, (cell_size, cell_size))
trophy_image = pygame.image.load('/home/alexv/ECE-160/FinalProject/trophy.png').convert_alpha()
trophy_image = pygame.transform.scale(trophy_image, (cell_size, cell_size))
game_font = pygame.font.Font(None,25)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)

def draw_menu():	#Draws the main menu
    global play_rect, quit_rect, leaderboard_rect
    screen.fill((0,0,0))
    menu_font = pygame.font.Font(None,50)
    text_font = pygame.font.Font(None, 25)
    #Renders text elements
    welcome1_text = text_font.render('Welcome to Goblin (snake but with goblins)!', True,(255,255,255))
    welcome2_text = text_font.render('Use your arrow keys to navigate around and get as many coins as you can', True, (255,255,255))
    welcome3_text = text_font.render('GOOD LUCK', True, (255,255,255))
    play_text = menu_font.render(' Play ', True,(245,6,253))
    quit_text = menu_font.render(' Quit ', True,(245,6,253))
    leaderboard_text = menu_font.render(' Leaderboard ', True,(245,6,253))
    #Positions the text
    play_rect = play_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 - 30))
    quit_rect = quit_text.get_rect(center=(cell_number *cell_size // 2, cell_number * cell_size - 40))
    leaderboard_rect = leaderboard_text.get_rect(center=(cell_number * cell_size // 2 + 10, cell_number * cell_size // 2 + 20))
    #Draws the rectangles on the screen around the text

    pygame.draw.rect(screen, (255,255,255), play_rect, 2)
    pygame.draw.rect(screen, (255,255,255), quit_rect, 2)
    trophy_rect = trophy_image.get_rect(midright = (leaderboard_rect.left,leaderboard_rect.centery))
    lb_rect = pygame.Rect(trophy_rect.left,trophy_rect.top,trophy_rect.width + leaderboard_rect.width + 2, leaderboard_rect.height)
    pygame.draw.rect(screen,(255,255,255), lb_rect, 2)
    screen.blit(trophy_image,trophy_rect)
    screen.blit(leaderboard_text, leaderboard_rect)
    screen.blit(play_text, play_text.get_rect(center=play_rect.center))
    screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))
    screen.blit(welcome1_text, (cell_number*cell_size // 2 - 175,20))
    screen.blit(welcome2_text, (cell_number*cell_size // 2 - 300,40))
    screen.blit(welcome3_text, (cell_number*cell_size // 2 - 50,60))
    goblin_image2 = pygame.transform.scale(goblin_image1, (180, 180))
    screen.blit(goblin_image2, (cell_number*cell_size // 2 - 75, 135))
    return play_rect, quit_rect, leaderboard_rect

def draw_game_over():	#Draws the game over screen
    global play_again_rect, game_over_rect, quit_rect, leaderboard_rect
    screen.fill((0,0,0))
    menu_font = pygame.font.Font(None,50)
    game_over_text = menu_font.render('GAME OVER', True, (246,6,253))
    play_again_text = menu_font.render(' Play Again ', True, (245,6,253))
    quit_text = menu_font.render(' QUIT ', True,(245,6,253))
    leaderboard_text = menu_font.render(' Leaderboard ', True,(245,6,253))
    play_again_rect = play_again_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 - 20))
    game_over_rect = game_over_text.get_rect(center=(cell_number * cell_size // 2, 40))
    leaderboard_rect = leaderboard_text.get_rect(center=(cell_number * cell_size // 2 + 3, cell_number * cell_size // 2 + 20))
    pygame.draw.rect(screen, (255,255,255), play_again_rect, 2)
    pygame.draw.rect(screen, (255,255,255), quit_rect, 2)
    trophy_rect = trophy_image.get_rect(midright = (leaderboard_rect.left,leaderboard_rect.centery))
    lb_rect = pygame.Rect(trophy_rect.left,trophy_rect.top,trophy_rect.width + leaderboard_rect.width + 2, leaderboard_rect.height)
    pygame.draw.rect(screen,(255,255,255), lb_rect, 2)
    screen.blit(play_again_text, play_again_text.get_rect(center=play_again_rect.center))
    screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(leaderboard_text, leaderboard_rect)
    screen.blit(trophy_image,trophy_rect)
    return play_again_rect, quit_rect, game_over_rect, leaderboard_rect

def save_score(score, username): #Saves the score and the username in the leaderboard file
    with open('leaderboard.txt', 'a') as file: #Opens leaderboard file in append mode
        file.write(f"{username}:{score}\n") #writes username and score in "username:score" format

def load_score():	#Loads score from leaderboard file and returns them sorted
    with open('leaderboard.txt', 'r') as file:
        lines = file.readlines() #Opens file and reads the lines
        scores = []
        for line in lines:
            username, score = line.strip().split(":")
            scores.append((username, int(score)))
        scores.sort(key=lambda x: x[1], reverse=True) #Sorts list in descending score order
    return scores #Returns the sorted list of scores

def display_leaderboard(screen, top_scores): #Displays the leaderboard on screen
    global menu_rect, quit_rect
    font = pygame.font.Font(None, 24)
    menu_font = pygame.font.Font(None,40)
    x = cell_size * cell_number // 2 - 50
    y = 50
    gap = 20
    title_surface = font.render('Leaderboard', True, pygame.Color('white'))
    screen.blit(title_surface,(x, y))
    for index, (username, score) in enumerate(top_scores[:5]): #Loops through the top 5 scores
        score_text = f"{index + 1}. {username} - {score}" #Formats the score text for the display
        score_surface = font.render(score_text, True, pygame.Color('white')) #Renders the score text
        screen.blit(score_surface, (x, y + index * gap + 20)) 

    quit_text = menu_font.render(' Quit ', True,(245,6,253))
    menu_text = menu_font.render(' Main Menu ', True,(245,6,253))
    quit_rect = quit_text.get_rect(center=(cell_number *cell_size // 2 + 50, cell_number * cell_size - 40))
    menu_rect = menu_text.get_rect(center=(cell_number * cell_size // 2 - 100, cell_number * cell_size - 40))
    pygame.draw.rect(screen, (255,255,255), quit_rect, 1)
    pygame.draw.rect(screen, (255,255,255), menu_rect, 1)
    screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))
    screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))
    return menu_rect, quit_rect

def get_user_input(screen, prompt): #This Function gets the username of the person after the game ends
    base_font = pygame.font.Font(None, 32)
    user_text = '' #Initializes the user_text to an empty string
    input_rect = pygame.Rect(200, 200, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive #Input box is inactive

    active = False #Tracks whether input box is active or inactive
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active #Toggles active state
                else:
                    active = False
                color = color_active if active else color_passive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN: #User presses enter, username is stored
                        done = True
                    elif event.key == pygame.K_BACKSPACE: #User presses backspace, deletes last character in string
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode #Add character typed to user_text 
        #Draws the Input box and screen
        screen.fill((0, 0, 0))
        prompt_surf = base_font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_surf, (50, 150))
        txt_surface = base_font.render(user_text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x+5, input_rect.y+5))
        pygame.draw.rect(screen, color, input_rect, 2)

        pygame.display.flip() #Updates the dispaly

    return user_text #Returns the username

