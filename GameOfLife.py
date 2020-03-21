import pygame
from pygame.locals import KEYDOWN, QUIT, K_SPACE, K_ESCAPE

#Initializing
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT = 1000, 1000, 20, 20
CELL_WIDTH, CELL_HEIGHT = SCREEN_WIDTH//BLOCK_WIDTH, SCREEN_HEIGHT//BLOCK_HEIGHT		#Width and height of the screen in terms of cell dimensions

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Conway\'s Game of Life') 

class Cell(pygame.sprite.Sprite):       #Cells on the board
    def __init__(self, coords = ()):
        super(Cell, self).__init__()
        self.is_active = False
        self.pos = coords if coords else (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.block = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.block.fill((255, 255, 255))
        self.rect = self.block.get_rect(topleft=coords)
        self.neighbors = pygame.sprite.Group()

    def activate(self):
        self.is_active = True
        self.block.fill((0, 0, 0))      #Black
        activated_cells.add(self)
        screen.blit(self.block, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        deactivated_cells.remove(self)

    def deactivate(self):
        self.is_active = False
        self.block.fill((255, 255, 255))          #White
        deactivated_cells.add(self)
        screen.blit(self.block, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        activated_cells.remove(self)
    
    def update(self):        #Update the state of a cell according to the rules of the game
        active_neighbour_count = sum([cell.is_active for cell in self.neighbors])
        
        if (active_neighbour_count < 2 or active_neighbour_count > 3):
            return "DEACTIVATE"    
        if active_neighbour_count == 3 and not self.is_active:
            return "ACTIVATE"

        return "STABLE"     #Numbers can be used instead of strings for efficiency

#Initializing cells
all_cells = pygame.sprite.Group()
activated_cells = pygame.sprite.Group()
deactivated_cells = pygame.sprite.Group()

for i in range(CELL_WIDTH):
    for j in range(CELL_HEIGHT):
        new_cell = Cell((i*BLOCK_WIDTH, j*BLOCK_HEIGHT))
        all_cells.add(new_cell)
        new_cell.deactivate()
        deactivated_cells.add(new_cell)

#Adding neighbors
for celf in all_cells:
    for cell in all_cells:
        if cell.pos in [((celf.pos[0]+x*BLOCK_WIDTH)%SCREEN_WIDTH, (celf.pos[1]+y*BLOCK_HEIGHT)%SCREEN_HEIGHT) for x in [-1, 0, 1] for y in [-1, 0, 1]]: #8 nearest neighbors
            celf.neighbors.add(cell)
    celf.neighbors.remove(celf)

play, running = False, True      #Variable to 1. play/pause 2. terminate the mian loop

#Main game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:      #Quit
            running = False
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:       #Play/Pause
                play = not play
                print('Unpaused' if play else 'Paused')
            elif pygame.key.get_pressed()[K_ESCAPE]:        #Reset
                for cell in all_cells:
                    cell.deactivate()
                print("Game Reset.")

    #Update cells
    to_activate, to_deactivate = pygame.sprite.Group(), pygame.sprite.Group()

    for cell in all_cells:
        if play:
            #Update the state of the cells
            if  cell.update() == "ACTIVATE":
                to_activate.add(cell)
            elif cell.update() == "DEACTIVATE":
                to_deactivate.add(cell)
        else:
            #Activate/Deactivate cells by mouse click
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                if not cell.is_active and pygame.mouse.get_pressed()[0]:
                    to_activate.add(cell)
                elif cell.is_active and pygame.mouse.get_pressed()[2]:
                    to_deactivate.add(cell)
                
    #Update cells
    for cell in to_activate:
        cell.activate()
    for cell in to_deactivate:
        cell.deactivate()

    #Update display
    pygame.display.flip()
    pygame.time.wait(150)

pygame.quit()
