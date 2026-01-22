import pygame
import math
import time
import random
from collections import deque

SCREEN_SIZE = 800
TILE_SIZE = 16
TILE_COUNT = SCREEN_SIZE//TILE_SIZE
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()
running = True
title_screen_active = True
title_screen_scene = 1
linesdrawn = True
mouseclicked = False
drawingblacksquares = True
drawingwhitesquares = False
selectinggreensquare = False
selectingredsquare = False
bfsactive = False
dfsactive = False
algovisualised = False
drawingpath = False
positions = set()
waitinglist = deque()
squaresofpath = deque()
visitedsquares = []
fromm = [-1]*(TILE_COUNT*TILE_COUNT)
nextROW = [-1,0,1,0]
nextCOL = [0,1,0,-1]
nextposition = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
greensquare = (-1, -1)
redsquare = (-1, -1)

def render_text(font, string, pos, color):
    text = font.render(string, True, color)
    screen.blit(text, (SCREEN_SIZE/2 - text.get_rect().width/2, pos))

def title_screen():
    global title_screen_active
    font1 = pygame.font.SysFont("Arial",40)
    font2 = pygame.font.SysFont("Arial",32)
    screen.fill("white")
    var = 96*math.sin(5*time.time())+96
    if title_screen_scene == 1:
        render_text(font1, "ПРОЕКТНА ЗАДАЧА ПО ПРЕДМЕТОТ", 20, (0, 0, 0))
        render_text(font1, "ПРОГРАМСКИ ЈАЗИЦИ", 70, (0, 0, 0))
        render_text(font1, "ТЕМА:", 230, (0, 0, 0))
        render_text(font1, "Визуелизација на алгоритмите БФС и ДФС", 280, (0, 0, 0))
        render_text(font1, "ИЗРАБОТИЛ:", 440, (0, 0, 0))
        render_text(font1, "Иван Георгиев IV-5", 490, (0, 0, 0))
        render_text(font1, "ПРИТИСНЕТЕ [SPACE] ЗА ДА ПРОДОЛЖИТЕ", 700, (var, var, var))
    elif title_screen_scene == 2:
        render_text(font2, "КОНТРОЛИ:", 20, (0, 0, 0))
        render_text(font2, "[1]* - Мод за цртање на непосетливи (црни) кавдратчиња", 70, (0, 0, 0))
        render_text(font2, "[2]* - Мод за цртање на посетливи (бели) кавдратчиња", 120, (0, 0, 0))
        render_text(font2, "[3]* - Мод за избирање на почетно (зелено) квадратче", 170, (0, 0, 0))
        render_text(font2, "[4]* - Мод за избирање на завршно (црвено) квадратче", 220, (0, 0, 0))
        render_text(font2, "[5]* - Визуелизирање на алгоритамот БФС", 270, (0, 0, 0))
        render_text(font2, "[6]* - Визуелизирање на алгоритамот ДФС", 320, (0, 0, 0))
        render_text(font2, "[G] - Вклучување/исклучување на линиите на мрежата", 370, (0, 0, 0))
        render_text(font2, "[C]* - Бришење на квадратчињата кои визуелизираат алгоритам", 420, (0, 0, 0))
        render_text(font2, "[M]* - Генерирање на мапа", 470, (0, 0, 0))
        render_text(font2, "[SPACE]* - Бришење на мапата", 520, (0, 0, 0))
        render_text(font2, "Сите контроли кои се обележани со * можат да се искористат", 585, (0, 0, 0))
        render_text(font2, "само доколку не е во тек визуелизација на алгоритам!", 635, (0, 0, 0))
        render_text(font1, "ПРИТИСНЕТЕ [SPACE] ЗА ДА ПРОДОЛЖИТЕ", 700, (var, var, var))
    else:
        title_screen_active = False

def drawsquare(color, col, row):
    pygame.draw.rect(screen, color, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_grid():
    t = time.time()
    for position in positions:
        col, row = position
        drawsquare("black", col, row)
    for square in squaresofpath:
        col, row = square
        if drawingpath:
            drawsquare("orange", col, row)
        else:
            drawsquare((255*(0.9+0.1*math.sin(3*t)),165*(0.9+0.1*math.sin(3*t)),0), col, row)
    for element in waitinglist:
        col, row = element
        if greensquare != (col, row) and redsquare != (col, row):
            drawsquare("purple", col, row)
    for element in visitedsquares:
        col, row = element
        if greensquare != (col, row) and redsquare != (col, row):
            drawsquare("blue", col, row)
    if greensquare != (-1, -1):
        col, row = greensquare
        drawsquare("green", col, row)
    if redsquare != (-1, -1):
        col, row = redsquare
        drawsquare("red", col, row)
    if linesdrawn:
        for i in range(TILE_COUNT):
            pygame.draw.line(screen, "black", (i*TILE_SIZE, 0), (i*TILE_SIZE, SCREEN_SIZE))
            pygame.draw.line(screen, "black", (0, i*TILE_SIZE), (SCREEN_SIZE, i*TILE_SIZE))

def set_modes(blacksquarescheck, whitesquarescheck, greensquarecheck, redsquarecheck):
    global drawingblacksquares, drawingwhitesquares, selectinggreensquare, selectingredsquare
    drawingblacksquares = blacksquarescheck
    drawingwhitesquares = whitesquarescheck
    selectinggreensquare = greensquarecheck
    selectingredsquare = redsquarecheck

def valid(col, row):
    if col >= 0 and col < TILE_COUNT and row >= 0 and row < TILE_COUNT and (col, row) not in positions and (col, row) not in waitinglist and (col, row) not in visitedsquares and greensquare != (col, row): return True
    return False

def draw_path():
    global squaresofpath, drawingpath
    redcol, redrow = redsquare
    greencol, greenrow = greensquare
    var = fromm[redrow*TILE_COUNT+redcol]
    while var != greenrow*TILE_COUNT+greencol:
        squaresofpath.appendleft((var-(var//TILE_COUNT)*TILE_COUNT,var//TILE_COUNT))
        var = fromm[var]
    for square in squaresofpath:
        col, row = square
        visitedsquares.remove((col, row))
        drawsquare("orange", col, row)
        draw_grid()
        pygame.display.update()
        time.sleep(0.02)
    drawingpath = False

def clear_visualisation():
    global algovisualised
    waitinglist.clear()
    visitedsquares.clear()
    squaresofpath.clear()
    algovisualised = False

def clear_map():
    global greensquare, redsquare
    clear_visualisation()
    positions.clear()
    greensquare = (-1, -1)
    redsquare = (-1, -1)

def valid_pos(col, row):
    if col>=0 and col<TILE_COUNT and row>=0 and row<TILE_COUNT: return True
    return False

def count_neighbours(col, row):
    neighbours = 0
    for nextpos in nextposition:
        nextcolidx, nextrowidx = nextpos
        nextcol = col+nextcolidx
        nextrow = row+nextrowidx
        if valid_pos(nextcol,nextrow) and (nextcol,nextrow) in positions: neighbours += 1
    return neighbours

def generate_map():
    global positions
    clear_map()
    for i in range(TILE_COUNT):
        for j in range(TILE_COUNT):
            x = random.randint(1,100)
            if x<=40: positions.add((i,j))
    for i in range(10):
        newpositions = set()
        for i in range(TILE_COUNT):
            for j in range(TILE_COUNT):
                neighbours = count_neighbours(i, j)
                if neighbours>=4: newpositions.add((i,j))
        positions = newpositions.copy()
    newpositions = set()
    for i in range(TILE_COUNT):
        for j in range(TILE_COUNT):
            if (i,j) not in positions: newpositions.add((i,j))
    positions = newpositions.copy()

def main_program():
    global greensquare, redsquare, bfsactive, dfsactive, algovisualised, drawingpath, fromm
    screen.fill("white")
    if mouseclicked and not (bfsactive or algovisualised or drawingpath):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = mouse_x//TILE_SIZE
        row = mouse_y//TILE_SIZE
        if drawingblacksquares:
            positions.add((col, row))
        elif drawingwhitesquares:
            if (col, row) in positions:
                positions.remove((col, row))
            if greensquare == (col, row):
                greensquare = (-1, -1)
            if redsquare == (col, row):
                redsquare = (-1, -1)
        elif selectinggreensquare:
            if (col, row) not in positions and redsquare != (col, row):
                greensquare = (col, row)
        elif selectingredsquare:
            if (col, row) not in positions and greensquare != (col, row):
                redsquare = (col, row)
    if bfsactive:
        length = len(waitinglist)
        if length == 0:
            bfsactive = False
            algovisualised = True
        for i in range(length):
            col, row = waitinglist.popleft()
            if redsquare == (col, row):
                bfsactive = False
                algovisualised = True
                drawingpath = True
            for j in range(4):
                nextcol = col+nextCOL[j]
                nextrow = row+nextROW[j]
                if (valid(nextcol, nextrow)):
                    waitinglist.append((nextcol, nextrow))
                    fromm[nextrow*TILE_COUNT+nextcol] = row*TILE_COUNT+col
            visitedsquares.append((col, row))
        time.sleep(0.05)
        if drawingpath:
            draw_path()
    if dfsactive:
        col, row = waitinglist.pop()
        for j in range(4):
                nextcol = col+nextCOL[j]
                nextrow = row+nextROW[j]
                if (valid(nextcol, nextrow)):
                    waitinglist.append((nextcol, nextrow))
                    fromm[nextrow*TILE_COUNT+nextcol] = row*TILE_COUNT+col
        if redsquare == (col, row):
            dfsactive = False
            drawingpath = True
            algovisualised = True
        length = len(waitinglist)
        if length == 0:
            dfsactive = False
            algovisualised = True
        visitedsquares.append((col, row))
        time.sleep(0.005)
        if drawingpath:
            draw_path()
    draw_grid()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if title_screen_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    title_screen_scene += 1
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseclicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouseclicked = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    set_modes(True, False, False, False)
                if event.key == pygame.K_2:
                    set_modes(False, True, False, False)
                if event.key == pygame.K_3:
                    set_modes(False, False, True, False)
                if event.key == pygame.K_4:
                    set_modes(False, False, False, True)
                if not (algovisualised or bfsactive or dfsactive or drawingpath):
                    if event.key == pygame.K_5 and greensquare != (-1, -1) and redsquare != (-1, -1):
                        waitinglist.append(greensquare)
                        bfsactive = True
                    if event.key == pygame.K_6 and greensquare != (-1, -1) and redsquare != (-1, -1):
                        waitinglist.append(greensquare)
                        dfsactive = True
                if not (bfsactive or dfsactive or drawingpath):
                    if event.key == pygame.K_c:
                        clear_visualisation()
                    if event.key == pygame.K_SPACE:
                        clear_map()
                    if event.key == pygame.K_m:
                        generate_map()
                if event.key == pygame.K_g:
                    linesdrawn = not linesdrawn
    if title_screen_active:
        title_screen()
    else:
        main_program()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
