import random
import numpy as np
import numpy.linalg as alg

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


def kalman(z, F, H, Q, R, x0, P0, delta_x, Pdx):

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

    L = np.size(F, 1); # taille du vecteur d'état
    [M, N] = np.size(z); # taille des observations et longueur de la séquence

    xest = np.zeros(L, N); # estimation de l'état

    Pest = np.zeros(L, L, N); # covariance de l'erreur d'estimation

    xap = np.zeros(L, N); # estimation de l'état

    Pap = np.zeros(L, L, N); # covariance de l'erreur d'estimation

    K = np.zeros(L, M, N); # gains de Kalman

    if (~exist('delta_x', 'var')):
        delta_x = np.zeros(L, N)
        Pdx = np.zeros(L, L)


    # première itération
    xap[:, 1] = F * x0 + delta_x[:, 1];  # estimation a priori de l'état (utilisation du modèle)
    Pap[:, :, 1] = F * P0 * F.T + Q + Pdx;  # covariance de l'estimation a priori

    innov = z[:, 1] - H * xap[:, 1];  # innovation
    S = H * Pap[:, :, 1] * H.T + R
    K[:, :, 1] = Pap[:, :, 1] * H.T * np.inv(S); # gain de Kalman

    xest[:, 1] = xap[:, 1] + K[:, :, 1] * innov;  # correction de l'estimation a posteriori
    Pest[:, :, 1] = (np.eye(L) - K[:, :, 1]*H) * Pap[:, :, 1];  # mise à jour de la covariance de l'estimation


    for u in range(2,N+1):

        xap[:, u] = F * xest[:, u-1] + delta_x[:, u];  # estimation a priori de l'état (utilisation du modèle)
        Pap[:, :, u] = F * Pest[:, :, u-1] * F.T + Q;  # covariance de l'estimation a priori

        innov = z[:, u] - H * xap[:, u];  # innovation
        S = H * Pap[:, :, u] * H.T + R
        K[:, :, u] = Pap[:, :, u] * H.T * np.inv(S); # gain de Kalman

        xest[:, u] = xap[:, u] + K[:, :, u] * innov;  # correction de l'estimation a posteriori
        Pest[:, :, u] = (np.eye(L) - K[:, :, u]*H) * Pap[:, :, u];  # mise à jour de la covariance de l'estimation


    end

    end


def filtre_kalman():
    speed_mesured=parse("speed_mesurement.csv")
    gps=parse("gps.csv")
    
    # On construit le modèle à partir du modèle continu.
    # L'état contient position et vitesse dans les deux directions
    # On suppose un bruit de modèle sur la vitesse uniquement

    dt = 1 # pas de temps


    dF = np.array([[0, 0, 1, 0],[ 0, 0, 0, 1],[0, 0, 0, 0],[0, 0, 0, 0]]) # matrice du système linéaire d'eq. diffs

    F = np.expm(dF*dt) # matrice du modèle discret

    sigma_q = 0.05
    Q = sigma_q^2 * np.array([[0 ,0, 0, 0],[0 ,0, 0, 0],[0, 0 ,1, 0],[0, 0, 0 ,1]])

    # On mesure uniquement la position.

    H = np.array([[1 ,0, 0, 0],[ 0, 1, 0, 0]])

    sigma_r = 1
    R = np.eye(2) * sigma_r^2

    ## Génération des données

    L = 40 # nombre d'échantillons


    V = np.array([[2],[ 1]]) # vitesse, supposée uniforme
    x = V * range(1,L) # position au cours du temps 

    z = x + randn(2, L) * sigma_r # position mesurée

    ## Initialisation
    # On initialise l'estimation de l'état en utilisant la première mesure pour
    # la position, et 0 pour la vitesse.
    # La covariance de l'estimation est prise égale à celle des mesures pour la
    # position, et arbitrairement grande pour la vitesse.

    X0 = np.array([[z[:, 1]],[ 0 ],[ 0]]) # première estimation de l'état
    P0 = np.diag(np.array([sigma_r, sigma_r, 100, 100])) # covariance de l'estimation 

    ## Filtre de Kalman

    [xest, Pest, K, xap] = kalman(z, F, H, Q, R, X0, P0) # Kalman







filtre_kalman()