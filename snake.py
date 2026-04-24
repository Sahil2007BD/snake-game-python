import tkinter as tk
import random

# Grid settings
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Window setup
window = tk.Tk()
window.title("Snake Game 🐍")
window.resizable(False, False)

canvas = tk.Canvas(window, bg="#111", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
canvas.pack()

# Center window
window.update()
x = (window.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
y = (window.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


# Game state
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []

velocity_x = 0
velocity_y = 0

score = 0
high_score = 0
game_over = False
game_started = False


def reset_game():
    global snake, food, snake_body, velocity_x, velocity_y, score, game_over, game_started

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = Tile(random.randint(0, COLS - 1) * TILE_SIZE,
                random.randint(0, ROWS - 1) * TILE_SIZE)
    snake_body.clear()

    velocity_x = 0
    velocity_y = 0

    score = 0
    game_over = False
    game_started = False


def change_direction(e):
    global velocity_x, velocity_y, game_over, game_started

    if e.keysym == "r":
        reset_game()
        return

    if game_over:
        return

    game_started = True

    if e.keysym == "Up" and velocity_y != 1:
        velocity_x, velocity_y = 0, -1
    elif e.keysym == "Down" and velocity_y != -1:
        velocity_x, velocity_y = 0, 1
    elif e.keysym == "Left" and velocity_x != 1:
        velocity_x, velocity_y = -1, 0
    elif e.keysym == "Right" and velocity_x != -1:
        velocity_x, velocity_y = 1, 0


def move():
    global game_over, food, score, high_score

    if not game_started or game_over:
        return

    # Wall collision
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        high_score = max(high_score, score)
        return

    # Self collision
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            high_score = max(high_score, score)
            return

    # Food collision
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(snake.x, snake.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Move body
    for i in range(len(snake_body) - 1, -1, -1):
        if i == 0:
            snake_body[i].x = snake.x
            snake_body[i].y = snake.y
        else:
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y

    # Move head
    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE


def draw_grid():
    for i in range(0, WINDOW_WIDTH, TILE_SIZE):
        canvas.create_line(i, 0, i, WINDOW_HEIGHT, fill="#222")
    for i in range(0, WINDOW_HEIGHT, TILE_SIZE):
        canvas.create_line(0, i, WINDOW_WIDTH, i, fill="#222")


def draw():
    canvas.delete("all")

    draw_grid()
    move()

    # Food
    canvas.create_oval(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="#00ff9c", outline="")

    # Snake head
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="#ff4c4c")

    # Snake body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="#ff7777")

    # UI Text
    canvas.create_text(80, 20, text=f"Score: {score}", fill="white", font=("Consolas", 14))
    canvas.create_text(220, 20, text=f"High: {high_score}", fill="white", font=("Consolas", 14))

    if not game_started:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                           text="Press Arrow Key to Start",
                           fill="white", font=("Arial", 18))

    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                           text="GAME OVER",
                           fill="red", font=("Arial", 28))
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40,
                           text="Press R to Restart",
                           fill="white", font=("Arial", 16))

    window.after(100, draw)


draw()
window.bind("<KeyPress>", change_direction)
window.mainloop()