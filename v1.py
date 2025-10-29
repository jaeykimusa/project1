import math

def getMagnitude(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class PointMassNode:
    def __init__(self, mass, position=None, velocity=None):
        self.mass = mass            # Data stored in the node
        self.position = position      # Tuple or coordinate (optional)
        self.velocity = velocity
        self.prev = None              # Reference to previous node
        self.next = None              # Reference to next node

    def __repr__(self):
        return f"PointMassNode(mass={self.mass}, position={self.position})"

class FixedSupportNode:
    def __init__(self, mass, position=None, velocity=None):
        self.mass = mass            # Data stored in the node
        self.position = position      # Tuple or coordinate (optional)
        self.velocity = None
        self.prev = None              # Reference to previous node
        self.next = None              # Reference to next node

    def __repr__(self):
        return f"FixedSupportNode(mass={self.mass}, position={self.position})"

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add(self, mass, position=None, velocity=None):
        if mass != 0:
            new_node = PointMassNode(mass, position, velocity)
        else:
            new_node = FixedSupportNode(mass, position, velocity)
        
        # case: first node
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.size += 1
            return new_node
        
        # otherwise attach to tail
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
        self.size += 1
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


class PointMassSystem:
    def __init__(self, list):
        self.list = list
        self.q = 3

list = LinkedList()

step = 1 / 15

list.add(mass=0.0, position=[0,0], velocity=[0,0])
for i in range(14):
    x = (i+1) * step
    list.add(mass=0.05, position=[x,0], velocity=[0,0])
list.add(mass=0.0, position=[1,0], velocity=[0,0])

p1 = PointMassSystem(list)

current = p1.list.head
while current is not None:
    print(current)
    current = current.next
print(list.size)