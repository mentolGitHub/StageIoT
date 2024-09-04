-- DROP TABLE IF EXISTS Data;
-- DROP TABLE IF EXISTS Obstacles;


CREATE TABLE IF NOT EXISTS Data (
    `timestamp` DATETIME(3) PRIMARY KEY NOT NULL,
    `temperature` float DEFAULT NULL,
    `humidity` float DEFAULT NULL,
    `luminosity` float DEFAULT NULL,
    `presence` tinyint(1) DEFAULT NULL,
    `pression` float DEFAULT NULL,
    `longitude` float DEFAULT NULL,
    `latitude` float DEFAULT NULL,
    `altitude` float DEFAULT NULL,
    `angle` float DEFAULT NULL,
    `vitesse_angulaire_X` float DEFAULT NULL,
    `vitesse_angulaire_Y` float DEFAULT NULL,
    `vitesse_angulaire_Z` float DEFAULT NULL,
    `acceleration_X` float DEFAULT NULL,
    `acceleration_Y` float DEFAULT NULL,
    `acceleration_Z` float DEFAULT NULL,
    `azimuth` float DEFAULT NULL,
    `distance_recul` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Objets (
    `ìd` serial,
    `timestamp` DATETIME(3) NOT NULL,
    `eui` varchar(255) NOT NULL,
    `x` float NOT NULL,
    `y` float NOT NULL,
    `z` float NOT NULL,
    `label` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
