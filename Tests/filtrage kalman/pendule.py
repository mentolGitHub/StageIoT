import random
import numpy as np
from generation_mesures import kalman
from matplotlib import pyplot as plt

sigmaq = 0.001 # écart type du bruit de modèle
sigmar = 0.5 # écart type du bruit de mesure

F = np.eye(1) # matrice d'évolution, constante, pas d'évolution
H = np.eye(1) # mesure directe de l'état
Q = sigmaq**2 # covariance du bruit de modèle
R = sigmar**2 # covariance du bruit de mesure

L = 2000 # longueur de la séquence
z = 1 * np.ones((1, L)) + np.array([ random.gauss(0, sigmar) for i in range(1,L+1)]).T # constante + du bruit
a = z[:,1:]

[xest, Pest, K] = kalman(a, F, H, Q, R, z[0,0], R)
Xe = [z[0][0], *xest[0,:]]  # unpack both iterables in a list literal
print(Xe[0:10])

b =2*np.sqrt(np.squeeze(Pest))
T= [2 * np.sqrt(R) ,*b[:]]
print(len(Xe))
print(len(T))
plt.errorbar(range(1,L+1),Xe, T)



plt.plot(np.ones((L,1)))
plt.scatter(range(1,L+1),z)

plt.xlabel('iterations')
plt.show()
