#__________Sources___________
# Source 1: https://www.youtube.com/watch?v=UZg49z76cLw
# Source 2: https://www.youtube.com/watch?v=Q-__8Xw9KTM&t=2815s


import pygame
import sys
from time import sleep
from random import randint


# Initializing pygame and fonts.
pygame.init()
pygame.font.init()
main_font = pygame.font.SysFont("comicsans",30)


# Setting the frame rate of the game. (Referenced off Source 1.)
clock = pygame.time.Clock()


# (Referenced off Source 2.)
screen = pygame.display.set_mode((500,500))

tommy = pygame.image.load("Pygame Sprites/Tommy side.png").convert_alpha() 
tommy = pygame.transform.scale2x(tommy)

background = pygame.image.load("Pygame Sprites/Background.png").convert()
background = pygame.transform.scale2x(background)

blob = pygame.image.load("Pygame Sprites/blob.png").convert_alpha()
blob = pygame.transform.scale2x(blob)

start_screen = pygame.image.load("Pygame Sprites/start screen.png").convert_alpha()
start_screen = pygame.transform.scale2x(start_screen)

end_screen = pygame.image.load("Pygame Sprites/end screen.png").convert_alpha()
end_screen = pygame.transform.scale2x(end_screen)


x = 50
y = 165
tommy_lives = 5
points = 0


blob_enemies = []
letter_keys = ["w", "s", "a", "d"]
high_score = [0]

class Blob(object):
  # (Referenced off Source 2.)
  def __init__(self):
    self.alive = True
    self.image = blob
    self.rect = self.image.get_rect()
    
    # Generating a random letter key from W, A, S, and D.
    global letter_keys
    self.letter_key = letter_keys[randint(0,3)]

    # X and Y Values of the blob (enemy).
    self.blob_x = randint(200,500)
    self.blob_y= randint(0,500)

    # Variables used following equations.
    self.rect.center = (self.blob_x, self.blob_y)
    self.x_math = abs(self.blob_x - x)
    self.y_math = abs(self.blob_y - y)
    self.movement_num = 40

    screen.blit(self.image, (self.rect.center))
    pygame.display.update()


  # Function that moves the enemy to the player sprite tommy, it calculates distance for both the X and Y coordinates of the enemy's spawning position.
  def move(self):
    if self.blob_x < x:
      self.blob_x += self.x_math/self.movement_num
      if self.blob_y < y:
        self.rect.center = (self.blob_x, self.blob_y + (self.y_math)/self.movement_num)
        self.blob_y+=self.y_math/self.movement_num
      elif self.blob_y == y:
        self.rect.center = (self.blob_x, self.blob_y)
      else:
        self.rect.center = (self.blob_x, self.blob_y - (self.y_math)/self.movement_num)
        self.blob_y-=(self.y_math)/self.movement_num

    elif self.blob_x == x:
      if self.blob_y < y:
        self.rect.center = (self.blob_x, self.blob_y + (self.y_math)/self.movement_num)
        self.blob_y+=self.y_math/self.movement_num
      elif self.blob_y == y:
        self.alive = False
        (self)
        del self
      else:
        self.rect.center = (self.blob_x, self.blob_y - (self.y_math)/self.movement_num)
        self.blob_y-=(self.y_math)/self.movement_num

    else:
      self.blob_x-=self.x_math/self.movement_num
      if self.blob_y < y:
        self.rect.center = (self.blob_x, self.blob_y + (self.y_math)/self.movement_num)
        self.blob_y+=self.y_math/self.movement_num
      elif self.blob_y == y:
        self.rect.center = (self.blob_x, self.blob_y)
      else:
        self.rect.center = (self.blob_x, self.blob_y - (self.y_math)/self.movement_num)
        self.blob_y-=(self.y_math)/self.movement_num   
      
      screen.blit(self.image, (self.rect.center))
      pygame.display.update() 
      sleep(0.04)

  # Function that detects whether the random key is being pressed or not and displays the random key on the pygame screen.
  def input_key(blob_list, key, function):
    global letter_keys
    global blob_enemies
    global letter_key
    global main_font
    global x
    global y
    if function == "detect":
      for i in range (len(letter_keys)):
        keys = pygame.key.get_pressed()
        if key == letter_keys[i]:
          if keys[int(ord(letter_keys[i]))]:
            return True
    else:
      letter_key_display = main_font.render(blob_enemies[0].letter_key, 1, (0,0,0))
      screen.blit(letter_key_display, (x,y+50))


# Main function.
def main():
  global tommy_lives
  global points
  global high_score

  # Function that updates the pygame screen every time the loop is run.
  def redraw_window():
    global tommy_lives
    global letter_key
    global letter_keys
    global main_font
    global points
    global high_score

    if high_score[-1] < points:
      high_score.append(points)

    screen.blit(background, (0,0))
    lives_display = main_font.render(f"Lives: {tommy_lives}", 1, (0,0,0))
    points_display = main_font.render(f"Points: {points}", 1, (0,0,0))
    high_score_display = main_font.render(f"High Score: {high_score[-1]}", 1, (0,0,0))
    screen.blit(lives_display, (10,10))
    screen.blit(points_display, (380,10))
    screen.blit(high_score_display, (10,470))
    pygame.display.update()

    screen.blit(tommy, (x,y))
    pygame.display.update()

    if len(blob_enemies) == 1:
      blob_enemies[0].input_key(key, 'none')
      blob_enemies[0].move()
      
      if x-20 < blob_enemies[0].blob_x < x+20 and y-20 < blob_enemies[0].blob_y < y+20:
        del blob_enemies[0]
        tommy_lives-=1
        points-=5


  game_start = False
  # Displays the start screen and executes the game when the space key is pressed.
  while game_start == False:
    screen.blit(start_screen, (0,0))
    pygame.display.update()
    for event in pygame.event.get():
      keys = pygame.key.get_pressed()
      if event.type == pygame.KEYDOWN:
        if keys[pygame.K_SPACE]:
          sleep(0.15)
          game_start = True


  # Main game loop that occurs when the game is running.
  running = True
  while running == True:

    clock.tick(60)

    # Quits the game.
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        running = False
        pygame.quit()
        sys.exit()

    # Displays the game over screen and restarts the game if the backspace button is pressed.
    if tommy_lives == 0:
     game_restart = True
     while game_restart == True:
      screen.blit(end_screen, (0,0))
      pygame.display.update()
      for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
          if keys[pygame.K_BACKSPACE]:
            sleep(0.15)
            game_restart = False
            tommy_lives = 5
        
    # Creates the enemy (blob).
    if len(blob_enemies) == 0:
      dream = Blob()
      blob_enemies.append(dream)

    # Calls the key detection function
    key = blob_enemies[0].letter_key
    blob_enemies[0].input_key(key, "detect")
    if blob_enemies[0].input_key(key, "detect") == True:
      points+=1
      del blob_enemies[0]
      print("y")

    redraw_window()
      
# Calls the main function that displays the entire game.    
main()