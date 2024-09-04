%% Suivi de véhicule

%% Définition du modèle
% On construit le modèle à partir du modèle continu.
% L'état contient position et vitesse dans les deux directions
% On suppose un bruit de modèle sur la vitesse uniquement

dt = 1; % pas de temps


dF = [0 0 1 0; 0 0 0 1;0 0 0 0;0 0 0 0]; % matrice du système linéaire d'eq. diffs

F = expm(dF*dt); % matrice du modèle discret

sigma_q = 0.05;
Q = sigma_q^2 * [0 0 0 0;0 0 0 0;0 0 1 0;0 0 0 1];

% On mesure uniquement la position.

H = [1 0 0 0; 0 1 0 0];

sigma_r = 1;
R = eye(2) * sigma_r^2;

%% Génération des données

L = 40; % nombre d'échantillons


V = [2; 1]; % vitesse, supposée uniforme
x = V * (1:L); % position au cours du temps 

z = x + randn(2, L) * sigma_r; % position mesurée

%% Initialisation
% On initialise l'estimation de l'état en utilisant la première mesure pour
% la position, et 0 pour la vitesse.
% La covariance de l'estimation est prise égale à celle des mesures pour la
% position, et arbitrairement grande pour la vitesse.

X0 = [z(:, 1); 0 ; 0]; % première estimation de l'état
P0 = diag([sigma_r sigma_r 100 100]); % covariance de l'estimation 

%% Filtre de Kalman

[xest, Pest, K, xap] = kalman(z, F, H, Q, R, X0, P0); % Kalman


%% Visualisation des résultats
% Premières estimations de l'état
% En rouge les estimations, en vert les prédictions
% position réelles en bleu
% position mesurées en noir

figure
hold on
quiver(xest(1, 1:10), xest(2, 1:10), xest(3, 1:10), xest(4, 1:10), 'r', 'linewidth', 2, 'AutoScale', 'off');
quiver(xap(1, 2:11), xap(2, 2:11), xap(3, 2:11), xap(4, 2:11), 'g', 'linewidth', 2, 'AutoScale', 'off');
scatter(z(1, 2:11), z(2, 2:11), 30, 'k', 'filled');
scatter(x(1, 2:11), x(2, 2:11), 30, 'b', 'filled');



%% Visualisation des résultats
% Après une trentaine d'itérations, le filtre converge
% En rouge les estimations, en vert les prédictions
% position réelles en bleu
% position mesurées en noir

figure
hold on
quiver(xest(1, 30:39), xest(2, 30:39), xest(3, 30:39), xest(4, 30:39), 'r', 'linewidth', 2, 'AutoScale', 'off');
quiver(xap(1, 31:40), xap(2, 31:40), xap(3, 31:40), xap(4, 31:40), 'g', 'linewidth', 2, 'AutoScale', 'off');
scatter(z(1, 31:40), z(2, 31:40), 30, 'k', 'filled');
scatter(x(1, 31:40), x(2, 31:40), 30, 'b', 'filled');

