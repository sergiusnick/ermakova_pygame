import pygame
import os
import sys
import random
import copy
pygame.init()
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))
pygame.display.set_caption('Три в ряд')
sound1 = pygame.mixer.Sound("data/" + 'pop.wav')
sound2 = pygame.mixer.Sound("data/" + 'lose1.wav')
sound3 = pygame.mixer.Sound("data/" + 'cheer2.wav')

clock = pygame.time.Clock()
running = True
STEP = 10
FPS = 100
tile_width = tile_height = 50

points = 0
all_points = 0

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        #print(fullname)
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
    global points
    points = 0
    with open("data/" + 'current_level.txt', 'r') as cur:
        level = cur.read()
    with open('data/' + 'current_lifes.txt', 'r') as l:
        lifes = l.read()
    with open('data/' + 'current_money.txt', 'r') as m:
        money = m.read()
    if int(lifes) > 0:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("data/" + 'fon_music.mp3')
            pygame.mixer.music.play(-1)
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
        heart_group.empty()
    else:
        lose(level, money, lifes)

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
    heart_group.empty()

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

    string_rendered = font.render(str(points), 1,
                                  pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    text_coord = 30
    intro_rect.top = text_coord
    intro_rect.x = 250
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
        goal.rect = goal.image.get_rect()
        goal.rect.x = intro_rect.x + 70
        goal.rect.y = text_coord - 60

    heart_group.draw(screen)
    moneta_group.draw(screen)
    goal_group.draw(screen)
    tiles_group.draw(screen)
    pygame.display.flip()
    loaded_level = [list(i) for i in loaded_level]
    first = True

    while moves != '0':
        goals_number = 0
        for i in goals:
            goals_number += int(i.split()[0])
        if goals_number == 0:
            win(level, money)
            return #победа
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data/" + 'current_lifes.txt', 'w') as current:
                    current.write(str(int(lifes) - 1))
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
                                        sound1.play()
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
        font5 = pygame.font.Font(None, 150)
        if need_to_shuffle(loaded_level):
            tiles_group.empty()
            for i in loaded_level:
                random.shuffle(i)
            random.shuffle(loaded_level)
            pygame.draw.rect(screen, pygame.Color('red'), (100, 320, 550, 150))
            string_rendered = font.render('Перемешиваем', 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord = 360
            intro_rect.top = text_coord
            intro_rect.x = 140
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
            generate_level(loaded_level)
            for i in range(10):
                clock.tick(10)
            while is_there_a_combination(loaded_level):
                loaded_level, goals = destruction(loaded_level, goals)
                tiles_group.empty()
                sound1.play()
                generate_level(loaded_level)
                loaded_level = falling(loaded_level, moves, goals)
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

    if moves == '0':
        goals_number = 0
        for i in goals:
            goals_number += int(i.split()[0])
        if goals_number != 0:
            lose(level, money, lifes)
            return #поражение
        else:
            win(level, money)
            return #победа


def change(first, second, loaded_level, cur, last, moves, goals):
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
        return loaded_level


def is_there_a_combination(level):
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


def need_to_shuffle(level):
    combination = False
    for i in range(len(level)):
        for j in range(len(level[0])):
            loaded_level = copy.deepcopy(level)
            if i == 0 and j == 0:
                loaded_level[i][j + 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j + 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i + 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i + 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
            elif i == 0 and j == len(level) - 1:
                loaded_level[i][j - 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j - 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i + 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i + 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
            elif i == len(level) - 1 and j == 0:
                loaded_level[i][j + 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j + 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i - 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i - 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
            elif i == len(level) - 1 and j == len(level) - 1:
                loaded_level[i][j - 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j - 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i - 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i - 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
            elif i == 0:
                loaded_level[i][j + 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j + 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i + 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i + 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i][j - 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j - 1]
                if is_there_a_combination(loaded_level):
                    combination = True
            elif j == 0:
                loaded_level[i][j + 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j + 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i + 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i + 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i - 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i - 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
            elif i == len(level) - 1:
                loaded_level[i][j + 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j + 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i][j - 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j - 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i - 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i - 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
            elif j == len(level) - 1:
                loaded_level[i][j - 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j - 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i + 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i + 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i - 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i - 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
            else:
                loaded_level[i][j - 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j - 1]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i + 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i + 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i - 1][j] = loaded_level[i][j]
                loaded_level[i][j] = level[i - 1][j]
                if is_there_a_combination(loaded_level):
                    combination = True
                loaded_level = copy.deepcopy(level)
                loaded_level[i][j + 1] = loaded_level[i][j]
                loaded_level[i][j] = level[i][j + 1]
                if is_there_a_combination(loaded_level):
                    combination = True
    if combination:
        return False
    else:
        return True




def win(level, money):
    global all_points
    all_points += points
    if int(level) != 10:
        pygame.mixer.music.stop()
        sound3.play()
        fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (100, 100, 800, 600))
        font = pygame.font.Font(None, 90)
        font2 = pygame.font.Font(None, 50)
        string_rendered = font.render('Уровень ' + str(level) + ' пройден !', 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 180
        intro_rect.top = text_coord
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render('+ 20', 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 320
        intro_rect.top = text_coord
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        moneta_group.empty()
        moneta = pygame.sprite.Sprite(all_sprites, moneta_group)
        moneta.image = moneta_image
        moneta.rect = moneta.image.get_rect()
        moneta.rect.x = 320
        moneta.rect.y = 310
        moneta_group.draw(screen)
        pygame.display.flip()
        moneta_group.remove(moneta)
        heart_group.empty()
        all_sprites.empty()
        tiles_group.empty()
        goal_group.empty()
        string_rendered = font2.render('Чтобы продолжить нажмите пробел', 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 550
        intro_rect.top = text_coord
        intro_rect.x = 180
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        with open("data/" + 'all_points.txt', 'r') as wp:
            current_points = wp.read()
        with open('data/' + 'current_money.txt', 'w') as m:
            m.write(str(int(money) + 20))
        with open("data/" + 'current_level.txt', 'w') as current:
            current.write(str(int(level) + 1))
        with open("data/" + 'all_points.txt', 'w') as p:
            p.write(str(int(current_points) + all_points))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_new()
                        return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)
    elif int(level) == 10:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("data/" + 'victory1.mp3')
        pygame.mixer.music.play(-1)
        with open("data/" + 'all_points.txt', 'r') as wp:
            current_points = wp.read()
        fon = pygame.transform.scale(load_image('fon5.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        font2 = pygame.font.Font(None, 40)
        font3 = pygame.font.Font(None, 200)
        string_rendered = font3.render('Победа !', 1,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord = 100
        intro_rect.top = text_coord
        intro_rect.x = 90
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render('Ваш итоговый счет: ' + str(int(current_points) + all_points) + ' очков', 1,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord = 300
        intro_rect.top = text_coord
        intro_rect.x = 90
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render('Топ-3 очков: ', 1,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord = 380
        intro_rect.top = text_coord
        intro_rect.x = 110
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        restart = Restart()
        restart_group.draw(screen)
        moneta_group.empty()
        pygame.display.flip()
        heart_group.empty()
        tiles_group.empty()
        goal_group.empty()
        with open('data/' + 'current_money.txt', 'w') as m:
            m.write(str(int(money) + 20))
        with open("data/" + 'current_level.txt', 'w') as current:
            current.write(str(1))
        with open("data/" + 'all_points.txt', 'w') as p:
            p.write(str(0))
        with open("data/" + 'top_points.txt', 'a') as t:
            t.write(str(int(current_points) + all_points))
            t.write(' ')
        with open("data/" + 'current_lifes.txt', 'w') as current:
            current.write(str(5))
        with open("data/" + 'top_points.txt', 'r') as t:
            top_scores = sorted([int(i) for i in t.read().split()], reverse=True)
        for i in range(3):
            if i < len(top_scores):
                string_rendered = font.render(str(i + 1) + '. ' + str(top_scores[i]) + ' очков', 1,
                                              pygame.Color('white'))
            else:
                string_rendered = font.render(str(i + 1) + '. ' + '-', 1,
                                              pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord = 450 + 50 * i
            intro_rect.top = text_coord
            intro_rect.x = 100
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    b = restart.get_event(event)
                    if b:
                        play_group.empty()
                        pygame.display.flip()
                        all_sprites.empty()
                        tiles_group.empty()
                        restart_group.empty()
                        continue_group.empty()
                        pygame.mixer.music.stop()
                        start_screen()
                        return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)


def lose(level, money, lifes):
    global all_points
    if int(lifes) - 1 > 0:
        fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (100, 100, 800, 600))
        font = pygame.font.Font(None, 90)
        font2 = pygame.font.Font(None, 50)
        string_rendered = font.render('Уровень ' + str(level) + ' не пройден !', 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 180
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render('- 1', 1,
                                      pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 320
        intro_rect.top = text_coord
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        heart_group.empty()
        heart = pygame.sprite.Sprite(all_sprites, heart_group)
        heart.image = heart_image
        heart.rect = heart.image.get_rect()
        heart.rect.x = 320
        heart.rect.y = 310
        heart_group.draw(screen)
        string_rendered = font2.render('Нажмите пробел чтобы попробовать еще раз', 1,
                                       pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord = 550
        intro_rect.top = text_coord
        intro_rect.x = 115
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        moneta_group.empty()
        pygame.display.flip()
        heart_group.empty()
        all_sprites.empty()
        tiles_group.empty()
        goal_group.empty()
        pygame.mixer.music.stop()
        sound2.play()
        with open("data/" + 'current_lifes.txt', 'w') as current:
            current.write(str(int(lifes) - 1))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_new()
                        return  # начинаем игру
                pygame.display.flip()
            clock.tick(FPS)
    else:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("data/" + 'lose2.mp3')
        pygame.mixer.music.play(-1)
        screen.fill((255, 255, 255))
        fon = pygame.transform.scale(load_image('fon4.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        font2 = pygame.font.Font(None, 40)
        font3 = pygame.font.Font(None, 200)
        string_rendered = font3.render('Поражение !', 1,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord = 180
        intro_rect.top = text_coord
        intro_rect.x = 90
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font.render('Продолжить игру за монеты или начать заново ?', 1,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord = 400
        intro_rect.top = text_coord
        intro_rect.x = 90
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        string_rendered = font2.render('Текущий счет: ' + str(money) + ' монет', 1,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord = 500
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        restart = Restart()
        restart_group.draw(screen)
        continue_ = Continue()
        continue_group.draw(screen)
        moneta_group.empty()
        pygame.display.flip()
        heart_group.empty()
        tiles_group.empty()
        goal_group.empty()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    a = continue_.get_event(event)
                    b = restart.get_event(event)
                    if b:
                        with open("data/" + 'current_level.txt', 'w') as current:
                            current.write(str(1))
                        with open("data/" + 'all_points.txt', 'w') as p:
                            p.write(str(0))
                        with open("data/" + 'current_lifes.txt', 'w') as current:
                            current.write(str(5))
                        play_group.empty()
                        pygame.display.flip()
                        all_sprites.empty()
                        tiles_group.empty()
                        restart_group.empty()
                        continue_group.empty()
                        pygame.mixer.music.stop()
                        start_screen()
                        return  # начинаем игру
                    if a:
                        if int(money) >= 100:
                            with open('data/' + 'current_money.txt', 'w') as m:
                                m.write(str(int(money) - 100))
                            with open("data/" + 'current_lifes.txt', 'w') as current:
                                current.write(str(1))
                            play_group.empty()
                            pygame.display.flip()
                            all_sprites.empty()
                            tiles_group.empty()
                            restart_group.empty()
                            continue_group.empty()
                            pygame.mixer.music.stop()
                            start_new()
                            return  # начинаем игру
                        else:
                            string_rendered = font2.render('Недостаточно средств', 1,
                                                          pygame.Color('red'))
                            intro_rect = string_rendered.get_rect()
                            text_coord = 830
                            intro_rect.top = text_coord
                            intro_rect.x = 500
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)

            pygame.display.flip()
            clock.tick(FPS)


def start_screen():
    global points
    with open("data/" + 'current_level.txt', 'r') as cur:
        level = cur.read()
    with open('data/' + 'current_lifes.txt', 'r') as l:
        lifes = l.read()
    with open('data/' + 'current_money.txt', 'r') as m:
        money = m.read()
    if int(lifes) > 0:
        pygame.mixer.music.load("data/" + 'fon_music.mp3')
        pygame.mixer.music.play(-1)
        points = 0
        intro_text = ["Правила игры.", "",
                      'Ваши цели - фрукты, ягоды и овощи. Чтобы пройти уровень, соберите нужное', "",
                      'количество целей. Собирать их вы можете составляя ряды длиной 3 и более. Помните, что', "",
                      'количество ходов ограничено. В начале игры у вас 5 жизней. Если вы не соберете все цели,', "",
                      'у вас отнимется одна жизнь и вы сможете попробовать пройти уровень еще раз. Когда', "",
                      'у вас закончатся жизни - вы проиграли, и начинаете с первого уровня. Но не переживайте,', "",
                      'вы всегда можете купить дополнительную жизнь за 100 монет ! Если вы собрали все цели,', "",
                      'то поздравляю - вы переходите на следующий уровень и получаете 20 монет. Проходя уровни', "",
                      'вы собираете очки, которые суммируются. Пройдя все десять уровней вы побеждаете.', ""]

        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        play = Play()
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 50)
        text_coord = 50
        string_rendered = font2.render('Добро пожаловать в игру !', 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 20
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 5
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        play_group.draw(screen)
        pygame.display.flip()
    else:
        lose(level, money, lifes)

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
restart_image = load_image('restart.png')
continue_image = load_image('continue.png')
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


class Restart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(restart_group, all_sprites)
        self.image = restart_image
        self.rect = self.image.get_rect().move(100, 650)

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False


class Continue(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(continue_group, all_sprites)
        self.image = continue_image
        self.rect = self.image.get_rect().move(320, 650)

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

restart_group = pygame.sprite.Group()

continue_group = pygame.sprite.Group()


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile(level[y][x], x, y)
    # вернем размер поля в клетках
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
    clock.tick(FPS)
    pygame.display.flip()
terminate()
