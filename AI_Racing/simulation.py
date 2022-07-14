import pygame
import Globals
import pycar
from game_utils import scaling_Images, set_back_flags
from enum import Enum
import numpy as np

# Game initialization
pygame.init()
font = pygame.font.Font("freesansbold.ttf", 32)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    FORWARD = 3


# Images
TRACK_IMG = scaling_Images(pygame.image.load("Images/pista2.png"), 0.9)
FINISH_IMG = scaling_Images(pygame.image.load("Images/finish_line.png"), 0.9)
FINISH_IMG = pygame.transform.rotate(FINISH_IMG, 90)
TRACK_IMG_PUNISHMENT_ONE = scaling_Images(pygame.image.load("Images/Bestrafungen.png"), 0.9)
TRACK_IMG_PUNISHMENT_TWO = scaling_Images(pygame.image.load("Images/Bestrafung2.png"), 0.9)
STRIPE_IMG_ONE = scaling_Images(pygame.image.load("Images/finish_line.png"), 0.9)
STRIPE_IMG_ONE = pygame.transform.scale(STRIPE_IMG_ONE, (87, 2))
STRIPE_IMG_ONE = pygame.transform.rotate(STRIPE_IMG_ONE, 90)
STRIPE_IMG_TWO = STRIPE_IMG_ONE
STRIPE_IMG_THREE = STRIPE_IMG_ONE
STRIPE_IMG_FOUR = STRIPE_IMG_ONE
STRIPE_IMG_FIVE = pygame.transform.rotate(STRIPE_IMG_ONE, 90)
STRIPE_IMG_SIX = STRIPE_IMG_FIVE
STRIPE_IMG_SEVEN = STRIPE_IMG_FIVE

# Masks
TRACK_MASK_ONE = pygame.mask.from_surface(TRACK_IMG_PUNISHMENT_ONE)
TRACK_MASK_TWO = pygame.mask.from_surface(TRACK_IMG_PUNISHMENT_TWO)
FINISH_MASK = pygame.mask.from_surface(FINISH_IMG)
STRIPE_IMG_MASK_ONE = pygame.mask.from_surface(STRIPE_IMG_ONE)
STRIPE_IMG_MASK_TWO = pygame.mask.from_surface(STRIPE_IMG_TWO)
STRIPE_IMG_MASK_THREE = pygame.mask.from_surface(STRIPE_IMG_THREE)
STRIPE_IMG_MASK_FOUR = pygame.mask.from_surface(STRIPE_IMG_FOUR)
STRIPE_IMG_MASK_FIVE = pygame.mask.from_surface(STRIPE_IMG_FIVE)
STRIPE_IMG_MASK_SIX = pygame.mask.from_surface(STRIPE_IMG_SIX)
STRIPE_IMG_MASK_SEVEN = pygame.mask.from_surface(STRIPE_IMG_SEVEN)

class AI_CAR:
    player1 = pycar.Car(1.8,3)

    def __init__(self):
        self.width = TRACK_IMG.get_width()
        self.height = TRACK_IMG.get_height()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Car")
        self.direction = Direction.FORWARD
        self.clock = pygame.time.Clock()
        self.score = Globals.score_value
        self.fps = Globals.GAME_FPS
        self.episode = 1
        self.flag_episode = False

    def check_which_stripe(self):
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
            return Globals.FINISH_POSITION

    def outside_of_road_detection(self, Point):
        try:
            if TRACK_MASK_ONE.get_at(Point):
                return True
        except IndexError:
            return True
        try:
            if TRACK_MASK_TWO.get_at((Point)):
                return True
        except IndexError:
            return True
        return False

    def new_episode(self):
        display_new_episode = font.render("New episode starts!", True, Globals.WHITE)
        Globals.frame_iteration = 0
        set_back_flags()
        self.player1.x, self.player1.y = self.player1.START_POS
        self.display.blit(TRACK_IMG, (0, 0))
        self.display.blit(FINISH_IMG, Globals.FINISH_POSITION)
        score = font.render("Score: " + str(Globals.score_value), True, Globals.WHITE)
        self.display.blit(score, (Globals.text_pos_X, Globals.text_pos_Y))
        score = font.render("Timer: " + str(Globals.countdown_value), True, Globals.WHITE)
        self.display.blit(score, (Globals.timer_pos_X, Globals.timer_pos_Y))
        score = font.render("Rounds: " + str(Globals.count_Rounds) + "/10", True, Globals.WHITE)
        self.display.blit(score, (400, 30))
        self.display.blit(STRIPE_IMG_ONE, Globals.STRIPE_ONE)
        self.display.blit(STRIPE_IMG_TWO, Globals.STRIPE_TWO)
        self.display.blit(STRIPE_IMG_THREE, Globals.STRIPE_THREE)
        self.display.blit(STRIPE_IMG_FOUR, Globals.STRIPE_FOUR)
        self.display.blit(STRIPE_IMG_FIVE, Globals.STRIPE_FIVE)
        self.display.blit(STRIPE_IMG_SIX, Globals.STRIPE_SIX)
        self.display.blit(STRIPE_IMG_SEVEN, Globals.STRIPE_SEVEN)
        self.display.blit(display_new_episode, (300, 300))
        Globals.score_value -= 4
        self.episode += 1
        self.player1.angle = 90
        Globals.Flags_round = 0
        pygame.display.update()
        Globals.countdown_value = 90
        pygame.time.delay(1500)
        Globals.score_value = 0
        Globals.SETBACK = False

    def check_flags(self):
        if self.player1.collide(STRIPE_IMG_MASK_ONE, *Globals.STRIPE_ONE) != None and Globals.STRIPE_FLAG_ONE:
            print("detected First Mask!")
            Globals.STRIPE_FLAG_ONE = False
            Globals.Flags_round+=1
            Globals.score_value += 1
        if self.player1.collide(STRIPE_IMG_MASK_TWO, *Globals.STRIPE_TWO) != None and Globals.STRIPE_FLAG_TWO:
            print("detected Second Mask!")
            Globals.STRIPE_FLAG_TWO = False
            Globals.Flags_round += 1
            Globals.score_value += 1
        if self.player1.collide(STRIPE_IMG_MASK_THREE, *Globals.STRIPE_THREE) != None and Globals.STRIPE_FLAG_THREE:
            print("detected Third Mask!")
            Globals.STRIPE_FLAG_THREE = False
            Globals.Flags_round += 1
            Globals.score_value += 1
        if self.player1.collide(STRIPE_IMG_MASK_FOUR, *Globals.STRIPE_FOUR) != None and Globals.STRIPE_FLAG_FOUR:
            print("detected Fourth Mask!")
            Globals.STRIPE_FLAG_FOUR = False
            Globals.Flags_round += 1
            Globals.score_value += 1
        if self.player1.collide(STRIPE_IMG_MASK_FIVE, *Globals.STRIPE_FIVE) != None and Globals.STRIPE_FLAG_FIVE:
            print("detected Fifth Mask!")
            Globals.STRIPE_FLAG_FIVE = False
            Globals.Flags_round += 1
            Globals.score_value += 1
        if self.player1.collide(STRIPE_IMG_MASK_SIX, *Globals.STRIPE_SIX) != None and Globals.STRIPE_FLAG_SIX:
            print("detected sixth Mask!")
            Globals.STRIPE_FLAG_SIX = False
            Globals.Flags_round += 1
            Globals.score_value+=1
        if self.player1.collide(STRIPE_IMG_MASK_SEVEN, *Globals.STRIPE_SEVEN) != None and Globals.STRIPE_FLAG_SEVEN:
            print("detected seventh Mask!")
            Globals.STRIPE_FLAG_SEVEN = False
            Globals.Flags_round += 1
            Globals.score_value+=1
    def end_game(self):
        display_new_episode = font.render("Goal achieved, Congratulations!", True, Globals.WHITE)
        self.display.blit(display_new_episode, (230, 300))
        pygame.display.update()
        pygame.time.delay(6000)
        pygame.quit()

    def collision_mask_one(self):
        if self.player1.collide(TRACK_MASK_ONE) != None:
            Globals.punish_score+=1
            if(Globals.punish_score==45):
                Globals.score_value-=1
                Globals.punish_score=0
                Globals.Punish_collision_detection-=1

    def collision_mask_two(self):
        if self.player1.collide(TRACK_MASK_TWO) != None:
            Globals.punish_score+=1
            if(Globals.punish_score==50):
                Globals.score_value-=1
                Globals.punish_score=0
                Globals.Punish_collision_detection-=1

    def reach_finishLine(self):
        if self.player1.collide(FINISH_MASK, *Globals.FINISH_POSITION) != None and Globals.Flags_round == 7:
            Globals.countdown_value = 90
            Globals.FINISH = True
            Globals.Flags_round = 0
            set_back_flags()
            Globals.Intermediate_target = 0
            if Globals.count_Rounds == 2:
                self.end_game()

    def simulation_step(self, action):
        Globals.frame_iteration+=1

        # 1. collect user input
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            moved = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.check_move(action)
        reward = 0
        if Globals.flag_episode == True:
            reward -=10 # return reward, globals.flag episode in agent und zurücksetzen des flags danach!
            return reward, Globals.flag_episode, self.score

        if Globals.compare_Rounds_for_reward < Globals.count_Rounds:
            reward+=10
            Globals.compare_Rounds_for_reward+=1
        if Globals.compare_punish_collision_detection > Globals.Punish_collision_detection:
            reward-=3
            Globals.Punish_collision_detection = 0
        if Globals.Intermediate_target < Globals.Flags_round:
            reward+=2
            Globals.Intermediate_target+=1
        self.update_ui()
        self.clock.tick(self.fps)
        return reward, self.flag_episode, self.score

    def update_ui(self):
        self.display.blit(TRACK_IMG, (0,0))
        self.display.blit(FINISH_IMG, Globals.FINISH_POSITION)
        score = font.render("Score: " + str(Globals.score_value), True, Globals.WHITE)
        self.display.blit(score, (Globals.text_pos_X, Globals.text_pos_Y))
        score = font.render("Timer: " + str(Globals.countdown_value), True, Globals.WHITE)
        self.display.blit(score, (Globals.timer_pos_X, Globals.timer_pos_Y))
        score = font.render("Rounds: " + str(Globals.count_Rounds)+"/10", True, Globals.WHITE)
        self.display.blit(score, (400, 30))
        self.display.blit(STRIPE_IMG_ONE, Globals.STRIPE_ONE)
        self.display.blit(STRIPE_IMG_TWO, Globals.STRIPE_TWO)
        self.display.blit(STRIPE_IMG_THREE, Globals.STRIPE_THREE)
        self.display.blit(STRIPE_IMG_FOUR, Globals.STRIPE_FOUR)
        self.display.blit(STRIPE_IMG_FIVE, Globals.STRIPE_FIVE)
        self.display.blit(STRIPE_IMG_SIX, Globals.STRIPE_SIX)
        self.display.blit(STRIPE_IMG_SEVEN, Globals.STRIPE_SEVEN)
        self.player1.draw(self.display)

        Globals.Seconds+=1
        if Globals.Seconds == 40:
            Globals.countdown_value-=1
            Globals.Seconds = 0

        self.collision_mask_one()
        self.collision_mask_two()
        self.reach_finishLine()
        self.check_flags()

        if Globals.FINISH:
            Globals.delay_count_round+=1
            if Globals.delay_count_round == 50:
                Globals.FINISH = False
                Globals.score_value+=6
                Globals.count_Rounds+=1
                Globals.delay_count_round = 0

        if Globals.countdown_value == 0 or Globals.SETBACK:
            Globals.flag_episode = True

        pygame.display.update()

    def check_move(self, action):
        agent_direction = [Direction.FORWARD, Direction.RIGHT, Direction.LEFT]
        index = agent_direction.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = agent_direction[index]
        elif np.array_equal(action, [0,1,0]):
            next_idx = (index +1) % 3
            new_dir = agent_direction[next_idx]
        else:
            next_idx = (index - 1) % 3
            new_dir = agent_direction[next_idx]

        self.direction = new_dir

        if self.direction == Direction.LEFT:
            self.player1.rotate(left=True)
        elif self.direction == Direction.RIGHT:
            self.player1.rotate(right=True)
        elif self.direction == Direction.FORWARD:
            moved = True
            self.player1.move_forward()









