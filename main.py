import matplotlib.pyplot as plt
import numpy as np
import random

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
	def __init__(self, n):
		self.number = n
	
	def drawParticles(self, ax):
		molecules = np.ndarray((self.number,),dtype=object)
		dx = 0
		dy = 0
		for i in range(self.number):
			x = random.random()
			y = random.random()
			molecules[i]=particle(x,y,dx,dy)
		for molecule in molecules:
			particle.draw(molecule, ax)


fig, ax = plt.subplots()
ani = animation(30)
ani.drawParticles(ax)
fig.savefig('animation.png')