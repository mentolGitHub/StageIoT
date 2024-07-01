

DROP TABLE IF EXISTS DeviceOwners;
#Drop TABLE IF EXISTS Device;
DROP TABLE IF EXISTS Users;

#DROP TABLE IF EXISTS Data;

CREATE TABLE IF NOT EXISTS Device (
    `dev-eui` varchar(255) NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS Users (
    `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(255),
    `role` varchar(255) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS DeviceOwners (
    `id` serial,
    `owner` int NOT NULL,
    `device` varchar(255) NOT NULL,
    FOREIGN KEY (`owner`) REFERENCES Users(`id`),
    FOREIGN KEY (`device`) REFERENCES Device(`dev-eui`)
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



CREATE TABLE IF NOT EXISTS Data (
    `timestamp` DATETIME(3) PRIMARY KEY NOT NULL,
    `temperature` float DEFAULT NULL,
    `humidity` float DEFAULT NULL,
    `luminosity` float DEFAULT NULL,
    `presence` tinyint(1) DEFAULT NULL,
    `pression` float DEFAULT NULL,
    `gps` POINT DEFAULT NULL,
    `altitude` float DEFAULT NULL,
    `angle` float DEFAULT NULL,
    `vitesse_angulaire_X` float DEFAULT NULL,
    `vitesse_angulaire_Y` float DEFAULT NULL,
    `vitesse_angulaire_Z` float DEFAULT NULL,
    `acceleration_X` float DEFAULT NULL,
    `acceleration_Y` float DEFAULT NULL,
    `acceleration_Z` float DEFAULT NULL,
    `azimut` float DEFAULT NULL,
    `distance_recul` float DEFAULT NULL,
    `source` varchar(255) NOT NULL,
    FOREIGN KEY (`source`) REFERENCES Device (`dev-eui`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Users (username, password, role) VALUES ('admin', 'admin', 'admin');

# renvoie les données entre 2 dates d'un device / d'une liste de device

# Donne la liste des device au alentours (rayon a selectionner)

# add user
#INSERT INTO Users (username,password) VALUES (%s,%s)

# verifier le mdp d'un user'
#SELECT (password) FROM Users WHERE usename = %s;
