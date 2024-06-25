DROP TABLE IF EXISTS 'Users';

CREATE TABLE 'Users' (
    'id' int NOT NULL AUTO_INCREMENT,
    'username' varchar(255) NOT NULL,
    'password' varchar(255) NOT NULL,
    'email' varchar(255) NOT NULL,
    'role' varchar(255) NOT NULL,
    PRIMARY KEY ('id')
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS 'Data';

CREATE TABLE 'Data' (
    'timestamp' datetime2 NOT NULL,
    'temperature' float,
    'humidity' float,
    'luminosity' float,
    'presence' tinyint(1),
    'pression' float,
    'longitude' ,
    'latitude' ,
    'altitude' ,
    'angle' ,
    'vitesse angulaire X' ,
    'vitesse angulaire Y' ,
    'vitesse angulaire Z' ,
    'azimut' ,
    'distance recul' float,
    'humidite'

    
    PRIMARY KEY ('timestamp')
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO 'Users' ('id', 'username', 'password', 'email', 'role') VALUES (1, 'admin', 'admin', '', 'admin');