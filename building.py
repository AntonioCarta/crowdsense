import numpy as np
import scipy.ndimage
from enum import IntEnum
from collections import deque
from matplotlib import pyplot as plt


class Field(IntEnum):
    UNPROCESSED = 0
    OUTSIDE = 1
    WALL = 2
    DOOR = 3
    EXIT_DOOR = 4
    INSIDE = 5


class Direction(IntEnum):
    UNPROCESSED = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Building:

    def __init__(self, filename, origin='Antonio'):
        self.image = scipy.ndimage.imread(filename)
        self.image = self.image[:, :, :3]
        self.origin = origin
        if self.origin == 'Antonio':
            self.rmap = {(34, 177, 76): Field.DOOR,
                         (255, 255, 255): Field.INSIDE,
                         # also outside, but already done
                         (0, 0, 0): Field.WALL,
                         }
            self.cmap = {self.rmap[b]: b for b in self.rmap}
            self.cmap[Field.OUTSIDE] = (255, 255, 255)
        self.fields = np.zeros(self.image.shape[:2], dtype=int)
        self.direction = np.zeros(self.image.shape[:2], dtype=int)
        self.parse_fields()

    def neighbours(self, point):
        n, m = self.image.shape[:2]
        x, y = point
        for i, dx, dy in zip(range(1, 5), [-1, 0, 1, 0], [0, 1, 0, -1]):
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= n or ny < 0 or ny >= m:
                continue
            yield i, (nx, ny)

    def parse_fields(self):
        n, m = self.image.shape[:2]
        processed = {(0, 0)}
        outside = deque([(0, 0)])
        walls_doors = []
        while len(outside) > 0:
            x, y = outside.popleft()
            self.fields[x, y] = Field.OUTSIDE
            for i, (nx, ny) in self.neighbours((x, y)):
                if (nx, ny) not in processed and \
                        np.all(self.image[nx, ny] == self.image[x, y]):
                    outside.append((nx, ny))
                    processed.add((nx, ny))
                elif np.any(self.image[nx, ny] != self.image[x, y]):
                    walls_doors.append((nx, ny))
        colours = {tuple(self.image[x, y]) for x, y in walls_doors}

        print(colours)

        for x in range(self.image.shape[0]):
            for y in range(self.image.shape[1]):
                el = tuple(self.image[x, y])
                if el in self.rmap and self.fields[x, y] == Field.UNPROCESSED:
                    self.fields[x, y] = self.rmap[el]
                elif el not in self.rmap:
                    print("Unknown field at ({}, {}) with value {}.".format(x, y, el))
        exit_doors = [(xx, yy) for (xx, yy) in walls_doors
                      if tuple(self.image[xx, yy]) == self.cmap[Field.DOOR]]
        for (x, y) in exit_doors:
            self.fields[x, y] = Field.EXIT_DOOR
        self.bfs_inside(deque(exit_doors))

    def bfs_inside(self, queue):
        visited = set()
        while len(queue):
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for (i, (nx, ny)) in self.neighbours((x, y)):
                if self.fields[nx, ny] in [Field.WALL, Field.OUTSIDE]:
                    continue
                queue.append((nx, ny))
                if self.direction[nx, ny] == Field.UNPROCESSED:
                    self.direction[nx, ny] = (i + 2) % 4
                    if self.direction[nx, ny] == 0:
                        self.direction[nx, ny] = 4


if __name__ == '__main__':
    r1 = 'buildings/export2.png'
    bdg = Building(r1)
    plt.imshow(bdg.direction)
    plt.colorbar()
    plt.show()
