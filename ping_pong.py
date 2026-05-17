# ping_pong.py
# Cream Pastel Ping Pong on Pygame (updated)

import pygame
import random

pygame.init()

# =========================
# ЭКРАН (увеличен)
# =========================
WIDTH, HEIGHT = 1300, 780
FPS = 60

WIN_SCORE = 3
GAME_TIME = 5 * 60

# =========================
# ЦВЕТА
# =========================
BG = (245, 236, 220)
PANEL = (228, 213, 190)
TEXT = (72, 58, 48)

BALL_COLOR = (120, 92, 72)
PLAYER_COLOR = (145, 118, 96)
AI_COLOR = (110, 92, 82)

PUFF_COLOR = (210, 190, 165)
PUFF_OUTLINE = (160, 130, 105)

CENTER_LINE = (220, 205, 185)

WIN_COLOR = (110, 150, 110)
LOSE_COLOR = (170, 90, 90)

# =========================
# ИНИЦИАЛИЗАЦИЯ
# =========================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cream Ping Pong")

clock = pygame.time.Clock()

font_small = pygame.font.SysFont("georgia", 28)
font_medium = pygame.font.SysFont("georgia", 42)
font_big = pygame.font.SysFont("georgia", 74)

# =========================
# ОБЪЕКТЫ
# =========================
PADDLE_WIDTH = 18
PADDLE_HEIGHT = 140
PADDLE_SPEED = 8

BALL_SIZE = 22

player = pygame.Rect(60, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                     PADDLE_WIDTH, PADDLE_HEIGHT)

enemy = pygame.Rect(WIDTH - 60 - PADDLE_WIDTH,
                    HEIGHT // 2 - PADDLE_HEIGHT // 2,
                    PADDLE_WIDTH, PADDLE_HEIGHT)

ball = pygame.Rect(WIDTH // 2, HEIGHT // 2,
                   BALL_SIZE, BALL_SIZE)

# Пуфики (верх/низ)
PUFF_W = 140
PUFF_H = 28

top_puff = pygame.Rect(WIDTH // 2 - PUFF_W // 2, 120,
                       PUFF_W, PUFF_H)

bottom_puff = pygame.Rect(WIDTH // 2 - PUFF_W // 2,
                          HEIGHT - 120,
                          PUFF_W, PUFF_H)

# =========================
# НОВЫЕ ПРЕПЯТСТВИЯ (центр слева/справа)
# =========================
MID_W = 22
MID_H = 180

left_mid = pygame.Rect(WIDTH // 2 - 320,
                       HEIGHT // 2 - MID_H // 2,
                       MID_W, MID_H)

right_mid = pygame.Rect(WIDTH // 2 + 320,
                        HEIGHT // 2 - MID_H // 2,
                        MID_W, MID_H)

# =========================
# СКОРОСТЬ (–20%)
# =========================
SPEED_MULT = 0.8

ball_speed_x = random.choice((-6, 6)) * SPEED_MULT
ball_speed_y = random.choice((-5, 5)) * SPEED_MULT


def reset_ball():
    global ball_speed_x, ball_speed_y

    ball.center = (WIDTH // 2, HEIGHT // 2)

    direction = random.choice([-1, 1])

    ball_speed_x = direction * random.randint(5, 7) * SPEED_MULT
    ball_speed_y = random.choice([-5, -4, 4, 5]) * SPEED_MULT


# =========================
# СЧЁТ
# =========================
player_score = 0
enemy_score = 0

start_ticks = pygame.time.get_ticks()

def show_end_screen(text, color):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((245, 236, 220))

    screen.blit(overlay, (0, 0))

    title = font_big.render(text, True, color)
    hint = font_small.render('Нажмите ESC для выхода', True, TEXT)

    screen.blit(title,
                (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
    
    screen.blit(hint,
                (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))
    
    pygame.display.flip()

    waiting = True

    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        
        clock.tick(FPS)

# =========================
# ОТРИСОВКА ФОНА
# =========================
def draw_background():
    screen.fill(BG)

    pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, 90))

    for y in range(110, HEIGHT, 40):
        pygame.draw.rect(screen, CENTER_LINE,
                         (WIDTH // 2 - 4, y, 8, 22))


def draw_paddle(rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=18)


def draw_ball():
    pygame.draw.ellipse(screen, BALL_COLOR, ball)


def draw_puff(rect):
    pygame.draw.rect(screen, PUFF_COLOR, rect, border_radius=18)


def draw_mid(rect):
    pygame.draw.rect(screen, (200, 180, 160), rect, border_radius=10)


def draw_ui(time_left):
    score = font_medium.render(f"{player_score} : {enemy_score}",
                               True, TEXT)
    screen.blit(score, (WIDTH // 2 - score.get_width() // 2, 22))

    m = time_left // 60
    s = time_left % 60

    timer = font_small.render(f"{m:02}:{s:02}", True, TEXT)
    screen.blit(timer, (WIDTH // 2 - timer.get_width() // 2, 65))


# =========================
# ИИ
# =========================
def ai_move():
    target = ball.centery - enemy.centery
    enemy.y += 6 if target > 0 else -6

def check_win():
    global running

    if player_score >= WIN_SCORE:
        running = False
        show_end_screen('ПОБЕДА', WIN_COLOR)
    
    if enemy_score >= WIN_SCORE:
        running = False
        show_end_screen('ПОРАЖЕНИЕ', LOSE_COLOR)

# =========================
# МЯЧ
# =========================
def move_ball():
    global ball_speed_x, ball_speed_y
    global player_score, enemy_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # стены
    if ball.top <= 95 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # ракетки
    if ball.colliderect(player):
        ball.left = player.right
        ball_speed_x *= -1
        ball_speed_y += (ball.centery - player.centery) / 20

    if ball.colliderect(enemy):
        ball.right = enemy.left
        ball_speed_x *= -1
        ball_speed_y += (ball.centery - enemy.centery) / 20

    # пуфики
    if ball.colliderect(top_puff):
        ball.bottom = top_puff.top
        ball_speed_y *= -1.2

    if ball.colliderect(bottom_puff):
        ball.top = bottom_puff.bottom
        ball_speed_y *= -1.2

    # новые препятствия
    if ball.colliderect(left_mid):
        ball.left = left_mid.right
        ball_speed_x *= -1

    if ball.colliderect(right_mid):
        ball.right = right_mid.left
        ball_speed_x *= -1

    # ограничение скорости (–20%)
    ball_speed_x = max(min(ball_speed_x, 11.2), -11.2)
    ball_speed_y = max(min(ball_speed_y, 9.6), -9.6)

    # голы
    if ball.left <= 0:
        enemy_score += 1
        reset_ball()

    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()


# =========================
# ЦИКЛ
# =========================
running = True

while running:
    clock.tick(FPS)

    time_left = max(0, GAME_TIME - (pygame.time.get_ticks() - start_ticks) // 1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.y += PADDLE_SPEED

    player.top = max(player.top, 100)
    player.bottom = min(player.bottom, HEIGHT)

    ai_move()
    move_ball()
    check_win()

    draw_background()

    draw_paddle(player, PLAYER_COLOR)
    draw_paddle(enemy, AI_COLOR)

    draw_ball()

    draw_puff(top_puff)
    draw_puff(bottom_puff)

    draw_mid(left_mid)
    draw_mid(right_mid)

    draw_ui(time_left)

    pygame.display.flip()

pygame.quit()