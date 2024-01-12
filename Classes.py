import time

import pygame
import numpy as np
from abc import ABC, abstractmethod


class Point:
    def __init__(self,X:int,Y:int):
        self.__X=X
        self.__Y=Y



    def getX(self):
        return self.__X
    def getY(self):
        return self.__Y



class Item(ABC):

    def __init__(self,position:Point):

        self.Position=position
    def getPosition(self)->Point:
        return self.Position
    def translate(self,p:Point):
        self.Position=Point(self.Position.getX()+p.getX(),self.Position.getY()+p.getY())

    @abstractmethod
    def getBoundingBox(self)->[Point,Point,Point,Point]:
        pass

    @abstractmethod
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        pass
    def drawBoundingBox(self,screen:pygame.surface,drawing_surface:pygame.surface):
        coords_list = self.getBoundingBox()

        pygame.draw.polygon(surface=drawing_surface, color=(255, 0, 0),
                            points=[(item.getX(),item.getY()) for item in coords_list ], width=1)
        screen.blit(drawing_surface, (0, 0))
        pygame.display.flip()
class Primitive(Item):
    @abstractmethod
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        pass


class ComplexItem(Item):
    def __init__(self,childrenItem:list[Item]):

        self.ChildrenList:list[Item]=childrenItem
        self.positionX = min([child.getPosition().getX() for child in self.ChildrenList])
        self.positionY = min([child.getPosition().getY() for child in self.ChildrenList])
        super().__init__(Point(self.positionX,self.positionY))

    def addChild(self,Child:Item):
        self.ChildrenList.append(Child)
        #update position
        if(self.positionX<Child.Position.getX()):
            self.positionX=Child.Position.getX()
        if (self.positionY < Child.Position.getY()):
            self.positionY = Child.Position.getY()
        self.Position=Point(self.positionX,self.positionY)


    def getChildren(self)->list[Item]:
        return self.ChildrenList

    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        for child in self.ChildrenList:
            child.draw(screen,drawing_surface)
    def getBoundingBox(self):
        maxX= max([child.getBoundingBox()[2].getX() for child in self.ChildrenList])

        maxY=max([child.getBoundingBox()[2].getY() for child in self.ChildrenList])

        topleft = self.Position
        topright = Point(maxX,self.Position.getY())
        bottomright = Point(maxX,maxY)
        bottomleft = Point(self.Position.getY(),maxY)
        return [topleft,topright,bottomright,bottomleft]
    def translate(self,p:Point):
        for child in self.ChildrenList:
            child.translate(p)
        self.Position=Point(self.Position.getX()+p.getX(),self.Position.getY()+p.getY())


class TextItem(Item):
    def __init__(self,position:Point,Text:str):
        self.Text=Text
        self.Size=(0,0)
        super().__init__(position)
    def getText(self)->str:
        return self.Text
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        font = pygame.font.Font(None, 50)
        tokens = self.Text.split("\n")

        Y_fix=0
        X_Max=0
        for token in tokens:
            text_surface= font.render(token, True, (255, 255, 255))
            drawing_surface.blit(text_surface, (self.Position.getX(), self.Position.getX()+Y_fix))
            if(X_Max<text_surface.get_size()[0]):
                X_Max=text_surface.get_size()[0]

            screen.blit(drawing_surface, (0, 0))
            pygame.display.flip()
            Y_fix+=text_surface.get_size()[1]
        self.Size=(X_Max,Y_fix)
    def getBoundingBox(self) ->[Point,Point,Point,Point]:
        x = self.Position.getX()
        y = self.Position.getY()
        x_moved = x+self.Size[0]
        y_moved = y+self.Size[1]

        return [self.Position, Point(x_moved, y), Point(x_moved, y_moved), Point(x, y_moved)]


class Shape(Primitive):
    def __init__(self,position:Point,isFilled:bool):
        super().__init__(position)
        self.isFilled=isFilled
    def getIsFilled(self)->bool:
        return self.isFilled

class Segment(Primitive):
    def __init__(self,Start:Point,End:Point):
        minX=min(Start.getX(),End.getY())
        minY=min(Start.getY(),End.getY())
        super().__init__(Point(minX,minY))

        self.Start=Start
        self.End=End
        self.Length = int(np.sqrt((self.Start.getX() - End.getX()) ** 2 + (self.Start.getY() - End.getY()) ** 2))
    def getLenth(self)->int:
        return self.Length
    def getStart(self)->Point:
        return self.Start
    def getEnd(self)->Point:
        return self.End
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        pygame.draw.polygon(surface=drawing_surface, color=(255, 255, 255),
                            points=[(self.Start.getX(), self.Start.getY()), (self.End.getX(), self.End.getY()),
                                    ], width= 1)
        screen.blit(drawing_surface, (0, 0))
        pygame.display.flip()
    def getBoundingBox(self) ->[Point,Point,Point,Point]:

        x = self.Start.getX()
        y = self.Start.getY()
        x_moved = self.End.getX()
        y_moved = self.End.getY()

        return [Point(x,y), Point(x_moved, y), Point(x_moved, y_moved), Point(x, y_moved)]
    def translate(self,p:Point):
        self.Position=Point(self.getPosition().getX()+p.getX(),self.getPosition().getY()+p.getY())
        self.Start=Point(self.Start.getX()+p.getX(),self.Start.getY()+p.getY())
        self.End=Point(self.End.getX()+p.getX(),self.End.getY()+p.getY())
class Circle(Shape):
    def __init__(self,position:Point,radius:int,isFilled:bool):
        super().__init__(position,isFilled)
        self.Radius=radius
    def getRadius(self) -> int:
        return self.Radius
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        pygame.draw.circle(drawing_surface,(255,255,255),center=(self.Position.getX()+self.Radius,self.Position.getY()+self.Radius),radius=self.Radius,width=(0 if self.getIsFilled() else 1))
        screen.blit(drawing_surface, (0, 0))
        pygame.display.flip()

    def getBoundingBox(self) -> [Point, Point, Point, Point]:
        x= self.Position.getX()
        y=self.Position.getY()
        x_moved= x+self.Radius*2
        y_moved=y+self.Radius*2

        return [self.Position,Point(x_moved,y),Point(x_moved,y_moved),Point(x,y_moved)]




class Rect(Shape):
    def __init__(self,position:Point,Width:int,Height:int,isFilled:bool):
        super().__init__(position,isFilled)
        self.Width=Width
        self.Height=Height

    def getWidth(self):
        return self.Width

    def getHeigt(self):
        return self.Height
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        pygame.draw.rect(drawing_surface, (255, 255, 255),rect=pygame.Rect(self.Position.getY(),self.Position.getY(),self.Width,self.Height), width=(0 if self.getIsFilled() else 1) )
        screen.blit(drawing_surface, (0, 0))
        pygame.display.flip()

    def getBoundingBox(self) -> [Point, Point, Point, Point]:
        x = self.Position.getX()
        y = self.Position.getY()
        x_moved = x + self.Width
        y_moved = y + self.Height

        return [self.Position, Point(x_moved, y), Point(x_moved, y_moved), Point(x, y_moved)]

class Triangle(Shape):
    def __init__(self,P1:Point,P2:Point,P3:Point,isFilled:bool):
        minLeftX = min(P1.getX(),P2.getX(),P3.getX())
        minLeftY = min(P1.getY(), P2.getY(), P3.getY())

        super().__init__(Point(minLeftX,minLeftY),isFilled)
        self.P1=P1
        self.P2=P2
        self.P3=P3
    def getP1(self) -> Point:
        return self.P1

    def getP2(self) -> Point:
        return self.P2

    def getP3(self) -> Point:
        return self.P3
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):

        pygame.draw.polygon(surface=drawing_surface,color=(255, 255, 255),points=[(self.P1.getX(),self.P1.getY()),(self.P2.getX(),self.P2.getY()),(self.P3.getX(),self.P3.getY())],width=(0 if self.getIsFilled() else 1))
        screen.blit(drawing_surface, (0, 0))
        pygame.display.flip()

    def getBoundingBox(self) -> [Point, Point, Point, Point]:
        X_max = max(self.P1.getX(),self.P2.getX(),self.P3.getX())
        X_min = min(self.P1.getX(), self.P2.getX(), self.P3.getX())
        Y_max = max(self.P1.getY(), self.P2.getY(), self.P3.getY())
        Y_min = min(self.P1.getY(), self.P2.getY(), self.P3.getY())
        return [Point(X_min,Y_min),Point(X_max,Y_min),Point(X_max,Y_max),Point(X_min,Y_max)]
    def translate(self,p:Point):
        self.P1=Point(self.P1.getX()+p.getX(),self.P1.getY()+p.getY())
        self.P2 = Point(self.P2.getX() + p.getX(), self.P2.getY() + p.getY())
        self.P3 = Point(self.P3.getX() + p.getX(), self.P3.getY() + p.getY())
        self.Position=Point(self.Position.getX()+p.getX(),self.Position.getY()+p.getY())

class Sinus(Shape):
    def __init__(self,Position:Point,isFilled=False,Amplitude=100,length=63,frequency=0.1):

        self.Amplitude = Amplitude


        self.Frequency=frequency
        self.Length=length
        super().__init__(Position, isFilled)
    def sin_and_translate(self,p:float):
        x = p
        y= np.sin(p*self.Frequency)*self.Amplitude

        # x_prim = x*np.cos(self.Translation_radians) - y * np.sin(self.Translation_radians)
        # y_prim = x*np.sin(self.Translation_radians)+y* np.cos(self.Translation_radians)


        return (int(self.Position.getX()+x), int(self.Position.getY()+self.Amplitude+y))
    def draw(self,screen:pygame.surface,drawing_surface:pygame.surface):
        pygame.draw.lines(drawing_surface,(255,255,255),False, [self.sin_and_translate(p) for p in range(0,self.Length)],width=(10 if self.getIsFilled() else 1))
        screen.blit(drawing_surface, (0, 0))
        pygame.display.flip()

    def getBoundingBox(self) ->[Point,Point,Point,Point]:
        x_pos,y_pos= self.Position.getX(),self.Position.getY()
        topleft=self.Position
        topright=Point(x_pos,y_pos+2*self.Amplitude)
        bottomright=Point(x_pos+self.Length,y_pos+2*self.Amplitude)
        bottomleft=Point(x_pos+self.Length,y_pos)
        return [topleft,topright,bottomright,bottomleft]



class Scene():
    def __init__(self,screen:pygame.surface,drawing_surface:pygame.surface):
        self.ItemList:list[Item]=[]
        self.screen=screen
        self.drawing_surface=drawing_surface

    def draw(self):
        for item in self.ItemList:
            item.draw(screen=self.screen,drawing_surface=self.drawing_surface)
            item.drawBoundingBox(self.screen,self.drawing_surface)


    def addItem(self,item:Item):
        self.ItemList.append(item)
