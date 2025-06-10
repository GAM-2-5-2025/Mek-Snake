import pygame
import time
import random
import math

pygame.init()

snake_size = 40
window_x = 720
window_y = 480
margin = 40

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red   = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(241, 196, 15)

pause_image = pygame.image.load('pauza.png')
pause_image = pygame.transform.scale(pause_image, (30, 30))

game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('MEK-SNAKE')

background_start = pygame.image.load('mek.png')
background_start = pygame.transform.scale(background_start, (window_x, window_y))

background_game = pygame.image.load('zmija.png')
background_game = pygame.transform.scale(background_game, (window_x, window_y))

fps = pygame.time.Clock()
snake_speed = 6

head_img = pygame.transform.scale(pygame.image.load('head.jpg.png'), (snake_size, snake_size))
body_img = pygame.transform.scale(pygame.image.load('body.jpg.png'), (snake_size, snake_size))
tail_img = pygame.transform.scale(pygame.image.load('tail.jpg.png'), (snake_size, snake_size))

food_images = [
    pygame.transform.scale(pygame.image.load(img), (snake_size, snake_size))
    for img in ['pomfri.png', 'kola.png', 'sladoled.png', 'happymeal.png', 'hamburger.png', 'chickenbox.png']
]

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

def random_food_position():
    min_x = math.ceil(margin / snake_size) * snake_size
    max_x = math.floor((window_x - margin - snake_size) / snake_size) * snake_size
    min_y = math.ceil(margin / snake_size) * snake_size
    max_y = math.floor((window_y - margin - snake_size) / snake_size) * snake_size
    x = random.randrange(min_x, max_x + 1, snake_size)
    y = random.randrange(min_y, max_y + 1, snake_size)
    return [x, y]

def show_score(color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Bodovi : ' + str(score), True, color)
    score_rect = score_surface.get_rect(topleft=(margin, margin // 4))
    game_window.blit(score_surface, score_rect)

    pause_button_rect = pygame.Rect(window_x - margin - 30, margin // 4 - 5, 30, 30)
    game_window.blit(pause_image, pause_button_rect)

    return pause_button_rect

def start_screen():
    waiting = True
    start_button_rect = pygame.Rect(window_x // 2 - 75, window_y - 80, 150, 50)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    waiting = False

        game_window.blit(background_start, (0, 0))
        title_font = pygame.font.SysFont('times new roman', 50)
        title_surface = title_font.render('MEK-SNAKE', True, yellow)
        title_rect = title_surface.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(title_surface, title_rect)

        pygame.draw.rect(game_window, yellow, start_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        button_surface = button_font.render('POČETAK', True, black)
        button_rect = button_surface.get_rect(center=start_button_rect.center)
        game_window.blit(button_surface, button_rect)

        pygame.display.update()
        fps.tick(15)

def pause_screen():
    resume_button_rect = pygame.Rect(window_x // 2 - 75, window_y - 80, 150, 50)
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    paused = False

        game_window.blit(background_start, (0, 0))

        pause_font = pygame.font.SysFont('times new roman', 50)
        pause_text = pause_font.render('PAUZA', True, yellow)
        pause_rect = pause_text.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(pause_text, pause_rect)

        pygame.draw.rect(game_window, yellow, resume_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        resume_text = button_font.render('NASTAVI', True, black)
        resume_rect = resume_text.get_rect(center=resume_button_rect.center)
        game_window.blit(resume_text, resume_rect)

        pygame.display.update()
        fps.tick(15)

def game_over_screen(score):
    waiting = True
    kraj_button_rect = pygame.Rect(window_x // 2 - 150, window_y - 80, 120, 50)
    ponovi_button_rect = pygame.Rect(window_x // 2 + 30, window_y - 80, 120, 50)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if kraj_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                if ponovi_button_rect.collidepoint(event.pos):
                    waiting = False

        game_window.blit(background_start, (0, 0))

        game_over_font = pygame.font.SysFont('times new roman', 50)
        over_text = game_over_font.render('Postignuti broj bodova : ' + str(score), True, yellow)
        over_rect = over_text.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(over_text, over_rect)

        pygame.draw.rect(game_window, yellow, kraj_button_rect)
        pygame.draw.rect(game_window, yellow, ponovi_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        kraj_text = button_font.render('KRAJ', True, black)
        ponovi_text = button_font.render('PONOVI', True, black)
        game_window.blit(kraj_text, kraj_text.get_rect(center=kraj_button_rect.center))
        game_window.blit(ponovi_text, ponovi_text.get_rect(center=ponovi_button_rect.center))

        pygame.display.update()
        fps.tick(15)

def get_segment_angle(prev, curr):
    dx = curr[0] - prev[0]
    dy = curr[1] - prev[1]
    if dx > 0: return 0
    elif dx < 0: return 180
    elif dy > 0: return 270
    elif dy < 0: return 90
    return 0

def main_game():
    snake_position = [160, 40]
    snake_body = [[160, 40], [120, 40], [80, 40], [40, 40]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    food_position = random_food_position()
    food_spawn = True
    current_food_img = random.choice(food_images)
    pause_button_rect = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect and pause_button_rect.collidepoint(event.pos):
                    pause_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: change_to = 'UP'
                elif event.key == pygame.K_DOWN: change_to = 'DOWN'
                elif event.key == pygame.K_LEFT: change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT: change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'

        if direction == 'UP': snake_position[1] -= snake_size
        elif direction == 'DOWN': snake_position[1] += snake_size
        elif direction == 'LEFT': snake_position[0] -= snake_size
        elif direction == 'RIGHT': snake_position[0] += snake_size

        snake_body.insert(0, list(snake_position))
        if snake_position == food_position:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_position = random_food_position()
            current_food_img = random.choice(food_images)
            food_spawn = True

        game_window.blit(background_game, (0, 0))

        # Draw white walls on game screen only
        pygame.draw.rect(game_window, white, (0, 0, window_x, margin))
        pygame.draw.rect(game_window, white, (0, window_y - margin, window_x, margin))
        pygame.draw.rect(game_window, white, (0, margin, margin, window_y - 2 * margin))
        pygame.draw.rect(game_window, white, (window_x - margin, margin, margin, window_y - 2 * margin))

        for i in range(len(snake_body)):
            if i == 0:
                angle = get_segment_angle(snake_body[0], snake_body[1])
                img = rotate_image(head_img, angle)
            elif i == len(snake_body) - 1:
                angle = get_segment_angle(snake_body[i - 1], snake_body[i])
                img = rotate_image(tail_img, angle)
            else:
                angle = get_segment_angle(snake_body[i - 1], snake_body[i])
                img = rotate_image(body_img, angle)
            game_window.blit(img, pygame.Rect(snake_body[i][0], snake_body[i][1], snake_size, snake_size))

        game_window.blit(current_food_img, pygame.Rect(food_position[0], food_position[1], snake_size, snake_size))
import pygame
import time
import random
import math

pygame.init()

snake_size = 40
window_x = 720
window_y = 480
margin = 40

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red   = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(241, 196, 15)

pause_image = pygame.image.load('pauza.png')
pause_image = pygame.transform.scale(pause_image, (30, 30))

game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('MEK-SNAKE')

background_start = pygame.image.load('mek.png')
background_start = pygame.transform.scale(background_start, (window_x, window_y))

background_game = pygame.image.load('zmija.png')
background_game = pygame.transform.scale(background_game, (window_x, window_y))

fps = pygame.time.Clock()
snake_speed = 7.5

head_img = pygame.transform.scale(pygame.image.load('head.jpg.png'), (snake_size, snake_size))
body_img = pygame.transform.scale(pygame.image.load('body.jpg.png'), (snake_size, snake_size))
tail_img = pygame.transform.scale(pygame.image.load('tail.jpg.png'), (snake_size, snake_size))

food_images = [
    pygame.transform.scale(pygame.image.load(img), (snake_size, snake_size))
    for img in ['pomfri.png', 'kola.png', 'sladoled.png', 'happymeal.png', 'hamburger.png', 'chickenbox.png']
]

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

def random_food_position():
    min_x = math.ceil(margin / snake_size) * snake_size
    max_x = math.floor((window_x - margin - snake_size) / snake_size) * snake_size
    min_y = math.ceil(margin / snake_size) * snake_size
    max_y = math.floor((window_y - margin - snake_size) / snake_size) * snake_size
    x = random.randrange(min_x, max_x + 1, snake_size)
    y = random.randrange(min_y, max_y + 1, snake_size)
    return [x, y]

def show_score(color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Bodovi : ' + str(score), True, color)
    score_rect = score_surface.get_rect(topleft=(margin, margin // 4))
    game_window.blit(score_surface, score_rect)

    pause_button_rect = pygame.Rect(window_x - margin - 30, margin // 4 - 5, 30, 30)
    game_window.blit(pause_image, pause_button_rect)

    return pause_button_rect

def start_screen():
    waiting = True
    start_button_rect = pygame.Rect(window_x // 2 - 75, window_y - 80, 150, 50)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    waiting = False

        game_window.blit(background_start, (0, 0))
        title_font = pygame.font.SysFont('times new roman', 50)
        title_surface = title_font.render('MEK-SNAKE', True, yellow)
        title_rect = title_surface.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(title_surface, title_rect)

        pygame.draw.rect(game_window, yellow, start_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        button_surface = button_font.render('POČETAK', True, black)
        button_rect = button_surface.get_rect(center=start_button_rect.center)
        game_window.blit(button_surface, button_rect)

        pygame.display.update()
        fps.tick(15)

def pause_screen():
    resume_button_rect = pygame.Rect(window_x // 2 - 75, window_y - 80, 150, 50)
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    paused = False

        game_window.blit(background_start, (0, 0))

        pause_font = pygame.font.SysFont('times new roman', 50)
        pause_text = pause_font.render('PAUZA', True, yellow)
        pause_rect = pause_text.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(pause_text, pause_rect)

        pygame.draw.rect(game_window, yellow, resume_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        resume_text = button_font.render('NASTAVI', True, black)
        resume_rect = resume_text.get_rect(center=resume_button_rect.center)
        game_window.blit(resume_text, resume_rect)

        pygame.display.update()
        fps.tick(15)

def game_over_screen(score):
    waiting = True
    kraj_button_rect = pygame.Rect(window_x // 2 - 150, window_y - 80, 120, 50)
    ponovi_button_rect = pygame.Rect(window_x // 2 + 30, window_y - 80, 120, 50)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if kraj_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                if ponovi_button_rect.collidepoint(event.pos):
                    waiting = False

        game_window.blit(background_start, (0, 0))

        game_over_font = pygame.font.SysFont('times new roman', 50)
        over_text = game_over_font.render('Postignuti broj bodova : ' + str(score), True, yellow)
        over_rect = over_text.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(over_text, over_rect)

        pygame.draw.rect(game_window, yellow, kraj_button_rect)
        pygame.draw.rect(game_window, yellow, ponovi_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        kraj_text = button_font.render('KRAJ', True, black)
        ponovi_text = button_font.render('PONOVI', True, black)
        game_window.blit(kraj_text, kraj_text.get_rect(center=kraj_button_rect.center))
        game_window.blit(ponovi_text, ponovi_text.get_rect(center=ponovi_button_rect.center))

        pygame.display.update()
        fps.tick(15)

def get_segment_angle(prev, curr):
    dx = curr[0] - prev[0]
    dy = curr[1] - prev[1]
    if dx > 0: return 0
    elif dx < 0: return 180
    elif dy > 0: return 270
    elif dy < 0: return 90
    return 0

def main_game():
    snake_position = [160, 40]
    snake_body = [[160, 40], [120, 40], [80, 40], [40, 40]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    food_position = random_food_position()
    food_spawn = True
    current_food_img = random.choice(food_images)
    pause_button_rect = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect and pause_button_rect.collidepoint(event.pos):
                    pause_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: change_to = 'UP'
                elif event.key == pygame.K_DOWN: change_to = 'DOWN'
                elif event.key == pygame.K_LEFT: change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT: change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'

        if direction == 'UP': snake_position[1] -= snake_size
        elif direction == 'DOWN': snake_position[1] += snake_size
        elif direction == 'LEFT': snake_position[0] -= snake_size
        elif direction == 'RIGHT': snake_position[0] += snake_size

        snake_body.insert(0, list(snake_position))
        if snake_position == food_position:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_position = random_food_position()
            current_food_img = random.choice(food_images)
            food_spawn = True

        game_window.blit(background_game, (0, 0))

        for i in range(len(snake_body)):
            if i == 0:
                angle = get_segment_angle(snake_body[0], snake_body[1])
                img = rotate_image(head_img, angle)
            elif i == len(snake_body) - 1:
                angle = get_segment_angle(snake_body[i - 1], snake_body[i])
                img = rotate_image(tail_img, angle)
            else:
                angle = get_segment_angle(snake_body[i - 1], snake_body[i])
                img = rotate_image(body_img, angle)
            game_window.blit(img, pygame.Rect(snake_body[i][0], snake_body[i][1], snake_size, snake_size))

        game_window.blit(current_food_img, pygame.Rect(food_position[0], food_position[1], snake_size, snake_size))
import pygame
import time
import random
import math

pygame.init()

snake_size = 40
window_x = 720
window_y = 480
margin = 40

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red   = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(241, 196, 15)

pause_image = pygame.image.load('pauza.png')
pause_image = pygame.transform.scale(pause_image, (30, 30))

game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('MEK-SNAKE')

background_start = pygame.image.load('mek.png')
background_start = pygame.transform.scale(background_start, (window_x, window_y))

background_game = pygame.image.load('zmija.png')
background_game = pygame.transform.scale(background_game, (window_x, window_y))

fps = pygame.time.Clock()
snake_speed = 7.5

head_img = pygame.transform.scale(pygame.image.load('head.jpg.png'), (snake_size, snake_size))
body_img = pygame.transform.scale(pygame.image.load('body.jpg.png'), (snake_size, snake_size))
tail_img = pygame.transform.scale(pygame.image.load('tail.jpg.png'), (snake_size, snake_size))

food_images = [
    pygame.transform.scale(pygame.image.load(img), (snake_size, snake_size))
    for img in ['pomfri.png', 'kola.png', 'sladoled.png', 'happymeal.png', 'hamburger.png', 'chickenbox.png']
]

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

def random_food_position():
    min_x = math.ceil(margin / snake_size) * snake_size
    max_x = math.floor((window_x - margin - snake_size) / snake_size) * snake_size
    min_y = math.ceil(margin / snake_size) * snake_size
    max_y = math.floor((window_y - margin - snake_size) / snake_size) * snake_size
    x = random.randrange(min_x, max_x + 1, snake_size)
    y = random.randrange(min_y, max_y + 1, snake_size)
    return [x, y]

def show_score(color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Bodovi : ' + str(score), True, color)
    score_rect = score_surface.get_rect(topleft=(margin, margin // 4))

    background_rect_score = pygame.Rect(score_rect.left - 5, score_rect.top - 2, score_rect.width + 10, score_rect.height + 4)
    pygame.draw.rect(game_window, white, background_rect_score)

    game_window.blit(score_surface, score_rect)

    pause_button_rect = pygame.Rect(window_x - margin - 30, margin // 4 - 5, 30, 30)

    background_rect_pause = pygame.Rect(pause_button_rect.left - 2, pause_button_rect.top - 2, pause_button_rect.width + 4, pause_button_rect.height + 4)
    pygame.draw.rect(game_window, white, background_rect_pause)

    game_window.blit(pause_image, pause_button_rect)

    return pause_button_rect


def start_screen():
    waiting = True
    start_button_rect = pygame.Rect(window_x // 2 - 75, window_y - 80, 150, 50)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    waiting = False

        game_window.blit(background_start, (0, 0))
        title_font = pygame.font.SysFont('times new roman', 50)
        title_surface = title_font.render('MEK-SNAKE', True, yellow)
        title_rect = title_surface.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(title_surface, title_rect)

        pygame.draw.rect(game_window, yellow, start_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        button_surface = button_font.render('POČETAK', True, black)
        button_rect = button_surface.get_rect(center=start_button_rect.center)
        game_window.blit(button_surface, button_rect)

        pygame.display.update()
        fps.tick(15)

def pause_screen():
    resume_button_rect = pygame.Rect(window_x // 2 - 75, window_y - 80, 150, 50)
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    paused = False

        game_window.blit(background_start, (0, 0))

        pause_font = pygame.font.SysFont('times new roman', 50)
        pause_text = pause_font.render('PAUZA', True, yellow)
        pause_rect = pause_text.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(pause_text, pause_rect)

        pygame.draw.rect(game_window, yellow, resume_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        resume_text = button_font.render('NASTAVI', True, black)
        resume_rect = resume_text.get_rect(center=resume_button_rect.center)
        game_window.blit(resume_text, resume_rect)

        pygame.display.update()
        fps.tick(15)

def game_over_screen(score):
    waiting = True
    kraj_button_rect = pygame.Rect(window_x // 2 - 150, window_y - 80, 120, 50)
    ponovi_button_rect = pygame.Rect(window_x // 2 + 30, window_y - 80, 120, 50)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if kraj_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                if ponovi_button_rect.collidepoint(event.pos):
                    waiting = False

        game_window.blit(background_start, (0, 0))

        game_over_font = pygame.font.SysFont('times new roman', 50)
        over_text = game_over_font.render('Postignuti broj bodova : ' + str(score), True, yellow)
        over_rect = over_text.get_rect(midtop=(window_x // 2, 20))
        game_window.blit(over_text, over_rect)

        pygame.draw.rect(game_window, yellow, kraj_button_rect)
        pygame.draw.rect(game_window, yellow, ponovi_button_rect)
        button_font = pygame.font.SysFont('times new roman', 30)
        kraj_text = button_font.render('KRAJ', True, black)
        ponovi_text = button_font.render('PONOVI', True, black)
        game_window.blit(kraj_text, kraj_text.get_rect(center=kraj_button_rect.center))
        game_window.blit(ponovi_text, ponovi_text.get_rect(center=ponovi_button_rect.center))

        pygame.display.update()
        fps.tick(15)

def get_segment_angle(prev, curr):
    dx = curr[0] - prev[0]
    dy = curr[1] - prev[1]
    if dx > 0: return 0
    elif dx < 0: return 180
    elif dy > 0: return 270
    elif dy < 0: return 90
    return 0

def main_game():
    snake_position = [160, 40]
    snake_body = [[160, 40], [120, 40], [80, 40], [40, 40]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    food_position = random_food_position()
    food_spawn = True
    current_food_img = random.choice(food_images)
    pause_button_rect = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect and pause_button_rect.collidepoint(event.pos):
                    pause_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: change_to = 'UP'
                elif event.key == pygame.K_DOWN: change_to = 'DOWN'
                elif event.key == pygame.K_LEFT: change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT: change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'

        if direction == 'UP': snake_position[1] -= snake_size
        elif direction == 'DOWN': snake_position[1] += snake_size
        elif direction == 'LEFT': snake_position[0] -= snake_size
        elif direction == 'RIGHT': snake_position[0] += snake_size

        snake_body.insert(0, list(snake_position))
        if snake_position == food_position:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            while True:
                food_position = random_food_position()
                if food_position not in snake_body:
                    break
            current_food_img = random.choice(food_images)
            food_spawn = True


        game_window.blit(background_game, (0, 0))
        green_color = (30, 132, 73)
        pygame.draw.rect(game_window, green_color, pygame.Rect(0, 0, margin, window_y)) 
        pygame.draw.rect(game_window, green_color, pygame.Rect(window_x - margin, 0, margin, window_y)) 
        pygame.draw.rect(game_window, green_color, pygame.Rect(0, 0, window_x, margin)) 
        pygame.draw.rect(game_window, green_color, pygame.Rect(0, window_y - margin, window_x, margin)) 


        for i in range(len(snake_body)):
            if i == 0:
                angle = get_segment_angle(snake_body[0], snake_body[1])
                img = rotate_image(head_img, angle)
            elif i == len(snake_body) - 1:
                angle = get_segment_angle(snake_body[i - 1], snake_body[i])
                img = rotate_image(tail_img, angle)
            else:
                angle = get_segment_angle(snake_body[i - 1], snake_body[i])
                img = rotate_image(body_img, angle)
            game_window.blit(img, pygame.Rect(snake_body[i][0], snake_body[i][1], snake_size, snake_size))

        game_window.blit(current_food_img, pygame.Rect(food_position[0], food_position[1], snake_size, snake_size))

        pause_button_rect = show_score(black, 'times new roman', 20, score)

        if (snake_position[0] < margin or snake_position[0] > window_x - margin - snake_size or
            snake_position[1] < margin or snake_position[1] > window_y - margin - snake_size):
            running = False

        for block in snake_body[1:]:
            if snake_position == block:
                running = False

        pygame.display.update()
        fps.tick(snake_speed)

    return score

def main():
    start_screen()
    while True:
        score = main_game()
        game_over_screen(score)

if __name__ == '__main__':
    main()


