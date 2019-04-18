from graphics import *
from abc import ABC, abstractmethod
from enum import Enum
import os
import sys
import glob
import random
from pathlib import Path

CIRCLE_BASIC_RADIUS = 40

class StructureType(Enum):
    CLASS = 0
    METHOD = 1
    VARIABLE = 2

class Parser(ABC):
    def __init__(self, dir):
        self.tracked_files = []
        self.updated_files = []
        self.directory = dir
    @abstractmethod
    def parse(self, file):
        pass
    @abstractmethod
    def update_dir(self):
        pass    
    def process_updated(self):
        pass
    def process_tracked(self):
        pass

class ParseC(Parser):

    def parse(self, file_path, obj_container):
        with open(file_path) as file:
            is_comment = False
            for str in file:
                if "/*" in str and not is_comment:
                    is_comment = True
                if "class " in str:
                    splitstr = str.split()
                    if ((str.index("class ") == 0 
                    or str[str.index("class ") - 1] in ["", " "])):
                        if not is_comment and not (str[1:2] == "//"):
                            print(str[-1])
                            print(splitstr)
                            name = splitstr[splitstr.index("class") + 1]
                            if (checkObjectName(obj_container, name)):                                   
                                struct = Structure(StructureType.CLASS, name, prepare_pos(obj_container))
                                obj_container.append(struct)
                if "*/" in str:
                    is_comment = False

    def update_dir(self, obj_container):
        for file in glob.iglob(self.directory + '/**', recursive=True):
            if file.endswith('.h') or file.endswith('.hpp'):
                if file not in self.tracked_files:
                    if file not in self.updated_files:
                        print("Caught this: " + file + "\n")
                        self.parse(file, obj_container)
                        self.updated_files.append(file)
                        #if os.stat(file).st_mtime > os.stat(self.tracked_files[self.tracked_files.index(file)]).st_mtime:

class Structure:
    def __init__(self, type, name = "Name_error", pos=Point(0,0)):
        self.name = Text(pos, name)
        if type == StructureType.CLASS:
            self.shape = Circle(pos, CIRCLE_BASIC_RADIUS) #TODO: compute_radius
        if type == StructureType.METHOD:
            self.shape = Rectangle(pos, Point(pos.getX() + 20, pos.getY() + 20))
    def getName(self):
        return self.name.getText()
class App:
    def __init__(self):
        self._win = GraphWin("DIVINEPLAN", 800, 600)
        self.obj = []
        self.isOn = True
        if len(sys.argv) > 1:
            self.parser = ParseC(sys.argv[1])
        self.loop()
    
    def draw(self):
        for obj in self.obj:
            obj.shape.draw(self._win)
            obj.name.draw(self._win)

    def loop(self):
        """ 
            Make element drawing work
        """        

        self.parser.update_dir(self.obj)
        self.draw()
        
        while self.isOn:
            mouse_point = self._win.getMouse()
            for obj in self.obj:
                if checkCollisions(mouse_point, obj.shape):
                    move_point = self._win.getMouse()
                    obj.shape.move(move_point.getX() - obj.shape.getCenter().getX(), move_point.getY() - obj.shape.getCenter().getY())
                    obj.name.move(move_point.getX() - obj.name.getAnchor().getX(), move_point.getY() - obj.name.getAnchor().getY())
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

def checkObjectName(obj_containter, name):
    for obj in obj_containter:
        if name == obj.getName():
            return False
    return True

def prepare_pos(obj_container):
    x = random.choice(range(0, 800))
    y = random.choice(range(0, 600))
    return Point(x,y)
