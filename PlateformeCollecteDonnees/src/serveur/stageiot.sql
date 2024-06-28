#DROP TABLE IF EXISTS `Users`;


CREATE TABLE IF NOT EXISTS `Users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `role` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


#DROP TABLE IF EXISTS `Data`;

CREATE TABLE IF NOT EXISTS `Data` (
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
    `distance_recul` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `Users` (`id`, `username`, `password`, `email`, `role`) VALUES (1, `admin`, `admin`, ``, `admin`);