import numpy as np
x = np.linspace(-0.5, 0.5, 100)
y = np.linspace(-0.5, 0.5, 100)
sum = 0
G = 1e9
n = 0
msk = [1, n for i in range(98), 1]

for i in range(100):
    for j in range(100):
        sum += x[i]**2 + y[j]**2 * G * msk[i][j]
print(sum)