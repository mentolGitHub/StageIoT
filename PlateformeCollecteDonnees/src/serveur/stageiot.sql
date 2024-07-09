-- DROP TABLE IF EXISTS Auth_Token;
-- DROP TABLE IF EXISTS Data;
-- DROP TABLE IF EXISTS DeviceOwners;
-- DROP TABLE IF EXISTS Device;
-- DROP TABLE IF EXISTS Users;

CREATE TABLE IF NOT EXISTS Device (
    `dev-eui` varchar(255) NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `status` varchar(255) NOT NULL DEFAULT 'public'
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




INSERT INTO Users (username, password, role) VALUES ('a', '$2b$12$MF83CvvYYxd6QSOb4SPm4.m4PXghwwRncpURAro7sfs2AAkZ6ORuW', 'admin');

-- renvoie les données entre 2 dates d'un device / d'une liste de device

-- Donne la liste des device au alentours (rayon a selectionner)

-- add user
-- INSERT INTO Users (username,password) VALUES (%s,%s)

-- verifier le mdp d'un user'
-- SELECT (password) FROM Users WHERE usename = %s;
