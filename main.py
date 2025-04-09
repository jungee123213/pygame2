import sys
import time
import pygame
import random
pygame.init()
pygame.display.set_caption("핑퐁")

WIDTH,HEIGHT=600,800
screen=pygame.display.set_mode((WIDTH,HEIGHT))
#c#
WHITE=(255,255,255)
ICE=(110,197,255)
BLACK=(0,0,0)

clock = pygame.time.Clock()

class Paddle:
    def __init__(self,x,y):
        self.init_x = x
        self.rect=pygame.Rect(x,y,80,15)
        self.speed=5
        self.is_skill_iced_usable = True
        self.is_skill_iced_used = False
        self.record_speed_y = 0
        self.record_speed_x = 0
        self.start_time = 0

    def go_to_start_position(self):
        self.rect.x = self.init_x

    def skill_iced(self, key):
        keys = pygame.key.get_pressed()
        if self.is_skill_iced_usable == True and self.is_skill_iced_used == False and keys[key]:
            self.start_time = pygame.time.get_ticks()
            self.is_skill_iced_used = True
            self.is_skill_iced_usable = False


        if self.is_skill_iced_used == True:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= 3000:
                self.is_skill_iced_used = False
                self.start_time = pygame.time.get_ticks()

        if self.is_skill_iced_used == False and self.is_skill_iced_usable == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= 7000:
                self.is_skill_iced_usable = True

    def move(self,up_key,down_key):
        keys=pygame.key.get_pressed()
        if keys[up_key]:
            self.rect.x -= self.speed
        if keys[down_key]:
            self.rect.x += self.speed
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
    def draw(self,screen):
        pygame.draw.rect(screen,WHITE,self.rect)



class Ball:
    def __init__(self):
        self.rect=pygame.Rect(WIDTH//2-15,HEIGHT//2-15,30,30)
        self.speed_x=0
        start_way = random.randint(0,1)
        if start_way == 0:
            self.speed_y = 8
        else:
            self.speed_y = -8

    def move(self):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x

    def draw(self,screen, is_iced):
        color = WHITE
        if is_iced:
            color = ICE
        pygame.draw.ellipse(screen,color,self.rect)


def game():
    paddle1=Paddle(WIDTH-350,HEIGHT//2+375)
    paddle2=Paddle(WIDTH-350,HEIGHT//2-375)
    ball=Ball()

    isStart = True
    score1 = 0
    score2 = 0
    font = pygame.font.SysFont("Arial", 32)
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        paddle1.move(pygame.K_a,pygame.K_d)
        paddle2.move(pygame.K_LEFT , pygame.K_RIGHT)
        paddle1.skill_iced(pygame.K_UP)
        paddle2.skill_iced(pygame.K_w)
        paddle1.draw(screen)
        paddle2.draw(screen)

        if not (paddle1.is_skill_iced_used or paddle2.is_skill_iced_used):
            ball.move()
        if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
            ball.speed_y = -ball.speed_y
            ball.speed_x = random.randint(-10,10)
        if ball.rect.top <= 0:
            score2 +=1
            ball = Ball()
            paddle1.go_to_start_position()
            paddle2.go_to_start_position()
        if ball.rect.bottom >= HEIGHT:
            score1 +=1
            ball = Ball()
            paddle1.go_to_start_position()
            paddle2.go_to_start_position()

        score_text = font.render(f"{score1}-{score2}", True,WHITE)
        screen.blit(score_text,(WIDTH // 2 - score_text.get_width() // 0.16, 375))

        skill_text = font.render(f"*", True, WHITE)

        if paddle1.is_skill_iced_usable == True:
            screen.blit(skill_text, (WIDTH // 2 - score_text.get_width() // 0.16, 335))
        if paddle2.is_skill_iced_usable == True:
            screen.blit(skill_text, (WIDTH // 2 - score_text.get_width() // 0.16, 425))
        ball.draw(screen, paddle1.is_skill_iced_used or paddle2.is_skill_iced_used)
        pygame.display.flip()
        clock.tick(60)
        if isStart == True:
            time.sleep(2)
            isStart = False


def start():
    title_font = pygame.font.SysFont("Arial", 60)
    choice_font = pygame.font.SysFont("Arial", 20)
    now_button = 0

    before_keys = pygame.key.get_pressed()
    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # if before_keys[pygame.K_UP] == False and keys[pygame.K_UP] == True:
        #     now_button -= 1
        #     if now_button == -1:
        #         now_button = 0
        #
        #
        # if before_keys[pygame.K_DOWN] == False and keys[pygame.K_DOWN] == True:
        #     now_button += 1
        #     if now_button == 3:
        #         now_button = 2


        if before_keys[pygame.K_SPACE] == False and keys[pygame.K_SPACE] == True:
            if now_button == 0:
                game()

        title = title_font.render("Amazing Pingpong",True,WHITE)
        screen.blit(title,(WIDTH // 2 - title.get_width() // 2, 100))
        pointer = ""
        if now_button == 0:
            pointer = ">"
        start_button = choice_font.render(pointer+"Game Start",True,WHITE)
        screen.blit(start_button,(WIDTH //  2 - start_button.get_width() // 2, 480))
        # pointer = ""
        # if now_button ==1:
        #     pointer = ">"
        # p1_skill_room_button = choice_font.render(pointer+"Player1 Skill", True, WHITE)
        # screen.blit(p1_skill_room_button, (WIDTH // 2 - p1_skill_room_button.get_width() // 2, 500))
        # pointer = ""
        # if now_button == 2:
        #     pointer = ">"
        # p2_skill_room_button = choice_font.render(pointer+"Player2 Skill", True,WHITE)
        # screen.blit(p2_skill_room_button, (WIDTH // 2 - p2_skill_room_button.get_width() // 2, 520))

        before_keys = keys
        pygame.display.flip()
        clock.tick(60)

start()