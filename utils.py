import numpy as np
import scipy.ndimage
from skimage import io

if __name__ == '__main__':
    img = scipy.ndimage.imread('buildings/export2.png')

    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            el = img[x, y, :3]
            if np.sum(el) > 600:
                img[x, y, :] = [255, 255, 255, 255]
            if np.all(el==[30,29,21]):
                img[x,y,:]= [255,255,255,255]
    
    io.imsave('buildings/export2.png', img)