class ScreenObject:
    def __init__(self, struct, objType, obj_container):
        self.struct = struct
        shape = {
            objType == StructureType.CLASS: Circle(preparePos(obj_container))#,
            #objType == StructureType.METHOD: Rectangle(preparePos(obj_container),preparePos(obj_container))
        }[True]


def preparePos(obj_container):
    x = random.choice(range(100, 700))
    y = random.choice(range(100, 500))
    return Point(x,y)