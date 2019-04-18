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
                    #and splitstr[splitstr.index("class") - 1] != "friend"
                    #and not splitstr[-1].endswith(';')):
                        if not is_comment and not (str[1:2] == "//"):
                            print(str[-1])
                            print(splitstr)
                            name = splitstr[splitstr.index("class") + 1]
                            for obj in obj_container:
                                if name == obj.getText()
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
        self._win.getMouse()
        #while self.isOn:
        #    pass
        self._win.close()


def relocate_shape(current_pos, obj_container):
    for obj in obj_container:
        obj_x = int(obj.shape.getCenter().getX())
        obj_y = int(obj.shape.getCenter().getY())
        if current_pos.getX() in range(obj_x - CIRCLE_BASIC_RADIUS, obj_x) and current_pos.getY() in range(obj_y - CIRCLE_BASIC_RADIUS, obj_y):
            current_pos.move(-CIRCLE_BASIC_RADIUS, -CIRCLE_BASIC_RADIUS)
            relocate_shape(current_pos, obj_container)
        elif current_pos.getX() in range(obj_x, obj_x + CIRCLE_BASIC_RADIUS) and current_pos.getY() in range(obj_y - CIRCLE_BASIC_RADIUS, obj_y):
            current_pos.move(CIRCLE_BASIC_RADIUS, -CIRCLE_BASIC_RADIUS)
            relocate_shape(current_pos, obj_container)
        elif current_pos.getX() in range(obj_x - CIRCLE_BASIC_RADIUS, obj_x) and current_pos.getY() in range(obj_y, obj_y + CIRCLE_BASIC_RADIUS):
            current_pos.move(-CIRCLE_BASIC_RADIUS, CIRCLE_BASIC_RADIUS)
            relocate_shape(current_pos, obj_container)
        elif current_pos.getX() in range(obj_x, obj_x + CIRCLE_BASIC_RADIUS) and current_pos.getY() in range(obj_y, obj_y + CIRCLE_BASIC_RADIUS):
            current_pos.move(CIRCLE_BASIC_RADIUS, CIRCLE_BASIC_RADIUS)
            relocate_shape(current_pos, obj_container)
    return current_pos

def prepare_pos(obj_container):
    x = random.choice(range(0, 800))
    y = random.choice(range(0, 600))
    return Point(x,y)
    #return relocate_shape(Point(x,y), obj_container)
    # x = random.choice(range(200, 400))
    # y = random.choice(range(200, 400))
    # #x = 400
    # #y = 300
    # for obj in obj_container:
    #     obj_x = int(obj.shape.getCenter().getX())
    #     obj_y = int(obj.shape.getCenter().getY())
    #     if x in range(obj_x - 40, obj_x + 40): #(obj_x - 20, 0)
    #         x_move_distance = random.choice(range(-80, 80))
    #         obj.shape.move(x_move_distance, 0)
    #         obj.name.move(x_move_distance, 0)
    #     if y in range(obj_y - 40, obj_y + 40):
    #         y_move_distance = random.choice(range(-80, 80))
    #         obj.shape.move(0, y_move_distance)
    #         obj.name.move(0, y_move_distance)


    # for i in range(100,700, 80):
    #     for j in range(100, 500, 80):
    #         collided = False
    #         for obj in obj_container:
    #             obj_x = int(obj.shape.getCenter().getX())
    #             obj_y = int(obj.shape.getCenter().getY())
    #             if i in range(obj_x - 40, obj_x + 40) and j in range(obj_y - 40, obj_y + 40):
    #                 collided = True
    #         if not collided:
    #             return Point(i,j)
    # return Point(400,300)


