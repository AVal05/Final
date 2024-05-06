import pygame 
pygame.init()	#imports and initializes pygame
cell_size = 40	#sets the size of each specific little box
cell_number = 20 	#sets the number of such boxes
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size)) #initializes the screen to have 20 boxes in x and y directions
clock = pygame.time.Clock() # Creates a clock object to manage game frame rate
coin_image = pygame.image.load('/home/alexv/ECE-160/FinalProject/coin.png').convert_alpha()
coin_image = pygame.transform.scale(coin_image, (cell_size,cell_size)) #Loads and scales the image of a coin to fit into a cell size
goblin_image1 = pygame.image.load('/home/alexv/ECE-160/FinalProject/goblin.png').convert_alpha()
goblin_image = pygame.transform.scale(goblin_image1, (cell_size, cell_size))#Loads and scales the image of the goblin to fit into a cell size
trophy_image = pygame.image.load('/home/alexv/ECE-160/FinalProject/trophy.png').convert_alpha()
trophy_image = pygame.transform.scale(trophy_image, (cell_size, cell_size)) #Loads and scales the image of a trophy to fit into a cell size
game_font = pygame.font.Font(None,25)  # Creates a Font object with a default font and size 25
GAME_STATE = 'MENU' #initializes the game state to be menu initially

