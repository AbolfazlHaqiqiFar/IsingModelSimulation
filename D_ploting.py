import matplotlib.pyplot as plt

X, Y = [], []
for line in open('data.ising', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[1])
  Y.append(values[2])

plt.scatter(Y,X)
plt.ylabel('aveP')
plt.xlabel('temperature')
plt.show()