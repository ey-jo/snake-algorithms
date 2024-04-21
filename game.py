"""
The screen is divided into cells with a size of CELL_SIZE, around which there is a row of empty pixels.
The snake has its own coordinate field (field), which is translated as parameters for the field in the update function.
At the start, the snake moves away from the edge.
snake: [[head: cell_x, cell_y][body1: cell_x, cell_y]...]

grafics made by Finley
"""


import pygame
import random
import sys
from algorithm import algorithm as algo
from stats import show
from manual import manual as m
pygame.init()



# screen info
WINDOW_WIDTH = pygame.display.Info().current_w
WINDOW_HEIGHT = pygame.display.Info().current_h
CELL_SIZE = 30
NUM_FOOD = 1   #not too much (limit about 10)


#load images
images = [
    pygame.transform.scale(pygame.image.load("./assets/head.png"), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load("./assets/straight.png"), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load("./assets/corner.png"), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load("./assets/tail.png"), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load("./assets/apple.png"), (CELL_SIZE, CELL_SIZE))
]


try:
    space = (sys.argv[2].lower() == "s") * show.get_space()
except:
    space = 0
tick, speed = 100, 1


# initialization
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN, pygame.RESIZABLE)
screen = pygame.display.set_mode((360 + space, 360), pygame.RESIZABLE) #temp
pygame.display.set_caption('Snake') 
clock = pygame.time.Clock()

# create event
RESTART = pygame.USEREVENT + 1


# colors
GREY = (150, 150, 150)
ORANGE = (220, 133, 40)
LIGHT_GREEN = (30, 212, 65)
DARK_GREEN = (10, 120, 30)
BLUE = (20, 20, 200)
RED = (235, 64, 52)
WHITE = (255, 255, 255)


# define field
def setup_field():
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()
    width = WINDOW_WIDTH - space
    COLS = int(WINDOW_HEIGHT / CELL_SIZE)
    ROWS = int(width / CELL_SIZE / 2) * 2   #only even numbers possible to use hamiltonian cycle
    x_frame = (width - ROWS * CELL_SIZE) /2
    y_frame = (WINDOW_HEIGHT - COLS * CELL_SIZE )/ 2


    """
    [[row:[element][element]
      row:[element][element]
      row:[element][element]]]
    """

    x, y = x_frame, y_frame
    field = [[] for row in range(ROWS)]
    for row in range(ROWS):
        for column in range(COLS):
            field[row].append([x, y])
            y += CELL_SIZE
        x += CELL_SIZE
        y = y_frame
    
    cells = []
    for row in range(ROWS):
        for col in range(COLS):
            cells.append([row, col])

    #start with one random square: the head
    snake = [[random.randint(0, ROWS -1), random.randint(0, COLS -1)]]

    return snake, ROWS, COLS, width, x_frame, y_frame

def cell_grid():
    cells = []
    for row in range(ROWS):
        for col in range(COLS):
            cells.append([row, col])
    return cells


def get_free_cells():
    free_cells = []
    for element in CELLS:
        if element not in snake:
            free_cells.append(element)
    return free_cells

def place_food(food):
    free_cells = get_free_cells()
    max_space = len(free_cells)
    if len(food) < min(NUM_FOOD, max_space):
        for apple in range(min(NUM_FOOD, max_space) - len(food)):
            food.append(free_cells[random.randint(0, len(free_cells) -1)])

    return food, free_cells


def get_field(pos):
    #takes input pos[x, y] and return coordinates to draw
    return pos[0] * CELL_SIZE + x_frame, pos[1] * CELL_SIZE + y_frame


#show snake images
def rotate(image, direction):
    #default 1, 0 right
    if direction == [-1, 0]:
        return pygame.transform.rotate(image, 180)
    elif direction == [0, 1]:
        return pygame.transform.rotate(image, -90)
    elif direction == [0, -1]:
        return pygame.transform.rotate(image, 90)
    return image

def show_images(type, posX=0, posY=0):
    #snake

    if type:
        screen.blit(rotate(images[0], current_dir), get_field(snake[0]))
        for part in range(1, len(snake) -1):
            #staright
            dif = [snake[part-1][i] - snake[part+1][i] for i in range(2)]
            if abs(dif[0]) == 2:
                screen.blit(images[1], get_field(snake[part]))
            elif abs(dif[1]) == 2:
                screen.blit(rotate(images[1], [0, 1]), get_field(snake[part]))
            #corner
            else:
                dif = [(snake[part-1][i] - snake[part][i]) + (snake[part+1][i] - snake[part][i]) for i in range(2)]
                if dif == [1, -1]:
                    screen.blit(rotate(images[2], [0, -1]), get_field(snake[part]))
                elif dif == [-1, -1]:
                    screen.blit(rotate(images[2], [-1, 0]), get_field(snake[part]))
                elif dif == [-1, 1]:
                    screen.blit(rotate(images[2], [0, 1]), get_field(snake[part]))
                else:
                    screen.blit(images[2], get_field(snake[part]))
            


        if len(snake) > 1:
            screen.blit(rotate(images[3], [snake[-2][i] - snake[-1][i] for i in range(2)]), get_field(snake[-1]))



    #food
    else:
        screen.blit(images[4], (posX, posY))


def stats():
    dir_naming = {
        (0, 1) : "down",
        (0, -1) : "up",
        (-1, 0) : "left",
        (1, 0): "right"
    }
    stats = []
    stats.append(["score: " + str(len(snake)) + " / " + str(ROWS * COLS), WHITE])
    stats.append(["speed: " + str(speed), WHITE])
    if tuple(next_dir) != (0, 0):
        stats.append(["best Move: " + dir_naming[tuple(next_dir)], DARK_GREEN])
    show.show_stats(screen, width, stats)


def update():
    screen.fill((0,0,0))
    #check available
    available = algo.reach(CELLS, snake)

    if space != 0:
        stats()
    
    #checks positions to color
    for row in range(ROWS):
        for col in range(COLS):
            color = GREY #default
            x, y = get_field([row, col])

            #show reach
            if [row, col] in available or [row, col] in snake:
                color = BLUE

            #draw default background
            pygame.draw.rect(screen, color, (x +1, y +1, CELL_SIZE -2, CELL_SIZE -2))

            #food
            if [row, col] in food:
                show_images(False, x, y)

    #snake
    show_images(True)

    
    #hamiltonian cycle
    if show_cycle:
        show.draw_cycle(screen, x_frame, y_frame, CELL_SIZE, WHITE, cycle)

    pygame.display.update()

def move(next_dir, current_dir, food, last_head, free_cells):
    
    #unable to move backwards
    if current_dir != [0, 0]:
        if next_dir[0] * -1 == current_dir[0] or next_dir[1] * -1 == current_dir[1]:
            next_dir = current_dir
    
    #save last head position
    last_head = snake[0][:]
    #apply current direction
    for i in range(2):
        snake[0][i] += next_dir[i]
    
    #check for food
    if snake[0] in food:
        food.remove(snake[0])

        #extend snake body
        snake.insert(1, last_head)
        food, free_cells = place_food(food)
    else:
        #move body forward (last elemet moves to where the head was)
        if len(snake) >= 2:
            for part in range(len(snake)-1, 1, -1):
                snake[part] = snake[part-1]
            snake[1] = last_head

    #save local values
    return next_dir, food, last_head, free_cells


def calc_game():
    if ((snake[0][0] < 0 or snake[0][1] < 0) or (snake[0][0] >= ROWS or snake[0][1] >= COLS) or snake[0] in snake[1:]):
        loose = True
    else:
        loose = False


    #loose
    if loose:
        return(1)

    #win
    elif (len(free_cells) == 0):
        return(5)

    return False



def again(time):
    algo.scores(score_name, len(snake), moves, (ROWS, COLS))
    print("Score:", str(int(len(snake) / (ROWS * COLS) * 100)) + "%,", len(snake))

    if time == 1:
        color = RED
    elif time == 5:
        color = LIGHT_GREEN
        print("Perfekt Score")
        print("Moves:", moves)

    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, color, (get_field((row, col))[0] +1, get_field((row, col))[1] +1, CELL_SIZE -2, CELL_SIZE -2))
    
    pygame.display.update()
    pygame.time.delay(time * 1000)
    pygame.event.post(pygame.event.Event(RESTART))


def get_controls():
    #control of algorithm
    arg = int(sys.argv[1])



    #manual gameplay
    if arg == 0:
        score_name = "manual"
        input = user_in

    #algorithms
    if arg == 1:
        score_name, input = algo.straight(snake[0], food)
    elif arg == 2:
        score_name, input = algo.turning(snake[0], food, current_dir)
    elif arg == 3:
        score_name, input = algo.smart(CELLS, snake, food)
    elif arg == 4:
        score_name, input = algo.perfect(CELLS, snake, food, current_dir, len(free_cells))
    elif arg == 5:
        score_name, input = algo.gab(CELLS, snake, food, current_dir, len(free_cells))[:2]

    #hamiltonian
    elif arg == 6:
        score_name, input = algo.move_along(cycle, snake[0])
    elif arg == 7:
        score_name, input = algo.shortcut(cycle, snake, food, current_dir)

    return score_name, input




# game
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE or event.type == RESTART:
            #start of game and when windowsize changes

            #global variables
            snake, ROWS, COLS, width, x_frame, y_frame = setup_field()
            CELLS = cell_grid()
            food, free_cells = place_food([])
            last_head, empty_fields = [], []
            next_dir, current_dir, user_in = [0, 0], [0, 0], [0, 0]
            count_time, pressed, t_val = 0, False, 0
            show_cycle, dead = False, False

            print("field of:",COLS,"*", ROWS)
            screen.fill((0,0,0))

            moves = 0
            """##########################"""
            #hamiltonian
            if 7 <= int(sys.argv[1]) <= 8:
                cycle = algo.pre_hamiltonian(ROWS, COLS)
                show_cycle = True
            """##########################"""

            update()




        #controls
        if event.type == pygame.MOUSEWHEEL:
            #change game speed
            t_val += (event.y * -1)
            speed = 2 ** t_val
            update()
        
        pushedKey = pygame.key.get_pressed()
        if pushedKey[pygame.K_SPACE]:
            #toggle freeze
            if not pressed:
                pressed = True

                if speed != 0:
                    speed = 0
                    update()
                else:
                    speed = 1
        else:
            pressed = False
        
        if pushedKey[pygame.K_1]:
            speed = 1
        elif pushedKey[pygame.K_2]:
            speed = 3
        elif pushedKey[pygame.K_3]:
            speed = 5


    #user input for manual gameplay
    if int(sys.argv[1]) == 0:
        user_in = m.get_input(user_in)


    #variable speed
    tick, factor = algo.get_tick(speed)
    if speed <= 0 or count_time < factor * 1/tick:
        count_time += 1
    else:
        count_time = 0

        #check for collision and game end
        if dead:
            again(dead)
        else:
            score_name, next_dir = get_controls()
            current_dir, food, last_head, free_cells = move(next_dir, current_dir, food, last_head, free_cells)
            moves += 1
        dead = calc_game()
        update()

    
    clock.tick(tick)  #per tick

#end game
pygame.quit()