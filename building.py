import numpy as np
import scipy.ndimage
from enum import IntEnum
from collections import deque
from matplotlib import pyplot as plt


class Field(IntEnum):
    UNPROCESSED = 0
    OUTSIDE = 1
    WALL = 2
    INSIDE = 3
    DOOR = 4
    EXIT_DOOR = 5


class Building:

    def __init__(self, filename, origin='Antonio'):
        self.image = scipy.ndimage.imread(filename)
        self.image = self.image[:, :, :3]
        self.origin = origin
        self.fields = np.zeros(self.image.shape[:2], dtype=int)
        print(self.fields.shape)
        self.parse_fields()

    def neighbours(self, point):
        n, m = self.image.shape[:2]
        x, y = point
        for dx, dy in zip([-1, 0, 1, 0], [0, 1, 0, -1]):
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= n or ny < 0 or ny >= m:
                    continue
                yield nx, ny

    def parse_fields(self):
        n, m = self.image.shape[:2]
        processed = {(0, 0)}
        outside = deque([(0, 0)])
        walls_doors = []
        while len(outside) > 0:
            x, y = outside.popleft()
            self.fields[x, y] = Field.OUTSIDE
            for nx, ny in self.neighbours((x, y)):
                if (nx, ny) not in processed and \
                        np.all(self.image[nx, ny] == self.image[x, y]):
                    outside.append((nx, ny))
                    processed.add((nx, ny))
                elif np.any(self.image[nx, ny] != self.image[x, y]):
                    walls_doors.append((nx, ny))
        colours = {tuple(self.image[x, y]) for x, y in walls_doors}

        print(colours)
        if self.origin == 'Antonio':
            rmap = {(34, 177, 76): Field.DOOR,
                    (255, 255, 255): Field.WALL,
                    # also outside, but already done
                    (0, 0, 0): Field.INSIDE,
                    }
            cmap = {rmap[b]: b for b in rmap}
            cmap[Field.OUTSIDE] = (0, 0, 0)

            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    el = tuple(self.image[x, y])
                    if el in rmap and self.fields[x,y] == Field.UNPROCESSED:
                        self.fields[x, y] = rmap[el]
                    elif el not in rmap:
                        print("Unknown field at ({}, {}) with value {}.".format(x, y, el))


if __name__ == '__main__':
    r1 = 'buildings/export2.png'
    bdg = Building(r1)
    plt.imshow(bdg.fields)
    plt.show()
