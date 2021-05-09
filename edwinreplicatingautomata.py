import pygame
from pygame.locals import KEYDOWN, QUIT, K_SPACE, K_ESCAPE, K_EQUALS, K_PLUS, K_MINUS

#Initializing
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT = 1250, 1250, 10, 10
CELL_WIDTH, CELL_HEIGHT = SCREEN_WIDTH//BLOCK_WIDTH, SCREEN_HEIGHT//BLOCK_HEIGHT		#Width and height of the screen in terms of cell dimensions

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Replicating Automaton')

class Cell(pygame.sprite.Sprite):       #Cells on the board
    def __init__(self, coords):
        super(Cell, self).__init__()
        self.is_active = False
        self.pos = coords
        self.block = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.block.fill((255, 255, 255))
        self.rect = self.block.get_rect(topleft=(coords[0]*BLOCK_WIDTH, coords[1]*BLOCK_HEIGHT))
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
        """
        In each iteration, any given cell is replaced by the modulo 2 sum of the values of its neighbouring cells.
        
        A black cell has a value of `1` and a white cell has a value of `0`.
        """

        active_neighbour_count = sum([cell.is_active for cell in self.neighbors])
        
        if (active_neighbour_count % 2 == 1) and not self.is_active:
            return "ACTIVATE"
        elif (active_neighbour_count % 2 == 0) and self.is_active:
            return "DEACTIVATE"
        
        return "STABLE"

#Initializing cells
all_cells = pygame.sprite.Group()
activated_cells = pygame.sprite.Group()
deactivated_cells = pygame.sprite.Group()

cellgrid = [[False for i in range(CELL_WIDTH)] for j in range(CELL_HEIGHT)]

for i in range(CELL_WIDTH):
    for j in range(CELL_HEIGHT):
        new_cell = Cell((i, j))
        all_cells.add(new_cell)
        new_cell.deactivate()
        deactivated_cells.add(new_cell)
        cellgrid[i][j] = new_cell

#the Von Neumann neighbourhood
neighborhood = lambda p, q: [(min(CELL_WIDTH-1, (p+x)), min(CELL_HEIGHT-1, (q+y))) for x in [-1, 0, 1] for y in [-1, 0, 1] if abs(x) + abs(y) == 1]

#Adding neighbors
for celf in all_cells:
    for (x, y) in neighborhood(*celf.pos): #4 nearest neighbors
            celf.neighbors.add(cellgrid[x][y])

play, running, wait_time = False, True, 150     #Variable to 1. play/pause 2. terminate the main loop 3. Specify the wait time in ms

print('Point and click to draw. Press `SPACE` to play/pause. Press the `+`/`-` keys to increase/decrease the simulation speed. \n')

#Main game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:      #Quit
            running = False
        if event.type == KEYDOWN:
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[K_SPACE]:       #Play/Pause
                play = not play
                print('Unpaused' if play else 'Paused')
            elif keys_pressed[K_ESCAPE]:        #Reset
                for cell in all_cells:
                    cell.deactivate()
                print("\nGame Reset.\n")
            elif keys_pressed[K_PLUS] or keys_pressed[K_EQUALS]:
                wait_time -= 50
                print("Simulation speed increased.")
            elif keys_pressed[K_MINUS]:
                wait_time += 50
                print("Simulation speed decreased.")

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

        if cell.pos[0] in (0, CELL_WIDTH-1) or cell.pos[1] in (0, CELL_HEIGHT-1):
            play = False
            print("The cells have hit the boundary.")
            
    for cell in to_deactivate:
        cell.deactivate()

    #Update display
    pygame.display.flip()
    pygame.time.wait(wait_time)

pygame.quit()