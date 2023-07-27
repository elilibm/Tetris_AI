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

def intersects(game_field, x, y, game_width, game_height, game_block_image):
    intersection = False
    for i in range(4):
        for j in range(4):
            if i * 4 + j in game_block_image:
                if i + y > game_height - 1 or \
                        j + x > game_width - 1 or \
                        j + x < 0 or \
                        game_field[i + y][j + x] > 0:
                    intersection = True
    return intersection
def simulate(game_field, x, y, game_width, game_height, game_block_image):
    while not intersects(game_field, x, y, game_width, game_height, game_block_image):
        y += 1
    y -= 1

    height = game_height
    holes = 0
    filled = []
    for i in range(game_height-1, -1, -1):
        for j in range(game_width):
            u = '_'
            if game_field[i][j] != 0:
                u = "x"
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in game_block_image:
                        if jj + x == j and ii + y == i:
                            u = "x"

            if u == "x" and i < height:
                height = i
            if u == "x":
                filled.append((i, j))
                for k in range(i, game_height):
                    if (k, j) not in filled:
                        holes += 1
                        filled.append((k,j))

    return holes, game_height-height

def best_rotation_position(game_field, game_block, game_width, game_height):
    best_height = game_height
    best_holes = game_height*game_width
    best_position = None
    best_rotation = None

    for rotation in range(len(game_block.blocks[game_block.type])):
        blo = game_block.blocks[game_block.type][rotation]
        for j in range(-3, game_width):
            if not intersects(
                    game_field,
                    j,
                    0,
                    game_width,
                    game_height,
                    blo):
                holes, height = simulate(
                    game_field,
                    j,
                    0,
                    game_width,
                    game_height,
                    blo
                )
                if best_position is None or best_holes > holes or \
                    best_holes == holes and best_height > height:
                    best_height = height
                    best_holes = holes
                    best_position = j
                    best_rotation = rotation
    return best_rotation, best_position

def run_ai(game_field, game_block, game_width, game_height):
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    rotation, position = best_rotation_position(game_field, game_block, game_width, game_height)
    if game_block.rotation != rotation:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
    elif game_block.x < position:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif game_block.x > position:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        e = Event(pygame.KEYDOWN, pygame.K_SPACE)
    return [e]

def simulate(game_field, x, y, game_width, game_height, game_block_image):
    while not intersects(game_field, x, y, game_width, game_height, game_block_image):
        y += 1
    y -= 1

    height = game_height
    holes = 0
    filled = []
    breaks = 0
    for i in range(game_height-1, -1, -1):
        it_is_full = True
        prev_holes = holes
        for j in range(game_width):
            u = '_'
            if game_field[i][j] != 0:
                u = "x"
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in game_block_image:
                        if jj + x == j and ii + y == i:
                            u = "x"

            if u == "x" and i < height:
                height = i
            if u == "x":
                filled.append((i, j))
                for k in range(i, game_height):
                    if (k, j) not in filled:
                        holes += 1
                        filled.append((k,j))
            else:
                it_is_full = False
        if it_is_full:
            breaks += 1
            holes = prev_holes

    return holes, game_height-height-breaks