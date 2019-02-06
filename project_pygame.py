import pygame
import os
import sys
import random
import copy
pygame.init()
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))

clock = pygame.time.Clock()
running = True
STEP = 10
FPS = 100
tile_width = tile_height = 50

points = 0

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()

def start_new():
    with open("data/" + 'current_level.txt', 'r') as cur:
        level = cur.read()
    with open('data/' + 'current_lifes.txt', 'r') as l:
        lifes = l.read()
    with open('data/' + 'current_money.txt', 'r') as m:
        money = m.read()
    screen.fill((255, 255, 255))
    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    play = Play()
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 90)
    text_coord = 50
    pygame.draw.ellipse(screen, (255, 0, 0), (150, 300, 650, 200),)
    string_rendered = font.render('Уровень ' + str(level), 1,
                                  pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    text_coord = 360
    intro_rect.top = text_coord
    intro_rect.x = 330
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    heart = pygame.sprite.Sprite(all_sprites, heart_group)
    heart.image = heart_image
    heart.rect = heart.image.get_rect()
    heart.rect.x = 170
    heart.rect.y = 50
    string_rendered = font.render(str(lifes), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = 65
    intro_rect.top = text_coord
    intro_rect.x = 90
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    moneta = pygame.sprite.Sprite(all_sprites, moneta_group)
    moneta.image = moneta_image
    moneta.rect = moneta.image.get_rect()
    moneta.rect.x = 800
    moneta.rect.y = 50
    string_rendered = font.render(str(money), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = 70
    intro_rect.top = text_coord
    intro_rect.x = 740 - len(money) * 20
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    heart_group.draw(screen)
    play_group.draw(screen)
    moneta_group.draw(screen)
    pygame.display.flip()
    heart_group.remove(heart)
    moneta_group.remove(moneta)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                b = play.get_event(event)
                if b:
                    game()
                    play_group.remove(play)
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def game():
    global points
    screen.fill((255, 255, 255))
    with open('data/' + 'current_money.txt', 'r') as m:
        money = m.read()
    with open('data/' + 'current_lifes.txt', 'r') as l:
        lifes = l.read()
    with open("data/" + 'current_level.txt', 'r') as cur:
        level = cur.read()
    loaded_level, moves, goals = load_level()
    level_x, level_y = generate_level(loaded_level)
    font = pygame.font.Font(None, 90)
    font2 = pygame.font.Font(None, 60)
    text_coord = 50

    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    heart = pygame.sprite.Sprite(all_sprites, heart_group)
    heart.image = heart_image
    heart.rect = heart.image.get_rect()
    heart.rect.x = 100
    heart.rect.y = 20
    string_rendered = font.render(str(lifes), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = 30
    intro_rect.top = text_coord
    intro_rect.x = 50
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    moneta = pygame.sprite.Sprite(all_sprites, moneta_group)
    moneta.image = moneta_image
    moneta.rect = moneta.image.get_rect()
    moneta.rect.x = 600
    moneta.rect.y = 20
    string_rendered = font.render(str(money), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = 30
    intro_rect.top = text_coord
    intro_rect.x = 540 - len(money) * 20
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    string_rendered = font2.render('Уровень ' + str(level), 1,
                                  pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    text_coord = 100
    intro_rect.top = text_coord
    intro_rect.x = 720
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    string_rendered = font2.render('Ходы: ' + str(moves), 1,
                                  pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    text_coord = 150
    intro_rect.top = text_coord
    intro_rect.x = 720
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    string_rendered = font2.render('Цели: ', 1,
                                  pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    text_coord = 200
    intro_rect.top = text_coord
    intro_rect.x = 720
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    string_rendered = font2.render(str(points), 1,
                                  pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    text_coord = 200
    intro_rect.top = text_coord
    intro_rect.x = 200
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    for i in range(len(goals)):
        string_rendered = font2.render(str(goals[i].split()[0]), 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 300 + 100 * i
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        goal = pygame.sprite.Sprite(all_sprites, goal_group)
        goal.image = load_image(tile_images[int(goals[i].split()[1])])
        goal.rect = heart.image.get_rect()
        goal.rect.x = intro_rect.x + 70
        goal.rect.y = text_coord - 60

    heart_group.draw(screen)
    moneta_group.draw(screen)
    goal_group.draw(screen)
    tiles_group.draw(screen)
    pygame.display.flip()
    loaded_level = [list(i) for i in loaded_level]
    first = True

    while moves != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for _ in tiles_group:
                    if _.get_event(event)[0]:
                        if first:
                            x1, y1 = _.get_event(event)[1], _.get_event(event)[2]
                            if loaded_level[int(y1)][int(x1)] != '':
                                _.image = load_image(lightning_tile_images[int(loaded_level[int(y1)][int(x1)])])
                                last = _
                                first = False
                                break
                        else:
                            x2, y2 = _.get_event(event)[1], _.get_event(event)[2]
                            if (x1, y1) == (x2, y2):
                                if loaded_level[int(y1)][int(x1)] != '' and (
                                    loaded_level[int(y2)][int(x2)] != ''):
                                    _.image = load_image(tile_images[int(loaded_level[int(y1)][int(x1)])])
                                    last.image = load_image(tile_images[int(loaded_level[int(y2)][int(x2)])])
                                first = True
                            elif (x1 + 1 == x2 and y1 == y2) or (
                                x1 - 1 == x2 and y1 == y2) or (
                                    x1 == x2 and y1 + 1 == y2) or (
                                        x1 == x2 and y1 - 1 == y2):
                                if loaded_level[int(y1)][int(x1)] != '' and (
                                    loaded_level[int(y2)][int(x2)] != ''):
                                    _.image = load_image(tile_images[int(loaded_level[int(y2)][int(x2)])])
                                    last.image = load_image(tile_images[int(loaded_level[int(y1)][int(x1)])])
                                    new_loaded_level = change((x1, y1), (x2, y2),
                                                          loaded_level, _, last,
                                                          moves, goals)
                                    loaded_level = copy.deepcopy(new_loaded_level)
                                    while is_there_a_combination(loaded_level):
                                        loaded_level, goals = destruction(loaded_level, goals)
                                        tiles_group.empty()
                                        generate_level(loaded_level)
                                        loaded_level = falling(loaded_level, moves, goals)
                                    if loaded_level != new_loaded_level:
                                        moves = str(int(moves) - 1)
                                    tiles_group.empty()
                                    generate_level(loaded_level)
                                    if loaded_level[int(y1)][int(x1)] != '' and (loaded_level[int(y2)][int(x2)] != ''):
                                        _.image = load_image(tile_images[int(loaded_level[int(y2)][int(x2)])])
                                        last.image = load_image(tile_images[int(loaded_level[int(y1)][int(x1)])])
                                    last = _
                                    first = True
                            else:
                                if loaded_level[int(y1)][int(x1)] != '' and (loaded_level[int(y2)][int(x2)] != ''):
                                    last.image = load_image(tile_images[int(loaded_level[int(y1)][int(x1)])])
                                    x1, y1 = _.get_event(event)[1], _.get_event(event)[2]
                                    _.image = load_image(lightning_tile_images[int(loaded_level[int(y1)][int(x1)])])
                                    last = _
                                    first = False
                            break



        screen.fill((255, 255, 255))
        screen.blit(fon, (0, 0))
        string_rendered = font.render(str(lifes), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = 30
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render(str(money), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = 30
        intro_rect.top = text_coord
        intro_rect.x = 540 - len(money) * 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font2.render('Уровень ' + str(level), 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 100
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        string_rendered = font2.render('Ходы: ' + str(moves), 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 150
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        string_rendered = font2.render('Цели: ', 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 200
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        done_group.empty()
        for i in range(len(goals)):
            if goals[i].split()[0] != '0':
                string_rendered = font2.render(str(goals[i].split()[0]), 1,
                                              pygame.Color('yellow'))
                intro_rect = string_rendered.get_rect()
                text_coord = 300 + 100 * i
                intro_rect.top = text_coord
                intro_rect.x = 720
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            else:
                done = pygame.sprite.Sprite(all_sprites, done_group)
                done.image = load_image('done.png')
                done.rect = done.image.get_rect()
                done.rect.x = 720
                done.rect.y = 290 + 100 * i
        string_rendered = font.render(str(points), 1,
                                  pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 30
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        heart_group.draw(screen)
        moneta_group.draw(screen)
        goal_group.draw(screen)
        tiles_group.draw(screen)
        done_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def change(first, second, loaded_level, cur, last, moves, goals):
    #print('i am in change')
    with open('data/' + 'current_money.txt', 'r') as m:
        money = m.read()
    with open('data/' + 'current_lifes.txt', 'r') as l:
        lifes = l.read()
    with open("data/" + 'current_level.txt', 'r') as current:
        level = current.read()
    font = pygame.font.Font(None, 90)
    font2 = pygame.font.Font(None, 60)
    text_coord = 50
    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    x1, y1 = first[0], first[1]
    x2, y2 = second[0], second[1]
    pr_coords = (cur.rect)
    moving = True
    while moving:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if x2 > x1:
            screen.fill((255, 255, 255))
            cur.rect = cur.rect.move(-1, 0)
            last.rect = last.rect.move(1, 0)
        elif x2 < x1:
            cur.rect = cur.rect.move(1, 0)
            last.rect = last.rect.move(-1, 0)
        if y2 > y1:
            cur.rect = cur.rect.move(0, -1)
            last.rect = last.rect.move(0, 1)
        elif y2 < y1:
            cur.rect = cur.rect.move(0, 1)
            last.rect = last.rect.move(0, -1)
        if loaded_level[int(y1)][int(x1)] != '' and (
            loaded_level[int(y2)][int(x2)] != ''):
            cur.image = load_image(tile_images[int(loaded_level[int(y2)][int(x2)])])
            last.image = load_image(tile_images[int(loaded_level[int(y1)][int(x1)])])
        screen.fill((255, 255, 255))
        screen.blit(fon, (0, 0))
        string_rendered = font.render(str(lifes), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = 30
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render(str(money), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = 30
        intro_rect.top = text_coord
        intro_rect.x = 540 - len(money) * 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font2.render('Уровень ' + str(level), 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 100
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        string_rendered = font2.render('Ходы: ' + str(moves), 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 150
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        string_rendered = font2.render('Цели: ', 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 200
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        done_group.empty()
        for i in range(len(goals)):
            if goals[i].split()[0] != '0':
                string_rendered = font2.render(str(goals[i].split()[0]), 1,
                                              pygame.Color('yellow'))
                intro_rect = string_rendered.get_rect()
                text_coord = 300 + 100 * i
                intro_rect.top = text_coord
                intro_rect.x = 720
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            else:
                done = pygame.sprite.Sprite(all_sprites, done_group)
                done.image = load_image('done.png')
                done.rect = done.image.get_rect()
                done.rect.x = 720
                done.rect.y = 290 + 100 * i
        string_rendered = font.render(str(points), 1,
                                  pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 30
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        heart_group.draw(screen)
        moneta_group.draw(screen)
        goal_group.draw(screen)
        tiles_group.draw(screen)
        done_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        if pr_coords == (last.rect):
            moving = False
    temp_level = copy.deepcopy(loaded_level)
    k = temp_level[y1][x1]
    m = loaded_level[y2][x2]
    temp_level[y1][x1] = m
    temp_level[y2][x2] = k
    if is_there_a_combination(temp_level):
        return temp_level
    else:
        pr_coords = (cur.rect)
        moving = True
        while moving:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            if x2 > x1:
                screen.fill((255, 255, 255))
                cur.rect = cur.rect.move(1, 0)
                last.rect = last.rect.move(-1, 0)
            elif x2 < x1:
                cur.rect = cur.rect.move(-1, 0)
                last.rect = last.rect.move(1, 0)
            if y2 > y1:
                cur.rect = cur.rect.move(0, 1)
                last.rect = last.rect.move(0, -1)
            elif y2 < y1:
                cur.rect = cur.rect.move(0, -1)
                last.rect = last.rect.move(0, 1)
            screen.fill((255, 255, 255))
            screen.blit(fon, (0, 0))
            string_rendered = font.render(str(lifes), 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord = 30
            intro_rect.top = text_coord
            intro_rect.x = 50
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            string_rendered = font.render(str(money), 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord = 30
            intro_rect.top = text_coord
            intro_rect.x = 540 - len(money) * 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            string_rendered = font2.render('Уровень ' + str(level), 1,
                                          pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 100
            intro_rect.top = text_coord
            intro_rect.x = 720
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

            string_rendered = font2.render('Ходы: ' + str(moves), 1,
                                          pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 150
            intro_rect.top = text_coord
            intro_rect.x = 720
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

            string_rendered = font2.render('Цели: ', 1,
                                          pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 200
            intro_rect.top = text_coord
            intro_rect.x = 720
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            for i in range(len(goals)):
                string_rendered = font2.render(str(goals[i].split()[0]), 1,
                                              pygame.Color('yellow'))
                intro_rect = string_rendered.get_rect()
                text_coord = 300 + 100 * i
                intro_rect.top = text_coord
                intro_rect.x = 720
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            string_rendered = font.render(str(points), 1,
                                  pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 30
            intro_rect.top = text_coord
            intro_rect.x = 250
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            heart_group.draw(screen)
            moneta_group.draw(screen)
            goal_group.draw(screen)
            tiles_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            if pr_coords == (last.rect):
                moving = False
        return loaded_level


def is_there_a_combination(level):
    #print('i am in is_there_a_combination')
    horizontal = [''.join(i) for i in level]
    vertical = []
    for i in range(len(level[0])):
        stroka = ''
        for j in range(len(level)):
            stroka += level[j][i]
        vertical.append(stroka)
    for i in range(9):
        for j in horizontal:
            if i != '':
                if str(i) * 3 in j:
                    return True
    for i in range(9):
        for j in vertical:
            if i != '':
                if str(i) * 3 in j:
                    return True
    return False


def destruction(level, goals):
    global points
    if is_there_a_combination(level):
        all_combo = []
        for i in range(len(level)):
            for j in range(len(level[0])):
                fruit = level[i][j]
                kolvo = 1
                if fruit != '':
                    h = check_seq(level, i, j, 0)
                    v = check_seq(level, i, j, 1)
                    if h > 2:
                        for _ in range(h):
                            if (i, j + _) not in all_combo:
                                all_combo.append((i, j + _))
                    if v > 2:
                        for _ in range(v):
                            if (i + _, j) not in all_combo:
                                all_combo.append((i + _, j))
        for _ in all_combo:
            for i in range(len(goals)):
                if goals[i].split()[1] == level[_[0]][_[1]] and goals[i].split()[0] != '0':
                    goals[i] = str(int(goals[i].split()[0]) - 1) +  ' ' + goals[i].split()[1]
            level[_[0]][_[1]] = ''
        points += len(all_combo) * 100
        return level, goals
    else:
        return level, goals


def check_seq(level, i, j, d = 0, k = 1):
    #print('i am in check_seq')
    if d == 0:
        if j < len(level[i]) - 1 and level[i][j] == level[i][j + 1]:
            k += 1
            k = check_seq(level, i, j + 1, d, k)
    elif d == 1:
        if i < len(level) - 1 and level[i][j] == level[i + 1][j]:
            k += 1
            k = check_seq(level, i + 1, j, d, k)
    return k


def falling(loaded_level, moves, goals):
    with open('data/' + 'current_money.txt', 'r') as m:
        money = m.read()
    with open('data/' + 'current_lifes.txt', 'r') as l:
        lifes = l.read()
    with open("data/" + 'current_level.txt', 'r') as current:
        level = current.read()
    font = pygame.font.Font(None, 90)
    font2 = pygame.font.Font(None, 60)
    text_coord = 50
    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    moving = True
    sprites_for_moving = []
    while moving:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        for i in range(len(loaded_level)):
            for j in range(len(loaded_level[0])):
                if i != len(loaded_level) - 1:
                    if loaded_level[i + 1][j] == '' and loaded_level[i][j] != '':
                        for _ in tiles_group:
                            if _.rect.x == tile_width * j + 50 and (
                                _.rect.y == tile_height * i + 120) and (
                                    _.image != empty_image):
                                if _ not in sprites_for_moving:
                                    sprites_for_moving.append([_, i + 1, j])
                    elif i == 0 and loaded_level[i][j] == '':
                        loaded_level[i][j] = str(random.randint(0, 7))
                        tiles_group.empty()
                        generate_level(loaded_level)
        while True:
            for i in sprites_for_moving:
                i[0].rect = i[0].rect.move(0, 5)
                if i[0].rect.y == tile_height * i[1] + 120:
                    sprites_for_moving.remove(i)
                    loaded_level[i[1]][i[2]] = loaded_level[i[1] - 1][i[2]]
                    loaded_level[i[1] - 1][i[2]] = ''
            screen.fill((255, 255, 255))
            screen.blit(fon, (0, 0))
            string_rendered = font.render(str(lifes), 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord = 30
            intro_rect.top = text_coord
            intro_rect.x = 50
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            string_rendered = font.render(str(money), 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord = 30
            intro_rect.top = text_coord
            intro_rect.x = 540 - len(money) * 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            string_rendered = font2.render('Уровень ' + str(level), 1,
                                          pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 100
            intro_rect.top = text_coord
            intro_rect.x = 720
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

            string_rendered = font2.render('Ходы: ' + str(moves), 1,
                                          pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 150
            intro_rect.top = text_coord
            intro_rect.x = 720
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

            string_rendered = font2.render('Цели: ', 1,
                                          pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 200
            intro_rect.top = text_coord
            intro_rect.x = 720
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            done_group.empty()
            for i in range(len(goals)):
                if goals[i].split()[0] != '0':
                    string_rendered = font2.render(str(goals[i].split()[0]), 1,
                                                  pygame.Color('yellow'))
                    intro_rect = string_rendered.get_rect()
                    text_coord = 300 + 100 * i
                    intro_rect.top = text_coord
                    intro_rect.x = 720
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
                else:
                    done = pygame.sprite.Sprite(all_sprites, done_group)
                    done.image = load_image('done.png')
                    done.rect = done.image.get_rect()
                    done.rect.x = 720
                    done.rect.y = 290 + 100 * i
            string_rendered = font.render(str(points), 1,
                                      pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 30
            intro_rect.top = text_coord
            intro_rect.x = 250
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            heart_group.draw(screen)
            moneta_group.draw(screen)
            goal_group.draw(screen)
            tiles_group.draw(screen)
            done_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            if len(sprites_for_moving) == 0:
                break
        kolvo = 0
        for i in range(len(loaded_level)):
            for j in range(len(loaded_level[0])):
                if loaded_level[i][j] == '':
                    kolvo += 1
        if kolvo == 0:
            moving = False
    return loaded_level

def start_screen():
    intro_text = ["Добро пожаловать в игру", "",
                  "Правила игры"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    play = Play()
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    play_group.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                b = play.get_event(event)
                if b:
                    start_new()
                    play_group.remove(play)
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level():
    with open("data/" + 'current_level.txt', 'r') as cur:
        level = cur.read()
    filename = "data/" + 'level' + str(level) + '.txt'
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    level = (list(level_map))
    return level[:8], level[8], level[9:]



tile_images = ['apple1.png', 'cucumber1.png', 'kiwi1.png',
                'lemon1.png', 'lichi1.png', 'pear1.png',
                'strawberry1.png', 'watermelon1.png']

lightning_tile_images = ['apple3.png', 'cucumber3.png', 'kiwi3.png',
                'lemon3.png', 'lichi3.png', 'pear3.png',
                'strawberry3.png', 'watermelon3.png']

play_image = load_image('play.png')
heart_image = load_image('heart2.png')
moneta_image = load_image('moneta2.png')
empty_image = pygame.transform.scale(load_image('empty.png'), (80, 80))
tile_width = tile_height = 80


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type != '':
            self.image = load_image(tile_images[int(tile_type)])
        else:
            self.image = empty_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 50, tile_height * pos_y + 120)
    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            x = int((event.pos[0] - 50) / 80)
            y = int((event.pos[1] - 120) / 80)
            return True, x, y
        return False, None, None


class Play(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(play_group, all_sprites)
        self.image = play_image
        self.rect = self.image.get_rect().move(250, 700)

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False

# основной персонаж
player = None

# группы спрайтов

all_sprites = pygame.sprite.Group()

tiles_group = pygame.sprite.Group()

play_group = pygame.sprite.Group()

heart_group = pygame.sprite.Group()

moneta_group = pygame.sprite.Group()

goal_group = pygame.sprite.Group()

done_group = pygame.sprite.Group()

def generate_level(level):
    #print('i am in generate_level')
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile(level[y][x], x, y)
    # вернем игрока, а также размер поля в клетках
    return x, y

with open("data/" + 'current_level.txt', 'r') as cur:
    level = cur.read()

if str(level) == '1':
    start_screen()
else:
    start_new()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #tiles_group.draw(screen)
    #play_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
terminate()
