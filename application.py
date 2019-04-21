from parser import *
import sys
from graphics import *

class App:
    def __init__(self):
        self._win = GraphWin("DIVINEPLAN", 800, 600)
        self._win.setBackground("cyan")
        self.isOn = True
        if len(sys.argv) > 1:
            self.parser = ParseC(sys.argv[1])
        self.loop()
    
    # def draw(self, objects):
    #     for obj in objects:
    #         obj.shape.undraw()
    #         obj.name.undraw()
    #         obj.shape.draw(self._win)
    #         obj.name.draw(self._win)

    def loop(self):
        while self._win.isOpen:
            self.parser.updateDir(self.parser.getObjects())
            self.parser.processUpdated(self.parser.getObjects())
            print(self.parser.getObjects())
            #self.draw()
            mouse_point = self._win.getMouse()
            for obj in self.obj:
                if checkCollisions(mouse_point, obj.shape):
                    obj.shape.setFill("yellow")
                    move_point = self._win.getMouse()
                    obj.shape.move(move_point.getX() - obj.shape.getCenter().getX(), move_point.getY() - obj.shape.getCenter().getY())
                    obj.name.move(move_point.getX() - obj.name.getAnchor().getX(), move_point.getY() - obj.name.getAnchor().getY())
                    obj.shape.setFill("white")
        self._win.close()

def checkCollisions(point, circle):
    dx = abs(point.getX() - circle.getCenter().getX())
    dy = abs(point.getY() - circle.getCenter().getY())
    if dx > circle.getRadius() or dy > circle.getRadius():
        return False
    if dx + dy <= circle.getRadius():
        return True
    if dx**2 + dy**2 <= circle.getRadius() ** 2:
        return True
    return False

