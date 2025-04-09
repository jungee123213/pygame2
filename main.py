import sys
import time
import pygame
import random

pygame.init()
pygame.display.set_caption("핑퐁")

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
ICE = (110, 197, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

font_large = pygame.font.SysFont("Arial", 60)
font_small = pygame.font.SysFont("Arial", 32)

mode = "start"
space_pressed_last = False
isStart = True
start_time = 0

class Paddle:
    def __init__(self, x, y):
        self.init_x = x
        self.rect = pygame.Rect(x, y, 80, 15)
        self.speed = 5
        self.is_skill_iced_usable = True
        self.is_skill_iced_used = False
        self.start_time = 0

    def go_to_start_position(self):
        self.rect.x = self.init_x

    def skill_iced(self, key):
        keys = pygame.key.get_pressed()
        if self.is_skill_iced_usable and not self.is_skill_iced_used and keys[key]:
            self.start_time = pygame.time.get_ticks()
            self.is_skill_iced_used = True
            self.is_skill_iced_usable = False

        if self.is_skill_iced_used:
            if pygame.time.get_ticks() - self.start_time >= 3000:
                self.is_skill_iced_used = False
                self.start_time = pygame.time.get_ticks()

        if not self.is_skill_iced_used and not self.is_skill_iced_usable:
            if pygame.time.get_ticks() - self.start_time >= 7000:
                self.is_skill_iced_usable = True

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key]:
            self.rect.x -= self.speed
        if keys[down_key]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.speed_x = 0
        self.speed_y = 8 if random.randint(0, 1) == 0 else -8

    def move(self):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x

    def draw(self, screen, is_iced):
        color = ICE if is_iced else WHITE
        pygame.draw.ellipse(screen, color, self.rect)

# 게임 객체 초기화
paddle1 = Paddle(WIDTH - 350, HEIGHT // 2 + 375)
paddle2 = Paddle(WIDTH - 350, HEIGHT // 2 - 375)
ball = Ball()
score1 = 0
score2 = 0

# 단일 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # SPACE 누르면 시작
    if mode == "start":
        if keys[pygame.K_SPACE] and not space_pressed_last:
            mode = "game"
            isStart = True
            start_time = pygame.time.get_ticks()
    space_pressed_last = keys[pygame.K_SPACE]

    screen.fill(BLACK)

    if mode == "start":
        title = font_large.render("Amazing Pingpong", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        start_button = font_small.render("> Game Start", True, WHITE)
        screen.blit(start_button, (WIDTH // 2 - start_button.get_width() // 2, 480))

    elif mode == "game":
        paddle1.move(pygame.K_a, pygame.K_d)
        paddle2.move(pygame.K_LEFT, pygame.K_RIGHT)
        paddle1.skill_iced(pygame.K_UP)
        paddle2.skill_iced(pygame.K_w)
        paddle1.draw(screen)
        paddle2.draw(screen)

        if not (paddle1.is_skill_iced_used or paddle2.is_skill_iced_used):
            if not isStart or pygame.time.get_ticks() - start_time > 2000:
                ball.move()
                isStart = False

        if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
            ball.speed_y = -ball.speed_y
            ball.speed_x = random.randint(-10, 10)

        if ball.rect.top <= 0:
            score2 += 1
            ball = Ball()
            paddle1.go_to_start_position()
            paddle2.go_to_start_position()
            isStart = True
            start_time = pygame.time.get_ticks()

        if ball.rect.bottom >= HEIGHT:
            score1 += 1
            ball = Ball()
            paddle1.go_to_start_position()
            paddle2.go_to_start_position()
            isStart = True
            start_time = pygame.time.get_ticks()

        # 점수, 스킬 UI (색상을 WHITE로 수정)
        score_text = font_small.render(f"{score1}-{score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 375))

        skill_text = font_small.render(" ", True, WHITE)
        if paddle1.is_skill_iced_usable:
            screen.blit(skill_text, (WIDTH // 2 - 10, 335))
        if paddle2.is_skill_iced_usable:
            screen.blit(skill_text, (WIDTH // 2 - 10, 425))

        ball.draw(screen, paddle1.is_skill_iced_used or paddle2.is_skill_iced_used)

    pygame.display.flip()
    clock.tick(60)
