-- DROP TABLE IF EXISTS Auth_Token;
-- DROP TABLE IF EXISTS Data;
-- DROP TABLE IF EXISTS DeviceOwners;
-- DROP TABLE IF EXISTS Device;
-- DROP TABLE IF EXISTS Users;
-- DROP TABLE IF EXISTS Obstacles;

CREATE TABLE IF NOT EXISTS Device (
    `dev-eui` varchar(255) NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `status` varchar(255) NOT NULL DEFAULT 'public',
    `description` varchar(500) DEFAULT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS Users (
    `username` varchar(255) PRIMARY KEY NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(255),
    `role` varchar(255) NOT NULL DEFAULT 'user',
    `api-key` varchar(255)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS DeviceOwners (
    `id` serial,
    `owner` varchar(255) NOT NULL,
    `device` varchar(255) NOT NULL,
    `super-owner` tinyint(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (`owner`) REFERENCES Users(`username`),
    FOREIGN KEY (`device`) REFERENCES Device(`dev-eui`)
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



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
    `distance_recul` float DEFAULT NULL,
    `source` varchar(255) NOT NULL,
    FOREIGN KEY (`source`) REFERENCES Device (`dev-eui`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Auth_Token (
    `token` varchar(255) PRIMARY KEY,
    `user` varchar(255) NOT NULL,
    `date-exp` DATETIME(3) NOT NULL,
    FOREIGN KEY (`user`) REFERENCES Users(`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Objets (
    `ìd` serial,
    `timestamp` DATETIME(3) NOT NULL,
    `eui` varchar(255) NOT NULL,
    `x` float NOT NULL,
    `y` float NOT NULL,
    `z` float NOT NULL,
    `label` varchar(255) NOT NULL,
    FOREIGN KEY (`eui`) REFERENCES Device (`dev-eui`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




INSERT INTO Users (username, password, role) VALUES ('a', '$2b$12$MF83CvvYYxd6QSOb4SPm4.m4PXghwwRncpURAro7sfs2AAkZ6ORuW', 'admin');

--   Ajout Capteur   --
--   Creer une nouvelle table pour les capteurs --
--   Pour plus de fonctionnalitées, il est possible de rajouter des colonnes dans la table Data   --


-- Fin ajout Capteur --
