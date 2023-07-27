import pygame
import random
import tetris_ai

# assigning all of the colours in the game
colors = [ 
    (0, 0, 0),
    (206, 16, 227),
    (85, 201, 201),
    (255, 211, 54),
    (122, 209, 29),
    (227, 33, 16),
    (17, 27, 217),
]


class block:
    x = 0 # initialize x value
    y = 0 # initialize y value

# creates blocks from a 4x4 matrix (from 0-15) where the outer list contains block types and the inner list contains each blocks rotations
# note these do not include translations within the matrix
    blocks = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

# init method is called automatically when an object is instantiated
# this method selects a colour and block at random for the game
    def __init__(self, x, y): # self is the instance of the class being created, x and y are initial values
        self.x = x # sets x value of the object (where x = 0 at the top)to the value passed through the parameters
        self.y = y # sets y value of the object (where y = 0 at the top)to the value passed through the parameters
        self.type = random.randint(0, len(self.blocks) - 1) # selects random block from list of range 0 to blocks-1 (cuz list starts at 0 so final range is one less)
        self.color = random.randint(1, len(colors) - 1) # selects random colour from the list 
        self.rotation = 0 # sets rotaition of the block to the initial orientation

    def image(self): # image meth0d
        return self.blocks[self.type][self.rotation] # returns the image of the type of block and rotation

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type]) # goes into inner lust to find rotation
        # the modeluls operator creates a range of fgure types given and cycles through each one in a loop
        # starts at zero +1 makes 1, then first type of rotation is selected (1%1 =0) goes to second and so on making sure self rotation does not equal 0

class Tetris:
    def __init__(self, height, width): # initializes objets state and takes in height and width parameters
        self.level = 2 # level of the game is level 2
        self.score = 0 # assigns the score to 0 in the beginning
        self.state = "start" # instance variable for state of the game 
        self.field = [] # creates empty list for feild to score game data as it runs
        self.x = 100 # outer x variable to 100 (dimensions)
        self.y = 60 # outer y variable to 60
        self.zoom = 20 # 
        self.block = None # stores a block but is not assigned initally (game is clear)
        self.height = height # assigns height of the object to what was passed in through the paramenters
        self.width = width # assigns width of the object to what was pssed in through the parameters
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line) 
            # nested loop that creates a 2D list of 0s to create our playing field

    def new_block(self):
        self.block = block(3, 0) # creates a new block and positions it at these coordinates (in the middle)
        # calls the whole block class to instantiate a new block
        
    def intersects(self): # checks if the block intersects with any other block on the field 
        intersection = False # assigns the block to no intersection at firt when it is dropped down to the field
        for i in range(4):
            for j in range(4): # nested loop to check 4x4 block matrix 
                if i * 4 + j in self.block.image(): # checks if (i,j) position has a piece of the block
                    if i + self.block.y > self.height - 1 or j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or self.field[i + self.block.y][j + self.block.x] > 0: # checks if other blocks occupy existing cell (num greater than 0)
                        # checks if it goes out of bounds vertically or horizonatally within the game field by comparing feild dimensions with block position
                        intersection = True # sets intersection to true since block is out of playing bounds
        return intersection # returns whether the block intersects or doesn't 

    def break_lines(self): # method to destroy the lines once they are full
        lines = 0 # initializes total num of complete lines to 0 and keeps track of cleared lines
        for i in range(1, self.height): # iterates through all of the rows on the grid except the top one
            zeros = 0 # initialized to count the number of empty cells in each row
            for j in range(self.width): # iterates through columns on grid
                if self.field[i][j] == 0: # checks if the cell is empty
                    zeros += 1 # adds 1 to zero
            if zeros == 0: # if all of the cells in the row are filled
                lines += 1 # add 1 to lines (you need to get rid of)
                for i1 in range(i, 1, -1): # itertes from the current filled row in reverse order
                    for j in range(self.width): # nested loop to iterate through each column
                        self.field[i1][j] = self.field[i1 - 1][j] # sets all of the cells one row down to make it look like a cleared row
        self.score += lines # updates score so it matches lines cleared

    def freeze(self): # method that freezes the block once it intersects
        for i in range(4):
            for j in range(4): # 2D list that circles through the block's 4x4 matrix
                if i * 4 + j in self.block.image(): # checks if (i,j) position has a piece of the block
                    self.field[i + self.block.y][j + self.block.x] = self.block.color # looks at the next cell on the field and adds the block's colour to it
                    # when the block intersents this shows its final position on the grid
        self.break_lines() # calls break lines method 
        self.new_block() # calls block method
        if self.intersects(): # since everything else cannot intersect the onky way is for the blocks to reach the top line
            self.state = "gameover" # once the blocks reach that line the game is over 

    def go_space(self): # goes down until it reaches a block/the bottom (prpactically duplicates go_down except for this)
        while not self.intersects(): # creates a loop that goes on as long as the block does to intersect
            self.block.y += 1 # increments vertical position of block by one (moving it down)
        self.block.y -= 1 # after loop ends it decreases y poisiton by 1 to bring it back to its last valid position on the grid
        self.freeze() # calls the method that freezes the block in place

    def go_down(self): # method solely for going down
        self.block.y += 1 # increments vertical position of block by one (moving it down)
        if self.intersects(): # if statement for when block intersects
            self.block.y -= 1 # after loop ends it decreases y poisiton by 1 to bring it back to its last valid position on the grid
            self.freeze() # calls the method that freezes the block in place

    def go_side(self, dx): # method for moving the block across the grid (left and right) that takes in movement parameter
        old_x = self.block.x # keeps track of original position before movement
        self.block.x += dx # updates x-coordinate of block. dx can be negative or positive for left and right
        if self.intersects(): # if the block intersects
            self.block.x = old_x # restrict the sideways momvent of the block and revert to original

    def rotate(self): # method to rotate the block
        old_rotation = self.block.rotation # keeps track of original position before rotation
        self.block.rotate() # calls the rotation method above to select the rotated type of block
        if self.intersects(): # if the block intersects
            self.block.rotation = old_rotation # restrict the rotation of the block and revert to original



pygame.init() # Initialize the game engine

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

screen = pygame.display.set_mode((400, 500)) # intializes and displays screen size 

pygame.display.set_caption("Elili's Tetris Bot") # displays this title when run at the top of the tab

done = False # the game is finished
clock = pygame.time.Clock()
fps = 25 # speed of game
game = Tetris(20, 10) # sets game to an istance of a tetris class with 20 rows and 10 columns in the grid
counter = 0 # sets/retsets counter to zero

pressing_down = False # press down to restart the game

while not done: # while the game is still going
    if game.block is None: # if there is no active game block
        game.new_block() # creates new game block
    counter += 1 # increments counter by one 
    if counter > 100000: # otherwise
        counter = 0 # resets counter to 0

    if counter % (fps // game.level // 2) == 0 or pressing_down: # checks all orientations of the block as it moves down the first few rows
        if game.state == "start": # and if the state of the game is start
            game.go_down() # calls the method to move the block down directly to the bottom (no moving around and much quicker)

    for event in list(pygame.event.get()) + tetris_ai.run_ai(game.field, game.block, game.width, game.height):
            if event.type == pygame.QUIT: # user clicks close button 
                done = True # game comes to an end
            if event.type == pygame.KEYDOWN: # if the user clicks down on a key
                if event.key == pygame.K_UP: # up arrow key is clicked
                    game.rotate() # rotates block
                if event.key == pygame.K_DOWN: # down arrow key is clicked
                    pressing_down = True # moves down quicker
                if event.key == pygame.K_LEFT: # left arrow key is clicked
                    game.go_side(-1) # moves 1 column left
                if event.key == pygame.K_RIGHT: # right arrow key is clicked
                    game.go_side(1) # moves one column right
                if event.key == pygame.K_SPACE: # space bar is clicked
                    game.go_space() # goes really fast down until it reaches bottom
                if event.key == pygame.K_ESCAPE: # esc key is clicked
                    game.__init__(20, 10) # game restarts

    screen.fill(BLACK) # fills screen design with white 

    for i in range(game.height): 
        for j in range(game.width): # nested loop that creates grid index
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1) #display the gray lines across the grid
            if game.field[i][j] > 0: # if there is a block/part there
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
                                # calls and draws a filled rectange of the colour of the corresponding block

    if game.block is not None: # if here is an active block
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.block.image(): # sets the index of the blocks to a linear index of range 0-15 to maeke mapping out the block shapes easier
                    pygame.draw.rect(screen, colors[game.block.color],[game.x + game.zoom * (j + game.block.x) + 1,
                                    game.y + game.zoom * (i + game.block.y) + 1, game.zoom - 2, game.zoom - 2])
                                    # uses a pygame draw function to draw out the block and fill it with the colours. The +1 and -2 create a margin to make the blocks look better 

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, WHITE)
    text_game_over = font1.render("Game Over", True, WHITE)
    text_game_over1 = font1.render("Press ESC", True, WHITE)
    # sets up and displays the written words on the gme in their correspondig colours and fonts. Fonts are retrieved from the pygame system

    screen.blit(text, [0, 0]) # creates a text surface on the pygame screen with the score at that position
    if game.state == "gameover": # if the game is done
        screen.blit(text_game_over, [20, 200]) # draws the text_game_over message at its position
        screen.blit(text_game_over1, [25, 265]) # draws the text_game_over1 message at its position

    pygame.display.flip() # displays the entire contents and changes made to the game/ for the user 
    clock.tick(fps) # controls the speed of the game so it is constant 
    

pygame.quit() # end the progam. The tetris game is complete