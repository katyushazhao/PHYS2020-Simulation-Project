import os
import matplotlib.pyplot as plt
import numpy as np
import random
import imageio.v2 as imageio

class Particle:
    '''A particle is a circle with position, velocity and radius.'''
    def __init__(self, x, y, dx, dy, r=0.01, m=1, color='black', fill=False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = r
        self.fill = fill
        self.mass = m

    def draw(self, ax):
        '''Draw the particle on the graph'''
        circle = plt.Circle((self.x, self.y), self.radius, color=self.color, fill=self.fill)
        ax.add_patch(circle)

    def collision(self, other):
        '''Check if this particle collides with another'''
        return np.linalg.norm(np.subtract((self.x, self.y), (other.x, other.y))) < self.radius + other.radius
    
    def boundary(self):
        '''Bounce off the walls of the unit square'''
        if self.x - self.radius < 0:
            self.x = self.radius
            self.dx = -self.dx
        if self.x + self.radius > 1:
            self.x = 1 - self.radius
            self.dx = -self.dx
        if self.y - self.radius < 0:
            self.y = self.radius
            self.dy = -self.dy
        if self.y + self.radius > 1:
            self.y = 1 - self.radius
            self.dy = -self.dy

    def bounce(self, other):
        '''Elastic collision between this particle and another'''
        dist = np.linalg.norm(np.subtract((self.x, self.y), (other.x, other.y)))
        
        # Avoid division by zero and very small distances
        if dist < 1e-6:
            return
        
        # Calculate unit normal vector
        normal_vector = np.subtract((self.x, self.y), (other.x, other.y)) / dist
        
        # Relative velocity components in normal direction
        vself_n = np.dot((self.dx, self.dy), normal_vector)
        vother_n = np.dot((other.dx, other.dy), normal_vector)

        # Calculate new velocities in normal direction (1D elastic collision formula)
        self.dx, other.dx = (
            self.dx - (2 * other.mass / (self.mass + other.mass)) * vself_n * normal_vector[0],
            other.dx + (2 * self.mass / (self.mass + other.mass)) * vself_n * normal_vector[0]
        )
        self.dy, other.dy = (
            self.dy - (2 * other.mass / (self.mass + other.mass)) * vself_n * normal_vector[1],
            other.dy + (2 * self.mass / (self.mass + other.mass)) * vself_n * normal_vector[1]
        )

        # Update positions to avoid overlap
        overlap = (self.radius + other.radius - dist) / 2
        self.x += overlap * normal_vector[0]
        self.y += overlap * normal_vector[1]
        other.x -= overlap * normal_vector[0]
        other.y -= overlap * normal_vector[1]

        # Ensure particles stay within bounds
        self.boundary()
        other.boundary()

class Frame:
    '''The animation frame'''
    def __init__(self, num_particles):
        self.num_particles = num_particles
        self.particles = []

        # Add a large particle (centered at 0.5, 0.5) with zero velocity (Brownian motion)
        center_particle = Particle(x=0.5, y=0.5, dx=0.0, dy=0.0, r=0.05, color='blue')
        self.particles.append(center_particle)

        # Add other particles with random initial conditions
        for _ in range(self.num_particles - 1):
            x = random.random() * 0.98 + 0.01
            y = random.random() * 0.98 + 0.01
            dx = (random.random() - 0.5) * 0.02
            dy = (random.random() - 0.5) * 0.02
            particle = Particle(x, y, dx, dy)
            self.particles.append(particle)

    def draw_particles(self, ax):
        '''Draw all particles onto the graph'''
        for particle in self.particles:
            particle.draw(ax)

    def update(self, ax):
        '''Update particles positions and velocities'''
        for particle in self.particles:
            for other in self.particles:
                if particle != other and particle.collision(other):
                    particle.bounce(other)
            particle.x += particle.dx
            particle.y += particle.dy

        # Draw updated particles on the graph
        self.draw_particles(ax)

def create_gif(path, frames):
    '''Create a GIF animation from saved frames'''
    images = []
    for i in range(frames):
        filename = os.path.join(path, f"{i}.png")
        images.append(imageio.imread(filename))
    imageio.mimsave("animation.gif", images, fps=10, loop=0)

# Simulation parameters
runs = 50

# Initialize the first frame
fig, ax = plt.subplots()
animation_frame = Frame(num_particles=100)
animation_frame.draw_particles(ax)
fig.savefig('0.png')
plt.close(fig)

# Generate frames for the animation
for t in range(1, runs):
    fig, ax = plt.subplots()
    animation_frame.update(ax)
    fig.savefig(f"{t}.png")
    plt.close(fig)

# Create the animated GIF from saved frames
create_gif(os.path.dirname(__file__), runs)
