import pygame
from pygame.locals import KEYDOWN, QUIT, K_SPACE, K_l, K_s, K_ESCAPE
import numpy as np

#Initializing
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT = 750, 750, 15, 15
CELL_WIDTH, CELL_HEIGHT = SCREEN_WIDTH//BLOCK_WIDTH, SCREEN_HEIGHT//BLOCK_HEIGHT		#Width and height of the screen in terms of cell dimensions

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Greenberg-Hastings model')

NUMBER_OF_STATES = 3
state_colours = [(255, 255, 255), (0, 255, 0), (255, 255, 0)]

TEMPLATE = np.zeros((CELL_WIDTH, CELL_HEIGHT), dtype='int') #default
#TEMPLATE = np.loadtxt('multispiral', dtype='int') #spiral

class Cell(pygame.sprite.Sprite):       #Cells on the board
    def __init__(self, coords = ()):
        super(Cell, self).__init__()
        self.state = 0
        self.pos = coords if coords else (random.randint(0, CELL_WIDTH), random.randint(0, CELL_HEIGHT))
        self.block = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.block.fill((255, 255, 255))
        self.rect = self.block.get_rect(topleft=coords)
        self.neighbors = pygame.sprite.Group()

    def switch(self, state):
        state_cells[self.state].remove(self)
        self.state = state
        state_cells[self.state].add(self)
        self.block.fill(state_colours[state])
        screen.blit(self.block, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
    
    def new_state(self):        #Update the state of a cell according to the rules of the game
        active_neighbour_count = sum([cell.state == 1 for cell in self.neighbors])

        if active_neighbour_count > 0 and self.state == 0:
            return 1
        elif self.state == 1:
            return 2

        return 0
            
#Initializing cells
all_cells = pygame.sprite.Group()
state_cells = [pygame.sprite.Group() for state in range(NUMBER_OF_STATES)]

for i in range(CELL_WIDTH):
    for j in range(CELL_HEIGHT):
        new_cell = Cell((i*BLOCK_WIDTH, j*BLOCK_HEIGHT))
        all_cells.add(new_cell)
        new_cell.switch(TEMPLATE[i, j])

#Adding neighbors
dist_4 = lambda celf, cell: abs(celf.pos[0] - cell.pos[0])//BLOCK_WIDTH + abs(celf.pos[1] - cell.pos[1])//BLOCK_HEIGHT
dist_8 = lambda celf, cell: max(abs(celf.pos[0] - cell.pos[0])//BLOCK_WIDTH, abs(celf.pos[1] - cell.pos[1])//BLOCK_HEIGHT) #8-neighbour

for celf in all_cells:
    for cell in all_cells:
        if dist_8(celf, cell) == 1: #4 nearest neighbors
            celf.neighbors.add(cell)

play, running = False, True      #Variable to 1. play/pause 2. terminate the main loop

#Main game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:      #Quit
            running = False
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:       #Play/Pause
                play = not play
                print('Unpaused' if play else 'Paused')
            elif pygame.key.get_pressed()[K_ESCAPE]:       #Reset
                for cell in all_cells:
                    cell.switch(0)
                print("Game Reset.")
            elif pygame.key.get_pressed()[K_s]:
                grid = np.zeros((CELL_WIDTH, CELL_HEIGHT), dtype='int')
                for cell in all_cells:
                    grid[cell.pos[0]//BLOCK_WIDTH, cell.pos[1]//BLOCK_HEIGHT] = cell.state

                name = input("Template name: ")
                np.savetxt(name, grid, fmt='%d')
            elif pygame.key.get_pressed()[K_l]:
                template = np.loadtxt(input("Template name: "), dtype='int')
                for cell in all_cells:
                    cell.switch(template[cell.pos[0]//BLOCK_WIDTH, cell.pos[1]//BLOCK_HEIGHT])                    

    #Update cells
    future_updates = [pygame.sprite.Group() for state in range(NUMBER_OF_STATES)]

    for cell in all_cells:
        if play:
            future_updates[cell.new_state()].add(cell)
        else:
            #Activate/Deactivate cells by mouse click
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    future_updates[(cell.state+1)%NUMBER_OF_STATES].add(cell)
                elif pygame.mouse.get_pressed()[2]:
                    future_updates[(cell.state-1)%NUMBER_OF_STATES].add(cell)
    
    #Update cells
    for state in range(NUMBER_OF_STATES):
        for cell in future_updates[state]:
            cell.switch(state)

    #Update display
    pygame.display.flip()
    if play:
        pygame.time.wait(150)
    else:
        pygame.time.wait(150)

pygame.quit()
