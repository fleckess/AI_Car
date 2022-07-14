import pygame
import Globals
pygame.init() # brauche ich um Schriftarten nutzen zu können
WHITE = (255,255,255)
font = pygame.font.Font("freesansbold.ttf", 32)

def scaling_Images(img_Name, scale_factor):
    WIDTH, HEIGHT = round(img_Name.get_width() * scale_factor), round(img_Name.get_height() * scale_factor)
    return pygame.transform.scale(img_Name, (WIDTH,HEIGHT))

def blit_rotate_center(display, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    display.blit(rotated_image, new_rect.topleft)

def showScore(x,y,score_value, DISPLAY):
    score = font.render("Score: "+ str(score_value), True,WHITE)
    DISPLAY.blit(score, (x, y))
def showCountDown(x,y,countdown_value, DISPLAY):
    score = font.render("Timer: "+ str(countdown_value), True,WHITE)
    DISPLAY.blit(score, (x, y))
def showRounds(x,y, count_Rounds, DISPLAY):
    score = font.render("Rounds: " + str(count_Rounds), True, WHITE)
    DISPLAY.blit(score, (x, y))

def set_back_flags():
    Globals.STRIPE_FLAG_ONE = True
    Globals.STRIPE_FLAG_TWO = True
    Globals.STRIPE_FLAG_THREE = True
    Globals.STRIPE_FLAG_FOUR = True
    Globals.STRIPE_FLAG_FIVE = True
    Globals.STRIPE_FLAG_SIX = True
    Globals.STRIPE_FLAG_SEVEN = True

def check_which_stripe():
    if Globals.Flags_round == 0:
        return Globals.STRIPE_ONE
    if Globals.Flags_round == 1:
        return Globals.STRIPE_TWO
    if Globals.Flags_round == 2:
        return Globals.STRIPE_THREE
    if Globals.Flags_round == 3:
        return Globals.STRIPE_FOUR
    if Globals.Flags_round == 4:
        return Globals.STRIPE_FIVE
    if Globals.Flags_round == 5:
        return Globals.STRIPE_SIX
    if Globals.Flags_round == 6:
        return Globals.STRIPE_SEVEN
    else:
        return (0,0)