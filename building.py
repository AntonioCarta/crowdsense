import numpy as np
import scipy.ndimage


class Building:
    def __init__(self, filename):
        self.image = scipy.ndimage.imread(filename)

    


if __name__=='__main__':
    r1 = 'buildings/export2.png'
    bdg = Building(r1)
