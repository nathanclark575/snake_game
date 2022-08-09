import pygame
import time
import random

# This program is a recreation of snake the game

# there are three difficulty settings for the user to chose between in the console
# there is a game loop that allows for the game to be replayed or exited after losing

print("\nSnake 1.0 by Nathan \n")

print("The rules of the game are as follows:")
print("1) Points are gained when the snake (white) eats the food (green)")
print("2) The game ends when the snake goes out of bounds")
print("3) Or if the snake eats itself\n")

# difficulty setting
difficulty = input("""please select the game dificulty (type 1/2/3)
1) Easy
2) Medium
3) hard\n""")

# starts the game
pygame.init()

# determines inital size of the snake and food
block_size = 10

# the speed of snake is based on the difficulty setting
if difficulty == "1":
    snake_speed = 10
elif difficulty == "2":
    snake_speed = 15
else:
    snake_speed = 20

# colour variables
blue = (0, 0, 225)
red = (225, 0, 0)
white = (225, 225, 225)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 102)

# fonts
#SysFont(font, size),
font_style = pygame.font.SysFont(None, 25)
score_font = pygame.font.SysFont(None, 35)

# genrates display
display_width = 600
display_height = 400
display = pygame.display.set_mode((display_width, display_height))

# allows changes to be made to the display
pygame.display.update()

# title added
pygame.display.set_caption('Snake 1.0 by Nathan')

# clock to keep track of time
clock = pygame.time.Clock()

# a function to keep track of and display the players score
def display_score(turn_score):
    value = score_font.render("Your Score " + str(turn_score), True, white)
    display.blit(value, [0, 0]) # blit overlaps value at the specified position on the display


# a function that draws the snake and allows its size to change upon eating food
def snake(block_size, snake_list):
    for block in snake_list:
        # pygame.draw.rect(surface the rectangle is drawn on, colour, [x_coordinate, y_coordinate, x_size, y_size])
        pygame.draw.rect(display, white, [block[0], block[1], block_size, block_size])


# Allows a message to be genrated with a specified text and colour
def message(text, colour):
    text_style = font_style.render(text, True, colour)
    display.blit(text_style, [display_width / 4, display_height / 4])


# game loop function to allow the option to either play another game or close it after losing
def game_loop():
    game_over = False # causes display to close if true
    game_close = False # causes current game to close if true

    # setting the inital coordinates of the snake, need to do this inside the game_loop function
    x_coordinate = display_width / 2
    y_coordinate = display_height / 2

    # define these so that the position of the snake can be updated in the loop
    x_change = 0
    y_change = 0

    # in itilizing snake list - this records the locations of the blocks that make up the snake
    snake_list = []
    snake_length = 1

    # setting the coordinate of the food

    # the block_size and factors of 10 are used to make sure the food is not exactly at the end as getting it would
    # cause the game to close upon eating it
    x_food = round(random.randrange(0, display_width - block_size) / 10) * 10
    y_food = round(random.randrange(0, display_height - block_size) / 10) * 10


# the folowing loops runs when the game is open, until q is pressed in order to exit
    while not game_over:

        # when the snake goes out of the display bounds
        while game_close == True: # turn ends

            # update to a clear display
            display.fill(black)

            # give a message and the option to play again or quit
            message("GAME OVER! Q to quit C to play again", red)
            pygame.display.update()

            # carry out input based on the key pressed in the message prompt
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True # so the game/main while loop can be closed
                        game_close = False # so the while loop can be closed
                    if event.key == pygame.K_c:
                        game_loop() # so it goes back to where game loop is called by defining it


        # monitors events - i.e. key presses
        for event in pygame.event.get():

            # causes the close button to end the game, red x in top left hand corner
            if event.type == pygame.QUIT:
                game_over = True # display closes

            # add key event movment
            if event.type == pygame.KEYDOWN:
                # relate a specific key to a movement
                if event.key == pygame.K_LEFT:
                    x_change = - block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = - block_size
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = block_size

        # setting limts to the movment equal to the dimensions of the display, so that if the snake exits the display
        # the turn will be over
        if x_coordinate >= display_width or x_coordinate < 0 or y_coordinate >= display_height or y_coordinate < 0:

            # exits the loop
            game_close = True # turn over

        # updating the coordinates of the snake based on the user input
        x_coordinate += x_change
        y_coordinate += y_change

        # fill is used in order to fill the display with a chosen colour
        display.fill(black)

        # draw the food
        pygame.draw.rect(display, green, [x_food, y_food, block_size, block_size])

        # the snake head changes relitive to the starting coordinates by the change in x and y caused by kepad interation
        snake_head = []
        # this updates after every change as the snake head will be at a new block
        snake_head.append(x_coordinate)
        snake_head.append(y_coordinate)
        # each snake block coordinate is saved as part of a 2D array [x, y]
        snake_list.append(snake_head)

        # the following if statment removes the old coordinates from the list so that the snake is plotted and not its
        # whole jorney. However the snake length constaint can be incresed if the snake eats some food alowing it to
        # become a longer snake. (code for this follows, it is one of the following if statments.)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # if the snake eats itself the turn is over
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # the snake needs to be updated in the display with its new coordiantes and/or size by calling the snake function
        snake(block_size, snake_list)

        # dipay the score
        display_score(snake_length - 1)

        # updates the diplay in order to show the snake, food, and the turn score after each keybord input
        pygame.display.update()

        # recognizing when the snake and food have the same coordinates, i.e. the snake is eating
        if x_coordinate == x_food and y_coordinate == y_food:
            # genrate a new peice of food
            x_food = round(random.randrange(0, display_width - block_size) / 10) * 10
            y_food = round(random.randrange(0, display_height - block_size) / 10) * 10
            # make the snake one block longer as it has eaten
            snake_length += 1

        # tells the game clock how fast to move the snake on the display
        clock.tick(snake_speed)

    # closes the display and exits the game
    pygame.quit()
    quit()

# Driver code that starts the game
game_loop()