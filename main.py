#!venv/bin/python3
import time
import keyboard
import curses
import random
from snake import *

FOOD_PAIR = 1
SNAKE_HEAD_PAIR = 2
SNAKE_BODY_PAIR = 3


def print_board(stdscr, WIDTH, HEIGHT, snake, food):
    world = []

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (j == 0 and (i == 0 or i == HEIGHT-1)) \
                or (j == WIDTH-1 and (i == 0 or i == HEIGHT-1)):
                stdscr.addch(i, j, '+')
            elif i == 0 or i == HEIGHT-1:
                stdscr.addch(i, j, '-')
            elif j == 0 or j == WIDTH-1:
                stdscr.addch(i, j, '|')

    stdscr.attron(curses.color_pair(SNAKE_BODY_PAIR))
    for p in snake.body:
        stdscr.addch(p.y, p.x, 'o')
    stdscr.attroff(curses.color_pair(SNAKE_BODY_PAIR))

    stdscr.attron(curses.color_pair(SNAKE_HEAD_PAIR))
    stdscr.addch(snake.head.y, snake.head.x, '@')
    stdscr.attroff(curses.color_pair(SNAKE_HEAD_PAIR))

    stdscr.attron(curses.color_pair(FOOD_PAIR))
    stdscr.addch(food.y, food.x, '$')
    stdscr.attroff(curses.color_pair(FOOD_PAIR))


def clear_snake(stdscr, snake):
    for p in snake.body:
        stdscr.addch(p.y, p.x, ' ')


def food_in_body(snake, food):
    in_body = False
    for p in snake.body:
        if p == food:
            in_body = True
            break
    return in_body


def handle_input(e, snake):
    #if e.name == "up" and snake.direction != 2:
    if (e.name == "k" or e.name == "up") and snake.direction != 2:
        snake.direction = 0
    #elif e.name == "right" and snake.direction != 3:
    elif (e.name == "l" or e.name == "right") and snake.direction != 3:
        snake.direction = 1
    #elif e.name == "down" and snake.direction != 0:
    elif (e.name == "j" or e.name == "down") and snake.direction != 0:
        snake.direction = 2
    #elif e.name == "left" and snake.direction != 1:
    elif (e.name == "h" or e.name == "left") and snake.direction != 1:
        snake.direction = 3
    elif e.scan_code == 16:
        curses.endwin()
    curses.flushinp()


def main(stdscr):
    maxy, maxx = stdscr.getmaxyx()
    WIDTH = min(60, maxx-1)
    HEIGHT = min(20, maxy-1)
    SCORE = 0

    ORIG = Point(abs(maxx-WIDTH)//2, abs(maxy-HEIGHT-1)//2)
    canvas = stdscr.subwin(HEIGHT+1, WIDTH+1, ORIG.y, ORIG.x)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(FOOD_PAIR, curses.COLOR_GREEN, -1)
    curses.init_pair(SNAKE_HEAD_PAIR, curses.COLOR_RED, -1)
    curses.init_pair(SNAKE_BODY_PAIR, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)

    s = Snake()
    food = Point(-1, -1)
    keyboard.on_press(lambda e: handle_input(e, s))
    curses.curs_set(0)
    stdscr.clear()
    old_tail = s.body[-1]

    while True:
        old_tail = s.body[0]
        while ((not food_in_body(s, food)) and food.x == -1):
            food = Point(random.randint(1, WIDTH-1),
                         random.randint(1, HEIGHT-1))

        print_board(canvas, WIDTH, HEIGHT, s, food)
        # score drawing
        stdscr.addstr(ORIG.y+HEIGHT, ORIG.x+WIDTH//2, '$'+str(SCORE))
        canvas.refresh()
        clear_snake(canvas, s)
        s.step(WIDTH, HEIGHT)
        time.sleep(0.1)

        if s.head.x == food.x and s.head.y == food.y:
            s.body.insert(0, old_tail)
            canvas.addch(food.y, food.x, ' ')
            food.x = -1
            SCORE += 1
        for p in s.body:
            if s.head.x == p.x and s.head.y == p.y:
                stdscr.addstr(ORIG.y+HEIGHT, ORIG.x+WIDTH//2-13,
                              "Game over you scored: $%d" % SCORE)
                print_board(canvas, WIDTH, HEIGHT, s, food)
                stdscr.refresh()
                time.sleep(3)
                stdscr.clear()
                SCORE = 0
                s = Snake()
                break
        if curses.isendwin():
            curses.flushinp()
            break


if __name__ == '__main__':
    curses.wrapper(main)
