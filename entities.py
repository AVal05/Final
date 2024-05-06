import pygame, sys, random, os
from pygame.math import Vector2
from constants import cell_size, cell_number, coin_image, goblin_image

pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT #Custom event for screen updates
pygame.time.set_timer(SCREEN_UPDATE,120) #Sets timer to trigger the screen update

class COIN:
    def __init__(self):
        self.randomize() #positions the coin in a random cell

    def draw_coin(self):
        coin_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        coin_size = cell_size 
        screen.blit(coin_image,coin_rect) #draws the coin on the random cell

    def randomize(self):
        self.x = random.randint(0,cell_number - 1) #Random x position
        self.y = random.randint(0, cell_number - 1) #Random y position
        self.pos = pygame.math.Vector2(self.x,self.y) #Updates position
        


class GOBLIN:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]     #THIS INITIALIZES THE GOBLIN TO FACE AND MOVE TO THE RIGHT WHEN THE GAME STARTS
        self.direction = Vector2(1,0) 
        self.new_block = False #Controls when a new block is added


    def draw_goblin(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)                            #CYCLES THROUGH THE GOBLINS 'BODY' AND PLACES THE IMAGE OF THE GOBLIN 
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            goblin_size = cell_size
            screen.blit(goblin_image,block_rect) #draws each goblin block on the screen


    def move_goblin(self):
        if self.new_block == True:
            body_copy = self.body[:] 
            body_copy.insert(0,body_copy[0] + self.direction)  #THIS ADDS A BLOCK TO THE GOBLINS BODY 
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1] #Removes last block
            body_copy.insert(0,body_copy[0] + self.direction) #Add a new block at the front
            self.body = body_copy[:] #updates the golbin's body

    def add_block(self):
        self.new_block = True #sets a flag to add a new block in the next move

coin = COIN() #creates an instance of coin	
goblin = GOBLIN() #creates an instance of goblin
