import random
import numpy as np
import numpy.linalg as alg
from matplotlib import pyplot as plt, quiver
from torch import scatter

def generation_mesures():
    Path="./Tests/filtrage kalman/"

    data = open(Path+"data.csv")

    gps= open(Path+"gps.csv",mode="w")
    speed_mesurement= open(Path+"speed_mesurement.csv",mode="w")
    for ligne in data:
        if ligne != "\n" and (ligne.find("POS,SPEED")!=0):
            l=ligne.split()
            [pos,speed]=l[0].split(",")
            delta_pos = random.gauss(mu=0.0, sigma=1.0)
            pos_gps= float(pos) + delta_pos
            gps.write(str(pos_gps)+"\n")
            delta_speed=random.gauss(mu=0.0, sigma=0.05)
            speed_mesured=float(speed)+delta_speed
            speed_mesurement.write(str(speed_mesured)+"\n")


            print(pos_gps,speed_mesured)


def parse(filename):
    Path="./Tests/filtrage kalman/"

    data = open(Path+filename)
    result=[]
    for ligne in data:
        if ligne != "\n":
            l=ligne.split()
            result.append(l[0].split(",")[0])
            


    return result


def kalman(z, F, H, Q, R, x0, P0, delta_x=0, Pdx=0):

    ## filtrage de Kalman
    # z observations
    # F matrice d'évolution du système
    # H matrice d'observation
    # Q covariance du bruit de modèle
    # R covariance du bruit de mesure
    # x0 état initial
    # P0 covariance de l'estimation initiale
    # delta_x (optionnel, 0 par défaut) mise à jour de l'état supposée connue
    # Pdx sa covariance


    ## implémentation du filtre de Kalman à fins pédagogiques uniquement
    # les questions numériques d'implémentations sont laissées de côté
    L = np.size(F, 1) # taille du vecteur d'état
    [M, N]=z.shape # taille des observations et longueur de la séquence
    
    
    
    xest = np.zeros((L, N)) # estimation de l'état
    Pest = np.zeros((L, L, N)) # covariance de l'erreur d'estimation

    xap = np.zeros((L, N)) # estimation de l'état

    Pap = np.zeros((L, L, N)) # covariance de l'erreur d'estimation

    K = np.zeros((L, M, N)) # gains de Kalman

    if (delta_x==0 and Pdx==0):
        delta_x = np.zeros((L, N))
        Pdx = np.zeros((L, L))


    # première itération
    xap[:, 0] = F * x0 + delta_x[:, 0]  # estimation a priori de l'état (utilisation du modèle)
    Pap[:, :, 0] = F * P0 * F.T + Q + Pdx  # covariance de l'estimation a priori

    innov = z[:, 0] - H * xap[:, 0]  # innovation
    S = H * Pap[:, :, 0] * H.T + R
    K[:, :, 0] = Pap[:, :, 0] * H.T * np.linalg.inv(S) # gain de Kalman

    xest[:, 0] = xap[:, 0] + K[:, :, 0] * innov  # correction de l'estimation a posteriori
    Pest[:, :, 0] = (np.eye(L) - K[:, :, 0]*H) * Pap[:, :, 0]  # mise à jour de la covariance de l'estimation


    for u in range(1,N):

        xap[:, u] = F * xest[:, u-1] + delta_x[:, u]  # estimation a priori de l'état (utilisation du modèle)
        Pap[:, :, u] = F * Pest[:, :, u-1] * F.T + Q  # covariance de l'estimation a priori

        innov = z[:, u] - H * xap[:, u]  # innovation
        S = H * Pap[:, :, u] * H.T + R
        K[:, :, u] = Pap[:, :, u] * H.T * np.linalg.inv(S) # gain de Kalman

        xest[:, u] = xap[:, u] + K[:, :, u] * innov  # correction de l'estimation a posteriori
        Pest[:, :, u] = (np.eye(L) - K[:, :, u]*H) * Pap[:, :, u]  # mise à jour de la covariance de l'estimation
    return [xest, Pest, K]




def filtre_kalman():
    speed_mesured=parse("speed_mesurement.csv")
    gps=parse("gps.csv")
    
    # On construit le modèle à partir du modèle continu.
    # L'état contient position et vitesse dans les deux directions
    # On suppose un bruit de modèle sur la vitesse uniquement

    dt = 1 # pas de temps


    dF = np.array([[0, 0, 1, 0],[ 0, 0, 0, 1],[0, 0, 0, 0],[0, 0, 0, 0]]) # matrice du système linéaire d'eq. diffs

    F = np.exp(dF*dt) # matrice du modèle discret
    
    sigma_q = 0.05
    
    Q = sigma_q**2 * np.array([[0 ,0, 0, 0],[0 ,0, 0, 0],[0, 0 ,1, 0],[0, 0, 0 ,1]])

    # On mesure uniquement la position.

    H = np.array([[1 ,0, 0, 0],[ 0, 1, 0, 0]])

    sigma_r = 1
    sigma_r2 = 0.3
    R = np.eye(2) * sigma_r**2

    ## Génération des données

    L = 40 # nombre d'échantillons


    V = np.array([[2],[ 1]]) # vitesse, supposée uniforme
    x = V * range(1,L+1) # position au cours du temps 

    z = x + np.array([[random.gauss(0, sigma_r),random.gauss(0, sigma_r2)] for i in range(1,L+1)]).T # position mesurée

    ## Initialisation
    # On initialise l'estimation de l'état en utilisant la première mesure pour
    # la position, et 0 pour la vitesse.
    # La covariance de l'estimation est prise égale à celle des mesures pour la
    # position, et arbitrairement grande pour la vitesse.

    X0 = np.array([[z[:, 0]],[ 0 ],[ 0]]) # première estimation de l'état
    P0 = np.diag(np.array([sigma_r, sigma_r, 100, 100])) # covariance de l'estimation 

    ## Filtre de Kalman

    [xest, Pest, K, xap] = kalman(z, F, H, Q, R, X0, P0) # Kalman
    
    quiver(xest[1, 1:10], xest[2, 1:10], xest[3, 1:10], xest[4, 1:10], 'r', 'linewidth', 2, 'AutoScale', 'off')
    quiver(xap[1, 2:11], xap[2, 2:11], xap[3, 2:11], xap[4, 2:11], 'g', 'linewidth', 2, 'AutoScale', 'off')
    scatter(z[1, 2:11], z[2, 2:11], 30, 'k', 'filled')
    scatter(x[1, 2:11], x[2, 2:11], 30, 'b', 'filled')

    plt.xlabel('iterations')
    plt.show()




def filtre_kalman_test():
    speed_mesured=parse("speed_mesurement.csv")
    gps=parse("gps.csv")
    dt = 1
    dF = np.array([[0, 0, 1, 0],[ 0, 0, 0, 1],[0, 0, 0, 0],[0, 0, 0, 0]]) # matrice du système linéaire d'eq. diffs
    F = np.exp(dF*dt) # matrice d'évolution, constante, pas d'évolution
    H = np.array([[1 ,0, 0, 0],[ 0, 1, 0, 0]]) # mesure directe de l'état
    L = len(gps)

    Q = sigmaq**2 # covariance du bruit de modèle
    R = sigmar**2 # covariance du bruit de mesure
    a= [gps,speed_mesured]
    print(a)
    [xest, Pest, K] = kalman(a, F, H, Q, R, a[0,0], R)
    Xe = [gps[0][0], *xest[0,:]]  # unpack both iterables in a list literal
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


filtre_kalman()