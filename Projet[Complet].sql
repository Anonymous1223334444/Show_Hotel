DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS hotel_room;
DROP TABLE IF EXISTS hotel;
DROP TABLE IF EXISTS ticket_spectacle;
DROP TABLE IF EXISTS spectacle ;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS distance;
DROP TABLE IF EXISTS ville;

CREATE TABLE client (
    id INT NOT NULL AUTO_INCREMENT,
    nom VARCHAR (255),
    prenom VARCHAR (255),
    PRIMARY KEY (id)
);

CREATE TABLE ville (
    id INT AUTO_INCREMENT,
    nom_ville VARCHAR (255),
    PRIMARY KEY (id)
);


CREATE TABLE distance ( 
    id_ville1 INT NOT NULL,
    id_ville2 INT NOT NULL,
    dist INT,
    PRIMARY KEY (id_ville1, id_ville2),
    FOREIGN KEY (id_ville1) REFERENCES ville(id),
    FOREIGN KEY (id_ville2) REFERENCES ville(id) 
);

------------------------ Création des tables caractéristiques de l'entité 'hôtel'

CREATE table hotel (
    id INT NOT NULL AUTO_INCREMENT,	-- Identifiant de l'hôtel
    name VARCHAR(255),			    -- Nom de l'hôtel pour faciliter la recherche client
    nbr_room INT NOT NULL,		    -- Nombre de chambre de l'hôtel
    ville_id INT,			        -- ville où il est basé
    loc_X INT,  			        -- sa location dans la ville suivant X
    loc_Y INT,  			        -- sa location dans la ville suivant Y
    PRIMARY KEY (id),			    -- la colonne id de hotel est unique
    FOREIGN KEY (ville_id) REFERENCES ville(id)
);

CREATE table hotel_room (
    id INT NOT NULL AUTO_INCREMENT,	-- Identifiant de la chambre
    categorie VARCHAR(255),		    -- categorie de la chambre. On va considérer les catégories luxe (Lu), middle (M) et cheap (C)
    prix INT NOT NULL,			    -- prix de la chambre
    etat VARCHAR(255),			    -- occupée (Oc) ou libre (Li)
    hotel_id INT NOT NULL,		    -- l'hôtel auquel la chambre appartient
    PRIMARY KEY (id),			    -- la colonne id de room est unique
    FOREIGN KEY (hotel_id) REFERENCES hotel(id) ON DELETE CASCADE  -- Une chambre a lieu d'être que dans un hôtel
);

CREATE table reservation (
    id INT NOT NULL AUTO_INCREMENT,	-- Identifiant de la réservation
    date_reservation_debut DATETIME,-- date pour laquelle on fait la réservation
    date_reservation_fin DATETIME,	-- date pour laquelle le séjour s'achêve
    room_id INT NOT NULL, 		    -- la chambre choisie pour la réservation
    client_id INT NOT NULL,		    -- id du client qui fait la réservation
    PRIMARY KEY (id),			    -- la colonne id de reservation est unique
    FOREIGN KEY (room_id) REFERENCES hotel_room(id) ON DELETE CASCADE,  -- chaque réservation contient au moins une chambre
    FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE  -- le client qui fait la réservation
);

------------------------ Création des tables caractéristiques de l'entité 'spectacle'
CREATE table spectacle (
    id INT NOT NULL AUTO_INCREMENT,	    -- Identifiant du spectacle
    name VARCHAR(255),			        -- Nom du spectacle
    nombre_place INT NOT NULL,          -- Nombre de place du spectacle donnée
    categorie_spectacle VARCHAR(255),	-- Type de spectacle (Théâtre, danse, cirque, cinéma, anime, concert, comédie, ...)
    ville_id INT,			            -- ville où il a lieu
    loc_X INT,  			            -- sa location dans la ville suivant X
    loc_Y INT,  			            -- sa location dans la ville suivant Y
    date_spectacle DATETIME,		    -- date où le spectacle a lieu
    PRIMARY KEY (id),			        -- la colonne id de spectacle est unique
    FOREIGN KEY (ville_id) REFERENCES ville(id)
);

CREATE table ticket_spectacle (
    id INT NOT NULL AUTO_INCREMENT,	-- Identifiant de l'achat d'un ticket
    prix INT NOT NULL,			    -- prix d'une place
    spectacle_id INT NOT NULL,		-- le spectacle pour lequel le ticket est acheté
    client_id INT NOT NULL,		    -- id du client qui achète le ticket
    etat VARCHAR(255),			    -- epuisé (E) ou restant (R)
    PRIMARY KEY (id),			    -- id de achat_tickets est unique
    FOREIGN KEY (spectacle_id) REFERENCES spectacle(id) ON DELETE CASCADE,  -- chaque achat de ticket est lié à un spectacle
    FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE         -- chaque achat de ticket est lié à un client
);

------------------------ Uploader nos données à partir de fichiers '.csv' stockés localement
SET GLOBAL local_infile = 'ON';
LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/client.csv'
                INTO TABLE client 
                FIELDS TERMINATED by ', '
                ENCLOSED BY '"' 
                LINES TERMINATED by '\n' (nom, prenom);

LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/ville.csv'
                INTO TABLE ville 
                FIELDS TERMINATED by ', '
                ENCLOSED BY '"' 
                LINES TERMINATED by '\n' (nom_ville);

LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/distance.csv'
                INTO TABLE distance 
                FIELDS TERMINATED by ', '
                ENCLOSED BY '"' 
                LINES TERMINATED by '\n' (id_ville1, id_ville2, dist);

LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/hotel.csv'
                INTO TABLE hotel 
                FIELDS TERMINATED by ', '
                ENCLOSED BY '"' 
                LINES TERMINATED by '\n' (name, nbr_room, ville_id, loc_X, loc_Y);

LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/hotel_room.csv'
                INTO TABLE hotel_room 
                FIELDS TERMINATED by ', ' 
                ENCLOSED BY '"' 
                LINES TERMINATED by '\n' (categorie, prix, etat, hotel_id);

LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/reservation.csv'
                INTO TABLE reservation
                FIELDS TERMINATED by ', ' 
                ENCLOSED BY '"' 
                LINES TERMINATED by '\n' (date_reservation_debut, date_reservation_fin, room_id, client_id);

LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/spectacle.csv'
                INTO TABLE spectacle 
                FIELDS TERMINATED by ', '
                ENCLOSED BY '"' 
                LINES TERMINATED by '\n' (name, categorie_spectacle, nombre_place, ville_id, loc_X, loc_Y, date_spectacle);

LOAD DATA LOCAL INFILE '/home/anonymous/Desktop/pro/data/ticket_spectacle.csv'
                INTO TABLE ticket_spectacle
                FIELDS TERMINATED by ', '
                ENCLOSED BY '"'
                LINES TERMINATED by '\n' (prix, spectacle_id, client_id, etat);

