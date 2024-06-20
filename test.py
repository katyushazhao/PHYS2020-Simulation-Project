import matplotlib.pyplot as plt

circle1 = plt.Circle((0.5,0.5),0.01, color = 'black', fill=False)
fig, ax = plt.subplots()
ax.add_patch(circle1)
fig.savefig('plotcircles.png')