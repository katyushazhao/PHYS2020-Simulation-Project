import matplotlib.pyplot as plt
import numpy as np
import random
import imageio.v2 as imageio
import os

import matplotlib.animation as animation

class particle:
	'''A particle is a circle with position, velocity and radius.'''
	def __init__(self, x, y, dx, dy, r=0.01, m=1,c = 'black', f = False):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.color = c
		self.radius = r
		self.fill = f
		self.mass = m

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

	def bounce(self, molecule):
		'''Elastic collision between two molecules'''
		dist = np.linalg.norm(np.subtract((self.x,self.y),(molecule.x,molecule.y)))
		vself = (self.dx,self.dy)
		vother = (molecule.dx,molecule.dy)
		posself = (self.x,self.y)
		posother = (molecule.x,molecule.y)
		(self.dx,self.dy) = np.subtract(vself, ((2*molecule.mass)/(self.mass+molecule.mass))*(np.dot(np.subtract(vself,vother),np.subtract(posself,posother))/(dist**2))*np.subtract(posself,posother))

class frame:
	'''The animation'''
	def __init__(self, n):
		self.number = n
		self.molecules = np.ndarray((n,),dtype=object)
	
	def drawParticles(self, ax):
		for i in range(self.number):
			x = random.random()*(0.98)+0.01
			y = random.random()*(0.98)+0.01
			dx = (random.random()-0.5)*0.02
			dy = (random.random()-0.5)*0.02
			self.molecules[i]=particle(x,y,dx,dy)
		for molecule in self.molecules:
			molecule.boundary()
			for other in self.molecules:
				if molecule.collision(other) and molecule != other:
					del molecule
					break
			try:
				particle.draw(molecule, ax)
			except UnboundLocalError:
				pass

	def update(self, ax):
		for molecule in self.molecules:
			molecule.boundary()
			for other in self.molecules:
				if molecule.collision(other) and molecule != other:
					molecule.bounce(other)
			molecule.x += molecule.dx
			molecule.y += molecule.dy
			particle.draw(molecule, ax)

def create_gif(path, frames):
	images = []
	for i in range(frames):
		filename = os.path.join(path,f"{i}.png")
		images.append(imageio.imread(filename))
	imageio.mimsave("animation.gif", images, duration=frames/5)

runs = 50
fig, ax = plt.subplots()
anime = frame(100)
anime.drawParticles(ax)
fig.savefig('0.png')
for t in range(runs-1):
	plt.clf()
	plt.close()
	fig, ax = plt.subplots()
	anime.update(ax)
	fig.savefig(str(t+1)+'.png')
	plt.close()
create_gif(os.path.dirname(__file__), runs)