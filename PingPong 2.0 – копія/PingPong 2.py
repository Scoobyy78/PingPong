from pygame import *


  

# --- НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
mixer.init()

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Пінг-Понг")
clock = time.Clock()

# --- ЗОБРАЖЕННЯ ---
bg_image = image.load("game.png")
bg_image = transform.scale(bg_image, (WIDTH, HEIGHT))

menu_bg = image.load("menuu.jpg")
menu_bg = transform.scale(menu_bg, (WIDTH, HEIGHT))

ball_image = image.load("ball.png")
ball_image = transform.scale(ball_image, (20, 20))

paddle_image = image.load("raketa.png")
paddle_image = transform.scale(paddle_image, (50, 100))

# --- ШРИФТИ ---
font_main = font.Font(None, 36)
font_win = font.Font(None, 72)

# --- ЗВУКИ ---
hit_sound = mixer.Sound("hit.mp3")
win_sound = mixer.Sound("win.mp3")
mixer.music.load("fonm.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1) 

# --- ГРАВЦІ ---
paddle_width = 50
paddle_height = 100
paddle_speed = 6

left_paddle = Rect(20, HEIGHT//2 - 50, paddle_width, paddle_height)
right_paddle = Rect(WIDTH - 70, HEIGHT//2 - 50, paddle_width, paddle_height)

# --- МʼЯЧ ---
ball = Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
ball_speed_x = 5
ball_speed_y = 5

# --- РАХУНОК ---
score_left = 0
score_right = 0
game_over = False
game_state = "menu"

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x *= -1

# --- ГОЛОВНИЙ ЦИКЛ ---
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    keys = key.get_pressed()

    # ================= MENU =================
    if game_state == "menu":
        screen.blit(menu_bg, (0,0))


    title_text = font_win.render("PING PONG", True, (255,255,255))
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
    draw.rect(screen, (0, 0, 0), title_rect.inflate(20, 10)) 
    screen.blit(title_text, title_rect)


    button_rect = Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 60)
    draw.rect(screen, (0, 0, 0), button_rect)  
    draw.rect(screen, (255,255,255), button_rect, 4) 
    enter_text = font_main.render("Натисни ENTER", True, (255,255,255))
    screen.blit(enter_text, enter_text.get_rect(center=button_rect.center))

    keys = key.get_pressed()
    if keys[K_RETURN]:
        game_state = "play"

        display.update()
        clock.tick(60)
        continue  

    # ================= PLAY =================
    if game_state == "play":

        # --- КЕРУВАННЯ ---
        if keys[K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed

        if keys[K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        # --- РУХ МʼЯЧА ---
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Відбиття від стін
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Відбиття від ракеток
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1
            hit_sound.play()

        # Гол
        if ball.left <= 0:
            score_right += 1
            reset_ball()
        if ball.right >= WIDTH:
            score_left += 1
            reset_ball()

        # Перемога
        if score_left == 5 or score_right == 5:
            game_over = True
            game_state = "game_over"
            win_sound.play()





        # --- МАЛЮВАННЯ ---
        screen.blit(bg_image, (0,0))
        screen.blit(paddle_image, left_paddle)
        screen.blit(paddle_image, right_paddle)
        screen.blit(ball_image, ball)
        score_text = font_main.render(f"{score_left} : {score_right}", True, (255,255,255))
        screen.blit(score_text, (WIDTH//2 - 25, 20))

    # ================= GAME OVER =================
    if game_state == "game_over":
        screen.blit(bg_image, (0,0))
        if score_left > score_right:
            text = "Лівий гравець переміг!"
        else:
            text = "Правий гравець переміг!"

        win_text = font_win.render(text, True, (255,215,0))
        restart_text = font_main.render("R - Рестарт", True, (255,255,255))

        screen.blit(win_text, win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))

        if keys[K_r]:
            score_left = 0
            score_right = 0
            reset_ball()
            game_state = "menu"

    display.update()
    clock.tick(60)