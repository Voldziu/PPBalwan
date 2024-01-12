# This is a sample Python script.
import time
from copy import copy

import pygame

from Classes import *

if __name__ == '__main__':
    pygame.init()


    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    drawing_surface = pygame.Surface((WIDTH,HEIGHT))
    P1, P2, P3 = Point(50, 100), Point(100, 50), Point(500, 2)
    drawing_surface.fill((0,0,0))
    position = Point(200,200)

    kolko1 = Circle(Point(200,200),20,isFilled=False)
    kolko2 = Circle(Point(200, 240), 30, isFilled=False)
    kolko3 = Circle(Point(200, 300), 50, isFilled=False)

    kompleks = ComplexItem([kolko1,kolko2,kolko3])
    kompleks2 = ComplexItem([kolko1, kolko2, kolko3])
    scena = Scene(screen,drawing_surface)

    scena.addItem(Circle(position, 5, True ))
    scena.addItem(Rect(position,50,100,True))
    scena.addItem(Triangle(position,P2,P3,True))
    scena.addItem(Segment(Point(100,100),Point(50,50)))
    scena.addItem(TextItem(Point(300,300),'KOCHAM\nPP'))
    scena.addItem(Sinus(position,isFilled=False))
    kompleks.translate(Point(100,100))
    scena.addItem(kompleks)
    for item in scena.ItemList:
        item.translate(Point(100,100))
    running = True
    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        scena.draw()
        if running == False:
            pygame.quit()
        time.sleep(5)









