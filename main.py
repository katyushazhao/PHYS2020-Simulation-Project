import matplotlib.pyplot as plt
import numpy as np
import random

import matplotlib.animation as animation

class particle:
	'''A particle is a circle with position, velocity and radius.'''
	def __init__(self, x, y, dx, dy, r=0.01, c = 'black', f = False):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.color = c
		self.radius = r
		self.fill = f

	def draw(self, ax):
		'''Draw onto graph'''
		circle = plt.Circle((self.x,self.y),self.radius, color = self.color, fill = self.fill)
		ax.add_patch(circle)

	def collision(self, molecule):
		'''Have I hit another molecule'''
		return np.linalg.norm(np.subtract((self.x,self.y),(molecule.x,molecule.y))) < self.radius + molecule.radius
	
	def boundary(self):
		'''Bounce off wall'''
		if self.x - self.radius <0:
			self.x = self.radius
			self.dx = -self.dx
		if self.x + self.radius >1:
			self.x = 1-self.radius
			self.dx = -self.dx
		if self.y - self.radius <0:
			self.y = self.radius
			self.dy = -self.dy
		if self.y - self.radius >1:
			self.y = 1-self.radius
			self.dy = -self.dy

class animation:
	'''The animation'''
	def __init__(self, n):
		self.number = n
	
	def drawParticles(self, ax):
		molecules = np.ndarray((self.number,),dtype=object)
		dx = 0
		dy = 0
		for i in range(self.number):
			x = random.random()*(0.98)+0.01
			y = random.random()*(0.98)+0.01
			molecules[i]=particle(x,y,dx,dy)
		for molecule in molecules:
			for other in molecules:
				if molecule.collision(other) and molecule != other:
					del molecule
					break
			try:
				particle.draw(molecule, ax)
			except UnboundLocalError:
				pass


fig, ax = plt.subplots()
ani = animation(100)
ani.drawParticles(ax)
fig.savefig('animation.png')