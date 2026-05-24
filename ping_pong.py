import pygame
import random

pygame.init()

WIDTH = 1300
HEIGHT = 780
FPS = 60

WIN_SCORE = 3
GAME_TIME = 300

BG = (245, 236, 220)
PANEL = (228, 213, 190)
TEXT = (72, 58, 48)

BALL_COLOR = (120, 92, 72)

PLAYER_COLOR = (145, 118, 96)
AI_COLOR = (110, 92, 82)

PUFF_COLOR = (210, 190, 165)
MID_COLOR = (200, 180, 160)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cream Ping Pong")

clock = pygame.time.Clock()

font_small = pygame.font.SysFont("georgia", 28)
font_medium = pygame.font.SysFont("georgia", 42)
font_big = pygame.font.SysFont("georgia", 70)

player = pygame.Rect(60, HEIGHT // 2 - 70, 18, 140)

enemy = pygame.Rect(
    WIDTH - 78,
    HEIGHT // 2 - 70,
    18,
    140
)

ball = pygame.Rect(
    WIDTH // 2,
    HEIGHT // 2,
    22,
    22
)

ball_x = float(ball.x)
ball_y = float(ball.y)

ball_speed_x = random.choice([-5, 5])
ball_speed_y = random.choice([-4, 4])

top_puff = pygame.Rect(
    WIDTH // 2 - 70,
    120,
    140,
    28
)

bottom_puff = pygame.Rect(
    WIDTH // 2 - 70,
    HEIGHT - 120,
    140,
    28
)

left_mid = pygame.Rect(
    WIDTH // 2 - 320,
    HEIGHT // 2 - 90,
    22,
    180
)

right_mid = pygame.Rect(
    WIDTH // 2 + 298,
    HEIGHT // 2 - 90,
    22,
    180
)

player_score = 0
enemy_score = 0

start_ticks = pygame.time.get_ticks()


def reset_ball():
    global ball_x
    global ball_y
    global ball_speed_x
    global ball_speed_y

    ball.center = (WIDTH // 2, HEIGHT // 2)

    ball_x = float(ball.x)
    ball_y = float(ball.y)

    ball_speed_x = random.choice([-5, 5])
    ball_speed_y = random.choice([-4, -3, 3, 4])


def draw_background():
    screen.fill(BG)

    pygame.draw.rect(
        screen,
        PANEL,
        (0, 0, WIDTH, 90)
    )

    for y in range(110, HEIGHT, 40):
        pygame.draw.rect(
            screen,
            (220, 205, 185),
            (WIDTH // 2 - 4, y, 8, 22),
            border_radius=4
        )


def draw_ui(time_left):
    score = font_medium.render(
        str(player_score) + " : " + str(enemy_score),
        1,
        TEXT
    )

    screen.blit(
        score,
        (WIDTH // 2 - score.get_width() // 2, 20)
    )

    m = time_left // 60
    s = time_left % 60

    timer_text = str(m).zfill(2) + ":" + str(s).zfill(2)

    timer = font_small.render(
        timer_text,
        1,
        TEXT
    )

    screen.blit(
        timer,
        (WIDTH // 2 - timer.get_width() // 2, 62)
    )


def draw_objects():
    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        player,
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        AI_COLOR,
        enemy,
        border_radius=18
    )

    pygame.draw.ellipse(
        screen,
        BALL_COLOR,
        ball
    )

    pygame.draw.rect(
        screen,
        PUFF_COLOR,
        top_puff,
        border_radius=16
    )

    pygame.draw.rect(
        screen,
        PUFF_COLOR,
        bottom_puff,
        border_radius=16
    )

    pygame.draw.rect(
        screen,
        MID_COLOR,
        left_mid,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        MID_COLOR,
        right_mid,
        border_radius=10
    )


def bounce_from_rect(rect):
    global ball_speed_x
    global ball_speed_y

    overlap_left = ball.right - rect.left
    overlap_right = rect.right - ball.left
    overlap_top = ball.bottom - rect.top
    overlap_bottom = rect.bottom - ball.top

    smallest = min(
        overlap_left,
        overlap_right,
        overlap_top,
        overlap_bottom
    )

    if smallest == overlap_left:
        ball.right = rect.left
        ball_speed_x *= -1

    elif smallest == overlap_right:
        ball.left = rect.right
        ball_speed_x *= -1

    elif smallest == overlap_top:
        ball.bottom = rect.top
        ball_speed_y *= -1

    else:
        ball.top = rect.bottom
        ball_speed_y *= -1


def ai_move():
    target = ball.centery - enemy.centery

    if abs(target) < 18:
        return

    if pygame.time.get_ticks() % 2 != 0:
        return

    if target > 0:
        enemy.y += 5
    else:
        enemy.y -= 5

    enemy.top = max(enemy.top, 100)
    enemy.bottom = min(enemy.bottom, HEIGHT)


def move_ball():
    global ball_x
    global ball_y
    global ball_speed_x
    global ball_speed_y
    global player_score
    global enemy_score

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    ball.x = int(ball_x)
    ball.y = int(ball_y)

    if ball.top <= 95:
        ball.top = 95
        ball_speed_y *= -1

    if ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT
        ball_speed_y *= -1

    if ball.colliderect(player):
        ball.left = player.right

        ball_x = ball.x

        ball_speed_x *= -1

        ball_speed_y += (
            ball.centery - player.centery
        ) / 20

    if ball.colliderect(enemy):
        ball.right = enemy.left

        ball_x = ball.x

        ball_speed_x *= -1

        ball_speed_y += (
            ball.centery - enemy.centery
        ) / 20

    if ball.colliderect(top_puff):
        bounce_from_rect(top_puff)
        ball_speed_y *= 1.1

    if ball.colliderect(bottom_puff):
        bounce_from_rect(bottom_puff)
        ball_speed_y *= 1.1

    if ball.colliderect(left_mid):
        bounce_from_rect(left_mid)

    if ball.colliderect(right_mid):
        bounce_from_rect(right_mid)

    ball_speed_x = max(min(ball_speed_x, 8), -8)
    ball_speed_y = max(min(ball_speed_y, 7), -7)

    if ball.left <= 0:
        enemy_score += 1
        reset_ball()

    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()


def show_end(text, color):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill(BG)

    screen.blit(overlay, (0, 0))

    title = font_big.render(
        text,
        1,
        color
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            HEIGHT // 2 - 40
        )
    )

    pygame.display.flip()

    wait = True

    while wait:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        clock.tick(FPS)


running = True

while running:
    clock.tick(FPS)

    time_left = max(
        0,
        GAME_TIME - (
            pygame.time.get_ticks() - start_ticks
        ) // 1000
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= 8

    if keys[pygame.K_s]:
        player.y += 8

    if keys[pygame.K_UP]:
        player.y -= 8

    if keys[pygame.K_DOWN]:
        player.y += 8

    player.top = max(player.top, 100)
    player.bottom = min(player.bottom, HEIGHT)

    ai_move()

    move_ball()

    if player_score >= WIN_SCORE:
        show_end(
            "ПОБЕДА",
            (110, 150, 110)
        )

    if enemy_score >= WIN_SCORE:
        show_end(
            "ПОРАЖЕНИЕ",
            (170, 90, 90)
        )

    if time_left <= 0:
        if player_score > enemy_score:
            show_end(
                "ВРЕМЯ ВЫШЛО — ПОБЕДА",
                (110, 150, 110)
            )
        elif enemy_score > player_score:
            show_end(
                "ВРЕМЯ ВЫШЛО — ПОРАЖЕНИЕ",
                (170, 90, 90)
            )
        else:
            show_end(
                "НИЧЬЯ",
                TEXT
            )

    draw_background()

    draw_objects()

    draw_ui(time_left)

    pygame.display.flip()

pygame.quit()