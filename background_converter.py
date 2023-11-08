import numpy as np
from PIL import Image

racetrack_image = Image.open('imgs\\racetrack.png')
racetrack_array = np.array(racetrack_image)
racetrack_binary = (racetrack_array!=0).all(axis=2) #white is 1, black is 0

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

black_points = np.argwhere(racetrack_binary==False)
print(black_points.shape)
# print(racetrack_binary[racetrack_binary].astype(np.uint8))
print(racetrack_binary.shape)
Image.fromarray(racetrack_binary).show() 
