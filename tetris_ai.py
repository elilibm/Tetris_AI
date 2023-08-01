import pygame

class Event():
    type = None # sets type to none 
    key = None # sets key to none

    def __init__(self, type, key):
        self.type = type # sets outer value of type to value passed in through parameters
        self.key = key # sets outer value of key to value passed in through parameters
counter = 0 # initializes counter to 0

def run_ai(): # creates a run_ai method to rotate the block
    global counter # use the same counter variable used outside of the function
    counter += 1 # increments the counter 
    if counter < 3: 
        return [] # returns an empty list
    counter = 0 # else set counter to 0
    e = Event(pygame.KEYDOWN, pygame.K_UP) # mimcs an AI clicking the UP arrow key
    return [e] # returns a block rotation

def intersects(game_field, x, y, game_width, game_height, game_block_image): # checks if block intersects wuth game field at the x and y positions
    intersection = False # initializes ad sets intersection to false (none)
    for i in range(4): 
        for j in range(4): # iterates over 4x4 matrix of the block
            if i * 4 + j in game_block_image: # checks if (i,j) position has a piece of the block
                if i + y > game_height - 1 or j + x > game_width - 1 or j + x < 0 or game_field[i + y][j + x] > 0:
                    # subtracts one if block goes out of field, greater than 0 if a block is already there
                    intersection = True # if the position does not equal zero then there is an intersection
    return intersection # returns whether there was or was not an intersection

def simulate(game_field, x, y, game_width, game_height, game_block_image): # defines simulate function which tries to find highest value ofy before the game field intersects
    while not intersects(game_field, x, y, game_width, game_height, game_block_image): # while the block does not intserect
        y += 1 # incremnet y by one (movie y down by one)
    y -= 1 # subract 1 if it intersects to get the last valid position of the block

    height = game_height # set height to the height of the game field
    holes = 0 # start the number of holes off at 0
    filled = [] # create an empty list that will store the poisitions of filled cells 
    breaks = 0 # sets breaks to 0
    for i in range(game_height-1, -1, -1): # for loop that itertes from game height-1 to 0
        it_is_full = True # sets condition to true to check if row is full
        prev_holes = holes # sets prev_holes to holes to keep track of the previous row of holes
        for j in range(game_width): # iterates from 0 to game width
            u = '_' #placeholder value inside outer for loop
            if game_field[i][j] != 0: # if the cell does not equal 0 (something is there)
                u = "x" # set u to x to map out the game field using '_' and 'x'
            for ii in range(4):
                for jj in range(4): # runs through block 4x4 matrix
                    if ii * 4 + jj in game_block_image: # if one of the cells has the block's image
                        if jj + x == j and ii + y == i: # if the calculated position of the block matches the current j and i coordinates
                            u = "x" # if above conditions are true then u = x (updates to the new calculated position of the block)

            if u == "x" and i < height: # checks if there is something at that cell and if the current height of that cell is less than the height variable
                height = i # sets height to the height of that filled cell to keep track of the lowest position of the block on the game 
            if u == "x": # checks if the cell has something
                filled.append((i, j)) # creates tuple (i,j) for the list that represents a cell in the game filed that is part of the block
                for k in range(i, game_height): # iterates values of k from current value of i to game_height-1
                    if (k, j) not in filled: # checks if current cell is not marked as filled by the block in the tuple
                        holes += 1 # increments holes by 1 to keep track of empty cells
                        filled.append((k,j)) # adds the tuple to the filled list marking that coordinate as filled
            else: # probably if the cell is not part of the block 
                it_is_full = False # the block is not fully placed on the game field 
        if it_is_full: # check if it is True
            breaks += 1 # adds 1 to break
            holes = prev_holes # sets holes to the number of previous holes (resets the value)

    return holes, game_height-height-breaks # returns these variables

def best_rotation_position(game_field, game_block, game_width, game_height): #method to find the best rotation position
    best_height = game_height # initializes best height to game height
    best_holes = game_height*game_width # initializes holes to dimensions of field
    best_position = None # assigns best position to none
    best_rotation = None # assigns best rotation to none 

    for rotation in range(len(game_block.blocks[game_block.type])): # uses for loop to iterate through possible rotations
        blo = game_block.blocks[game_block.type][rotation] # assigns current rotation/block patter to blo
        for j in range(-3, game_width): # loop that iterates through horizontal positions on the field
            if not intersects(game_field, j, 0, game_width, game_height, blo): # checks if current position does not intersect with game field
                holes, height = simulate(game_field, j, 0, game_width, game_height, blo) # if it doesn't let the block move down until it intersects
                if best_position is None or best_holes > holes or best_holes == holes and best_height > height: # if any conditions are met then this is not best rotation
                    best_height = height  
                    best_holes = holes
                    best_position = j
                    best_rotation = rotation
                    # best positions and variables are updated to actual best rotations and positions
    return best_rotation, best_position # returns the best possible move

def run_ai(game_field, game_block, game_width, game_height): # defines a run_ai function
    global counter # use the same counter variable used outside of the function
    counter += 1 # increments the counter 
    if counter < 3: 
        return [] # returns an empty list
    counter = 0 # else set counter to 0
    rotation, position = best_rotation_position(game_field, game_block, game_width, game_height) # calls emthod abd assigns return values to rotation and position
    if game_block.rotation != rotation: # if current block rotation is not equal to the best rotation
        e = Event(pygame.KEYDOWN, pygame.K_UP) # the AI presses the up arrow key
    elif game_block.x < position: # if current x-position of game block is less than best position
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT) # AI presses the right arrow key
    elif game_block.x > position: # if current y-position of game block is greater than best position
        e = Event(pygame.KEYDOWN, pygame.K_LEFT) # AI presses the left arrow key
    else: # if none of the above conditions
        e = Event(pygame.KEYDOWN, pygame.K_SPACE) # AI presses the space key
    return [e] # returns a list with the AI's decision on what key press

