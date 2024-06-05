import dpkt
import socket
import random
import matplotlib.pyplot as plt

# Scatter plot
x = [random.random() for _ in range(0,100)]
y = [i*i for i in x]
plt.scatter(x,y,s=2)
plt.xlabel("x")
plt.ylabel("x^2")
plt.show()

# Line plot
x = [random.random() for _ in range(0,100)]
x.sort()
y = [i*i for i in x]
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("x^2")
plt.show()
