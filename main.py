# This is a sample Python script.
import time
from copy import copy

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

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
    scena.addItem("Circle", position, 20, False)
    scena.addItem("Circle",position, 5, False )


    scena.addItem("Rect",position,50,100,True)
    scena.addItem("Triangle",position,P2,P3,True)
    scena.addItem("Segment",Point(100,100),Point(50,50))
    scena.addItem("TextItem",Point(300,300),'KOCHAM\nPP')
    scena.addItem("Sinus",position,)
    # kompleks.translate(Point(100,100))
    scena.addItem("ComplexItem",[kolko1,kolko2,kolko3])
    # for item in scena.ItemList:
    #     item.translate(Point(100,100))
    running = True
    while running:
        for event in pygame.event.get():

            scena.draw()
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    drawing_surface.fill((0, 0, 0))

                    for item in scena.ItemList:
                        bounding_box = item.getBoundingBox()

                        for point in bounding_box:
                            print(f'{point.getX()},{point.getY()}')
                        if (
                                bounding_box[0].getX() <= event.pos[0] <= bounding_box[2].getX()
                                and bounding_box[0].getY() <= event.pos[1] <= bounding_box[2].getY()
                        ):
                            print(f'selected:{item.__class__.__name__}')

                            decorated_item=DecoratedItem(item.getPosition(),item)
                            decorated_item.draw(screen,drawing_surface)










