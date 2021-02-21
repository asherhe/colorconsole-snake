import colorconsole, keyboard, ctypes, time, random, math, os

# Set up console
stdout = colorconsole.ColorConsole("Snake");

# Initiate variables

# The string value of a square block
block = "  "
# The positions of each segment of the snake
snake = [[1, 10]]

food = [18, 10]
dir = [1, 0]
changeddir = False
size = [20, 20]
starttime = time.time()
tickspassed = 0
speed = 0.25
lastSeg = [0, 10]
lastFood = None

def calctextpos(pos):
  '''
  Calculates the position in terms of rows and columns
  '''
  return pos[1] + 2, pos[0] * 2 + 3


def render():
  '''
  Renders the current frame of the snake game
  '''
  global snake, food, lastSeg, lastFood
  # Writes the length of the snake
  stdout.printAt(str(len(snake)), size[1]+3, 8, rgbFg="010")
  # Draws the food
  stdout.printAt(block, *calctextpos(food), rgbBg="100")
  # Shades out the last position of the last segment and food
  stdout.printAt(block, *calctextpos(lastSeg), rgbBg="000")
  try:
    stdout.printAt(block, *calctextpos(lastFood), rgbBg="000")
  except:
    pass
  # Renders the snake
  stdout.printAt(block, *calctextpos(snake[-1]), rgbBg="010")

def update():
  '''
  Updates the current state of the snake game
  '''
  global snake, food, starttime, tickspassed, speed, lastFood, lastSeg
  # Get the number of ticks passed
  tickspassed = round(4*(time.time() - starttime))
  # Alter the speed depending on the length of the snake and how long the game has been played
  newspeed = 0.25 - (tickspassed * len(snake)**0.5 / 10000)
  if newspeed < speed:
    speed = newspeed
  else:
    speed -= 0.0001
  # Move snake
  head = snake[-1]
  snake.append([head[0] + dir[0],
    head[1] + dir[1]])

  # Check for death
  if not (-1 < head[0] < size[0] and -1 < head[1] < size[1]):
    end("You got a concussion.")
  elif head in snake[:-2]:
    end("You ate yourself.")

  # Check if food has been eaten
  if food in snake:
    lastFood = food
    food = [random.randint(0, size[0]-1),
      random.randint(0, size[1]-1)]
  else:
    lastFood = None # To prevent a hole in the snake during rendering
    lastSeg = snake[0]
    snake = snake[1:]



def end(deathmessage):
  '''
  Sends a death message and ends the game with an infinite loop
  '''
  stdout.printAt("%s Final Length: %d" % (deathmessage, len(snake)-1), *calctextpos([0, 0]), rgbFg="111", rgbBg="100")
  while True:
    pass

def setdir(dirx, diry):
  '''
  Sets the direction, putting the current direction and if the player has already changed direction into thought
  '''
  global dir
  if not (-dir[0] == dirx or -dir[1] == diry):
          dir = [dirx, diry]

# Maps hotkeys for direction changing
keyboard.add_hotkey("UP", lambda: setdir(0, -1))
keyboard.add_hotkey("DOWN", lambda: setdir(0, 1))
keyboard.add_hotkey("LEFT", lambda: setdir(-1, 0))
keyboard.add_hotkey("RIGHT", lambda: setdir(1, 0))

# Draws the playfield
stdout.printAt(block * (size[0]+2), *calctextpos([-1, -1]), rgbBg="111")
for i in range(1, size[1]+1):
  stdout.printAt(block, *calctextpos([-1, -1+i]), rgbBg="111")
  stdout.printAt(block*size[0], *calctextpos([0, -1+i]))
  stdout.printAt(block, *calctextpos([20, -1+i]), rgbBg="111")
stdout.printAt(block * (size[0]+2), *calctextpos([-1, 20]), rgbBg="111")

stdout.printAt("Score: ", *calctextpos([-1, 21]), rgbFg="100")
# Mainloop
while True:
  changeddir = False
  update()
  render()
  time.sleep(speed)
