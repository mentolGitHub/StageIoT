DROP TABLE IF EXISTS `Users`;

CREATE TABLE `Users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `role` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Data`;

CREATE TABLE `Data` (
    `id` int NOT NULL AUTO_INCREMENT,
    `date` datetime NOT NULL,
    `temperature` float NOT NULL,
    `humidity` float NOT NULL,
    `luminosity` float NOT NULL,
    `presence` tinyint(1) NOT NULL,
    `user_id` int(11) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `Users` (`id`, `username`, `password`, `email`, `role`) VALUES (1, 'admin', 'admin', '', 'admin');