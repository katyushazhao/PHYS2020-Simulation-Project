import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

class particle:
	'''A particle is a circle with position, velocity and radius.'''
	def __init__(self, x, y, dx, dy, r=0.01, c = 'black', f = False):
		self.x = x
		self.y = y
		self.color = c
		self.radius = r
		self.fill = f

	def draw(self, ax):
		'''Draw onto graph'''
		circle = plt.Circle((self.x,self.y),self.radius, color = self.color, fill = self.fill)
		ax.add_patch(circle)

class animation:
	'''The animation'''
	def __init__(self):
		fig, ax = plt.subplots()
		molecule = particle(0.7,0.3,0,0)
		particle.draw(molecule, ax)
		fig.savefig('animation.png')

ani = animation()