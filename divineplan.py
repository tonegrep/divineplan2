from graphics import *
from abc import ABC, abstractmethod
from enum import Enum
import os
import sys
import glob
import random
from pathlib import Path

class StructureType(Enum):
    CLASS = 0
    METHOD = 1
    VARIABLE = 2

class Graphics:

    def __init__(self):
        self._win = GraphWin("DIVINEPLAN", 800, 600)

    def draw(self, objects):
        for obj in objects:
            obj.shape.draw(self._win)

    def flush_screen(self):
        self._win.flush()

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
            for str in file:
                if "class" in str:
                    #TODO: creation of class elements
                    struct = Structure(StructureType.CLASS, str.split()[str.split().index("class") + 1], prepare_pos(obj_container))
                    obj_container.append(struct)

    def update_dir(self, obj_container):
        for file in glob.iglob(self.directory + '/**', recursive=True):
            if file.endswith('.h') or file.endswith('.hpp'):
                if file not in self.tracked_files:
                    if file not in self.updated_files:
                        print("Caught this little shit: " + file + "\n")
                        self.parse(file, obj_container)
                        self.updated_files.append(file)
                        #if os.stat(file).st_mtime > os.stat(self.tracked_files[self.tracked_files.index(file)]).st_mtime:

class Structure:
    def __init__(self, type, name = "Name_error", pos=Point(0,0)):
        if type == StructureType.CLASS:
            self.shape = Circle(pos, 20) #TODO: compute_radius

class App:
    def __init__(self):
        self.obj = []
        self.isOn = True
        self.graph = Graphics()
        self.parser = ParseC(sys.argv[1])
        self.loop()

    def loop(self):
        """ 
            Make element drawing work
        """        
        while self.isOn:
            self.graph.flush_screen()
            #self.graph._win.
            self.parser.update_dir(self.obj)
            self.graph.draw(self.obj)
            self.graph._win.getMouse()
        self.graph._win.close()

def prepare_pos(obj_container):
    x = random.choice([20, 800])
    y = random.choice([20, 600])
    for obj in obj_container:
        obj_x = int(obj.shape.getCenter().getX())
        obj_y = int(obj.shape.getCenter().getY())
        if x in range(obj_x - 20, obj_x + 20): #(obj_x - 20, 0)
            obj.shape.move(-20, 0)
        if y in range(obj_y - 20, obj_y + 20):
            obj.shape.move(0,-20)
    return Point(x,y)

app = App()