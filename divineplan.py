from graphics import *
from abc import ABC, abstractmethod
from enum import Enum
import os
import sys
import glob
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
                    struct = Structure("class","""formula""",compute_pos(obj_container))
                    obj_container.append(struct)

    def update_dir(self):
        for file in glob.iglob(self.directory + '/**', recursive=True):
            if file.endswith('.h') or file.endswith('.hpp'):
                if file not in self.tracked_files:
                    if file not in self.updated_files:
                        print("Caught this little shit: " + file + "\n")
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
        while self.isOn:
            self.graph.flush_screen()
            self.parser.update_dir()
            self.graph.draw(self.obj)
        self.graph._win.close()




def compute_pos(obj_container):
    pass


app = App()