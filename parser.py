from abc import ABC, abstractmethod
import glob
import os
from enum import Enum

class StructureType(Enum):
    CLASS = 0
    METHOD = 1
    VARIABLE = 2

class Structure:
    def __init__(self, type, name= "Some class"):
        self._name = name
        self._type = type
        self._children = []
    def getName(self):
        return self._name
    def setName(self, newName):
        self._name = newName
    def getType(self):
        return self._type
    def setType(self, type):
        self._type = type
    def getChildren(self):
        return self._children

class Parser(ABC):
    def __init__(self, dir):
        self.objects = []
        self.tracked_files = []
        self.updated_files = []
        self.directory = dir
        self.extensions = None
    @abstractmethod
    def parse(self, file, obj_container):
        pass
    def updateDir(self, obj_container):
        for file in glob.iglob(self.directory + '/**', recursive=True):
            if file.endswith(self.extensions):
                if (file not in self.tracked_files
                or (os.stat(file).st_mtime != os.stat(self.tracked_files[self.tracked_files.index(file)]).st_mtime 
                and file not in self.updated_files)):
                    print("Caught this: " + file + "\n")
                    self.updated_files.append(file)

    def processUpdated(self, obj_container):
        for file in self.updated_files:
            self.parse(file, obj_container)
            self.tracked_files.append(file)
        self.updated_files.clear()

    def getObjects(self):
        return self.objects

class ParseC(Parser):

    def __init__(self, dir):
        Parser.__init__(self, dir)
        self.extensions = ('h', 'hpp')

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
                        if not is_comment and not (splitstr[0] == "//"):
                            print(str[-1])
                            print(splitstr)
                            name = splitstr[splitstr.index("class") + 1]
                            if (checkObjectName(obj_container, name)):
                                struct = Structure(StructureType.CLASS, name)
                                self.objects.append(struct)
                if "*/" in str:
                    is_comment = False

def checkObjectName(obj_containter, name):
    for obj in obj_containter:
        if name == obj.getName():
            return False
    return True