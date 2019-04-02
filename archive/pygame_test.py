import pygame as pg

import time
import threading


def graphics(nr):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    yellow = (255, 255, 0)

    pg.init()

    size = (700, 500)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("HojDoj")

    done = False

    clock = pg.time.Clock()
    screen = pg.display.set_mode((640, 280))
    myfont = pg.font.SysFont("Comic Sans MS", 60)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        label_1 = myfont.render(str(nr[0]), 1, GREEN)

        screen.fill(WHITE)
        screen.blit(label_1, (100, 100))
        pg.display.flip()

        clock.tick(60)

    pg.quit()


def test_loop(nr):
    while True:
        print("Yo {}".format(nr[0]))
        time.sleep(1)
        nr[0] = nr[0] + 1


values = [3]
t1 = threading.Thread(target=graphics, args=(values,))
t2 = threading.Thread(target=test_loop, args=(values,))

t1.start()
t2.start()

t1.join()
t2.join()

