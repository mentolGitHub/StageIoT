%% Une implémentation (basique) du filtrage de Kalman

function [xest, Pest, K, xap] = kalman(z, F, H, Q, R, x0, P0, delta_x, Pdx)

%% filtrage de Kalman
% z observations
% F matrice d'évolution du système
% H matrice d'observation
% Q covariance du bruit de modèle
% R covariance du bruit de mesure
% x0 état initial
% P0 covariance de l'estimation initiale
% delta_x (optionnel, 0 par défaut) mise à jour de l'état supposée connue
% Pdx sa covariance


%% implémentation du filtre de Kalman à fins pédagogiques uniquement
% les questions numériques d'implémentations sont laissées de côté

L = size(F, 1); % taille du vecteur d'état
[M, N] = size(z); % taille des observations et longueur de la séquence

xest = zeros(L, N); % estimation de l'état

Pest = zeros(L, L, N); % covariance de l'erreur d'estimation

xap = zeros(L, N); % estimation de l'état

Pap = zeros(L, L, N); % covariance de l'erreur d'estimation

K = zeros(L, M, N); % gains de Kalman

if (~exist('delta_x', 'var'))
    delta_x = zeros(L, N);
    Pdx = zeros(L, L);

end

% première itération
    xap(:, 1) = F * x0 + delta_x(:, 1);  % estimation a priori de l'état (utilisation du modèle)
    Pap(:, :, 1) = F * P0 * F' + Q + Pdx;  % covariance de l'estimation a priori

    innov = z(:, 1) - H * xap(:, 1);  % innovation
    S = H * Pap(:, :, 1) * H' + R;
    K(:, :, 1) = Pap(:, :, 1) * H' * inv(S); % gain de Kalman

    xest(:, 1) = xap(:, 1) + K(:, :, 1) * innov;  % correction de l'estimation a posteriori
    Pest(:, :, 1) = (eye(L) - K(:, :, 1)*H) * Pap(:, :, 1);  % mise à jour de la covariance de l'estimation


for u=2:N

    xap(:, u) = F * xest(:, u-1) + delta_x(:, u);  % estimation a priori de l'état (utilisation du modèle)
    Pap(:, :, u) = F * Pest(:, :, u-1) * F' + Q;  % covariance de l'estimation a priori

    innov = z(:, u) - H * xap(:, u);  % innovation
    S = H * Pap(:, :, u) * H' + R;
    K(:, :, u) = Pap(:, :, u) * H' * inv(S); % gain de Kalman

    xest(:, u) = xap(:, u) + K(:, :, u) * innov;  % correction de l'estimation a posteriori
    Pest(:, :, u) = (eye(L) - K(:, :, u)*H) * Pap(:, :, u);  % mise à jour de la covariance de l'estimation


end

end
