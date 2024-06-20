import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

class particle:
	'''A particle is a circle with position, velocity and radius.'''
	def __init__(self, x, y, dx, dy, r=0.01, c = 'black', f = False):
		circle = plt.Circle((x,y),r, color = c, fill = f)
		ax.add_patch(circle)