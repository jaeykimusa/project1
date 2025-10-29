import math

def getMagnitude(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class PointMassNode:
    def __init__(self, mass, position=None):
        self.mass = mass            # Data stored in the node
        self.position = position      # Tuple or coordinate (optional)
        self.prev = None              # Reference to previous node
        self.next = None              # Reference to next node

    def __repr__(self):
        return f"PointMassNode(mass={self.mass}, position={self.position})"

class FixedSupportNode:
    def __init__(self, mass, position=None):
        self.mass = mass            # Data stored in the node
        self.position = position      # Tuple or coordinate (optional)
        self.prev = None              # Reference to previous node
        self.next = None              # Reference to next node

    def __repr__(self):
        return f"FixedSupportNode(mass={self.mass}, position={self.position})"

class PointMassLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add(self, mass, position=None):
        if mass != 0:
            new_node = PointMassNode(mass, position)
        else:
            new_node = FixedSupportNode(mass, position)
        
        # case: first node
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return new_node
        
        # otherwise attach to tail
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
        return new_node

    def get(self, index):
        current = self.head
        count = 0
        while current is not None:
            if count == index:
                return current
            current = current.next
            count += 1
        raise IndexError("Index out of range")


lst = PointMassLinkedList()

step = 1 / 15

lst.add(mass=0.0, position=[0,0])
for i in range(14):
    x = (i+1) * step
    lst.add(mass=0.05, position=[x,0])
lst.add(mass=0.0, position=[1,0])

current = lst.head
while current is not None:
    print(current)
    current = current.next