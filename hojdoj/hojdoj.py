import pygame as pg
 
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


number_1 = 1
number_2 = 2

between_label = myfont.render('+', 1 , GREEN)
 
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    label_1 = myfont.render(str(number_1), 1, GREEN)
    label_2 = myfont.render(str(number_2), 1, GREEN)
    
    screen.fill(WHITE)
    screen.blit(label_1, (100, 100))
    screen.blit(between_label, (150, 100-5))
    screen.blit(label_2, (200, 100)) 
    pg.display.flip()
 
    clock.tick(60)
 
pg.quit()
