import math
import random
import pygame
import time
import sys
from pygame import mixer
from time import sleep

pygame.init()

# Screen
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Invader")

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
#mixer.music.play()




# Spaceship
spaceship = pygame.image.load('spaceship.png')
spaceship_x = 370
spaceship_y = 480
spaceship_x_change = 0

# Enemy
alien = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alien.append(pygame.image.load('ufoo.png'))
    alien_x.append(random.randint(0, 736))
    alien_y.append(random.randint(50, 150))
    alien_x_change.append(4)
    alien_y_change.append(40)

# Bullet
missile = pygame.image.load('missile.png')
missile_x = 0
missile_y = 480
missile_x_change = 0
missile_y_change = 10
missile_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Funtions
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    screen.fill((0,0,55))
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def display_spaceship(x, y):
    screen.blit(spaceship, (x, y))


def display_alien(x, y, i):
    screen.blit(alien[i], (x, y))


def fire_goli(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile, (x + 16, y + 10))


def Takkar(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def main():
    display_spaceship(spaceship_x, spaceship_y)

    show_score(text_x, text_y)





# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                spaceship_x_change = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                spaceship_x_change = 5
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    
                    missile_x = spaceship_x
                    fire_goli(missile_x, missile_y)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                spaceship_x_change = 0

    
    # Boundary
    spaceship_x = spaceship_x + spaceship_x_change
    if spaceship_x <= 0:
        spaceship_x = 0
    elif spaceship_x >= 736:
        spaceship_x = 736

    # Enemy Movement
    for i in range(num_of_aliens):

        # Game Over
        if alien_y[i] > 440:
            for j in range(num_of_aliens):
                alien_y[j] = 2000
              
            game_over_text()
            '''sleep(5)
            pygame.quit()
            sys.exit()'''

            

        alien_x[i] += alien_x_change[i]
        if alien_x[i] <= 0:
            alien_x_change[i] = 3
            alien_y[i] += alien_y_change[i]
        elif alien_x[i] >= 736:
            alien_x_change[i] = -3
            alien_y[i] += alien_y_change[i]

        

        # Collision
        collision = Takkar(alien_x[i], alien_y[i], missile_x, missile_y)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            missile_y = 480
            missile_state = "ready"
            score_value += 1
            alien_x[i] = random.randint(0, 736)
            alien_y[i] = random.randint(50, 150)

        display_alien(alien_x[i], alien_y[i], i)

        # Difficulty
        if score_value >=5 and score_value <=10:
            
            if alien_x[i] <= 0:
                alien_x_change[i] = 4
                alien_y[i] += alien_y_change[i]

            elif alien_x[i] >= 736:
                alien_x_change[i] = -4
                alien_y[i] += alien_y_change[i]

        if score_value >=11 and score_value <=15:

            if alien_x[i] <= 0:
                alien_x_change[i] = 5
                alien_y[i] += alien_y_change[i]

            elif alien_x[i] >= 736:
                alien_x_change[i] = -5
                alien_y[i] += alien_y_change[i]

        if score_value >=16 and score_value <=20:

            if alien_x[i] <= 0:
                alien_x_change[i] = 5
                alien_y[i] += alien_y_change[i]

            elif alien_x[i] >= 736:
                alien_x_change[i] = -5
                alien_y[i] += alien_y_change[i]

        if score_value >=21:

            if alien_x[i] <= 0:
                alien_x_change[i] = 6
                alien_y[i] += alien_y_change[i]

            elif alien_x[i] >= 736:
                alien_x_change[i] = -6
                alien_y[i] += alien_y_change[i]

        
    # Bullet Movement
    if missile_y <= 0:
        missile_y = 480
        missile_state = "ready"

    if missile_state == "fire":
        fire_goli(missile_x, missile_y)
        missile_y -= missile_y_change

    main()
    
    pygame.display.update()
