
class Point():
    x = 0
    y = 0
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Snake():
    body = []
    head = Point(0,0)
    direction = 1

    def __init__(self):
        self.body = [Point(1,1),Point(2,1),Point(3,1)]
        self.head = Point(4,1)

    def step(self, WIDTH, HEIGHT):
        tail = self.body.pop(0)
        self.body.append(Point(self.head.x,self.head.y))
        if self.direction == 0:
            self.head.y = (self.head.y - 1) % HEIGHT
        elif self.direction == 1:
            self.head.x = (self.head.x + 1) % WIDTH 
        elif self.direction == 2:
            self.head.y = (self.head.y + 1) % HEIGHT
        elif self.direction == 3:
            self.head.x = (self.head.x - 1) % WIDTH
