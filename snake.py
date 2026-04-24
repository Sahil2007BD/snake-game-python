import tkinter
import random



ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE




class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y








#game window

window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)

canvas.pack()
window.update()



#center the snake in the middle of the window

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")






#initialize the game

snake = Tile(5*TILE_SIZE,5*TILE_SIZE) #single tile snake for now
food = Tile(10*TILE_SIZE,10*TILE_SIZE) #single tile food for now
snake_body = [] #list to hold the body of the snake, will be used to grow the snake when it eats food and to check for collisions with itself
velocity_x = 0
velocity_y = 0
score = 0
game_over = False

def change_direction(e):
    # print(e.keysym)

    global velocity_x, velocity_y, game_over, score
    if game_over:
        return

    if (e.keysym == "Up" and velocity_y != 1):
        velocity_x = 0
        velocity_y = -1
    elif (e.keysym == "Down" and velocity_y != -1):
        velocity_x = 0
        velocity_y = 1
    elif (e.keysym == "Left" and velocity_x != 1):
        velocity_x = -1
        velocity_y = 0
    elif (e.keysym == "Right" and velocity_x != -1):
        velocity_x = 1
        velocity_y = 0


def move():
    global snake, game_over , food , snake_body, velocity_x, velocity_y, score
    if game_over:
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #collision with food
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(snake.x, snake.y)) #add a new tile to the snake body at the current position of the snake
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1


    #update the position of the snake
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i==0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y


    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE


def draw():
    global snake, food, snake_body, velocity_x, velocity_y, score, game_over
    move()

    canvas.delete("all") #clear the canvas before redrawing
    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "green")

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "red")
    

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "red")




    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text = "Game Over", fill = "white", font = ("Arial", 24))
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30, text = f"Score: {score}", fill = "white", font = ("Arial", 18))
    else:
        canvas.create_text(50, 40, text = f"Score: {score}", fill = "white", font = ("Arial", 18))
    window.after(95, draw)
draw()


window.bind("<KeyPress>", change_direction)
window.mainloop()