-- Nombre d'hôtel dans une ville donnée
SELECT v.id, v.nom_ville, COUNT(*) AS Nbr_hotel FROM ville v
JOIN hotel h ON h.ville_id=v.id GROUP BY ville_id ORDER BY Nbr_hotel, v.id;

-- Nombre spectacle dans une ville donnée
SELECT v.id, v.nom_ville, COUNT(*) AS Nbr_spectacle FROM ville v
JOIN spectacle s ON s.ville_id=v.id GROUP BY ville_id ORDER BY Nbr_spectacle, v.id;

-- Liste des hôtels ayant des chambres non disponibles;
SELECT id AS id_hotel, nbr_room,
	CASE 
		WHEN hr.etat="Oc" 
		THEN "Tout occupe" 
	END AS etat
FROM (SELECT nbr_room, id, ville_id FROM hotel) AS h 
JOIN (SELECT COUNT(*) AS room_dispo, hotel_id, etat FROM hotel_room 
WHERE etat="Oc" GROUP BY hotel_id) AS hr 
ON hr.hotel_id=h.id WHERE h.nbr_room=hr.room_dispo;

-- Liste des hôtels ayant des chambres disponibles;
-- Cela est vérifié lorsqu'il y'a au moins une chambre de l'hôtel cible dont l'état = "Li"
SELECT h.id AS hotel, h.nbr_room AS Nbr_Total_Chambre, COUNT(*) Nbr_Chambre_Dispo
FROM hotel h
JOIN hotel_room hr ON h.id=hr.hotel_id
WHERE hr.etat="Li"
GROUP BY h.id;

-- Distances entre hotel et spectacle
SELECT h.id AS hotel, s.id as spectacle, 
	CASE
		WHEN s.ville_id = h.ville_id THEN
			ROUND(SQRT(POWER(s.loc_X - h.loc_X, 2) + POWER(s.loc_Y - h.loc_Y, 2)), 1)
		ELSE ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + d.dist, 1)
	END AS "Distance",
	CASE
		WHEN s.ville_id = h.ville_id THEN
			1
		ELSE 2
	END AS "Verif"
FROM distance d 
JOIN ville v1 ON d.id_ville1=v1.id
JOIN ville v2 ON d.id_ville2=v2.id
JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id 
GROUP BY h.id, s.id, Distance order by h.id, s.id;

-- Distances entre hotel et hotel
SELECT h.id AS hotel, h2.id AS another_hotel, 
	CASE
		WHEN h.ville_id = h2.ville_id THEN
			ROUND(SQRT(POWER(h.loc_X - h2.loc_X, 2) + POWER(h.loc_Y - h2.loc_Y, 2)), 1)
		ELSE ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(h2.loc_X, 2) + POWER(h2.loc_Y, 2)) + d.dist, 1)
	END AS "Distance",
	CASE
		WHEN h.ville_id = h2.ville_id THEN
			1
		ELSE 2
	END AS "Verif"
FROM distance d
JOIN ville v1 ON d.id_ville1=v1.id
JOIN ville v2 ON d.id_ville2=v2.id
JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
JOIN (SELECT id, ville_id, loc_X, loc_Y FROM hotel) AS h2 ON v1.id=h2.ville_id OR v2.id=h2.ville_id
GROUP BY h.id, h2.id, Distance order by h.id, h2.id;

-- Spectacles qui auront lieu un jour donné
SELECT s.id, s.name, s.categorie_spectacle FROM spectacle s
WHERE s.date_spectacle="2024-03-05 21:15:00";


-- Distances entre spectacle et spectacle
SELECT s.id AS spectacle, s2.id AS another_spectacle, 
	CASE
		WHEN s.ville_id = s2.ville_id THEN
			ROUND(SQRT(POWER(s.loc_X - s2.loc_X, 2) + POWER(s.loc_Y - s2.loc_Y, 2)), 1)
		ELSE ROUND(SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + SQRT(POWER(s2.loc_X, 2) + POWER(s2.loc_Y, 2)) + d.dist, 1)
	END AS "Distance",
	CASE
		WHEN s.ville_id = s2.ville_id THEN
			1
		ELSE 2
	END AS "Verif"
FROM distance d
JOIN ville v1 ON d.id_ville1=v1.id
JOIN ville v2 ON d.id_ville2=v2.id
JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id
JOIN (SELECT id, ville_id, loc_X, loc_Y FROM spectacle) AS s2 ON v1.id=s2.ville_id OR v2.id=s2.ville_id
GROUP BY s.id, s2.id, Distance order by s.id, s2.id;


-- Les spectacle et d'hôtel se trouvant dans la même ville  &&  Les spectacles qui ont lieu dans une ville
SELECT s.hotel, s.spectacle, s.Distance FROM (SELECT h.id AS hotel, s.id as spectacle,
	CASE
		WHEN s.ville_id = h.ville_id THEN
			ROUND(SQRT(POWER(s.loc_X - h.loc_X, 2) + POWER(s.loc_Y - h.loc_Y, 2)), 1)
		ELSE ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + d.dist, 1)
	END AS "Distance",
	CASE
		WHEN s.ville_id = h.ville_id THEN
			1
		ELSE 2
	END AS "Verif", h.ville_id as hotelvid, s.ville_id AS specvid
FROM distance d 
JOIN ville v1 ON d.id_ville1=v1.id
JOIN ville v2 ON d.id_ville2=v2.id
JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id 
GROUP BY h.id, s.id, Distance order by h.id, s.id) AS s WHERE Verif=1;

--1 hôtels ayant une distance inférieure à 5km par rapport au lieu d'un spectacle définit
SELECT pos.spectacle, pos.hotel, pos.Distance FROM 
(SELECT h.id AS hotel, s.id as spectacle, s.date_spectacle,
	CASE
		WHEN s.ville_id = h.ville_id THEN
			ROUND(SQRT(POWER(s.loc_X - h.loc_X, 2) + POWER(s.loc_Y - h.loc_Y, 2)), 1)
		ELSE 
			ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + d.dist, 1)
	END AS "Distance"
FROM distance d 
JOIN ville v1 ON d.id_ville1=v1.id
JOIN ville v2 ON d.id_ville2=v2.id
JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id 
GROUP BY h.id, s.id, Distance order by h.id, s.id) AS pos 
WHERE pos.Distance<5000 AND pos.spectacle=3
GROUP BY pos.spectacle, pos.hotel, pos.Distance;


--2 Les hôtels complets de la ville VVVV à la date dddd.
SELECT h.id AS id_hotel, nbr_room, h.ville_id,
	CASE 
		WHEN hr.etat="Oc" 
		THEN "Tout occupe" 
	END AS etat
FROM (SELECT nbr_room, id, ville_id FROM hotel) AS h 
JOIN (SELECT COUNT(*) AS room_dispo, hotel_id, etat FROM hotel_room 
WHERE etat="Oc" GROUP BY hotel_id) AS hr 
ON hr.hotel_id=h.id
WHERE h.nbr_room=hr.room_dispo AND h.ville_id=2 AND date_reservation_debut={}; -- 12:  13  2



--3 L'hôtel (les hôtels) qui a la chambre la moins chère disponible à la date ddddd dans la ville VVVVVV.
SELECT h.id, h.name FROM ville v
JOIN hotel h ON v.id = h.ville_id
JOIN hotel_room hr ON hr.hotel_id=h.id
WHERE v.id = 12 AND
hr.prix=(SELECT MIN(prix) FROM hotel_room hr JOIN hotel h ON h.id=hr.hotel_id)
AND NOT EXISTS (SELECT r.room_id FROM reservation r JOIN hotel_room hr ON
r.room_id=hr.id AND ‘ddddd’ BETWEEN r.date_reservation_debut AND r.date_reservation_fin);

-- les hotels dans une ville donnée ayant chambre moins cher
SELECT tab_p.ville_id As ville_id, tab_p.name AS 'Nom hotel', CONCAT_WS("", MIN(tab_p.prix), " £") AS prix_chambre_moins_cher FROM 
(SELECT h.name, v.nom_ville, v.id AS ville_id, hr.prix, hr.id 
FROM hotel h JOIN ville v ON h.ville_id=v.id
JOIN hotel_room hr ON hr.hotel_id=h.id
WHERE v.id=1 AND hr.categorie='C' AND hr.etat='Li') tab_p GROUP BY tab_p.name, tab_p.ville_id;

-- Nombre d'hotel dans une ville donnée
select v.nom_ville, v.id, count(*) as Nbr_hotel from ville v join hotel h on h.ville_id=v.id group by ville_id order
by Nbr_hotel;

--4 La ville proposant le séjour de trois jours le plus cher ; ici, séjour veut dire 2 nuits d'hôtel avec spectacles chaque soirée 
--  précédant les 2 nuitées, le tout dans la même ville.
SELECT S.id, S.ville, S.prix_sejour_3_jour
FROM (SELECT v.id, v.nom_ville AS ville, SUM(hr.prix)*2+SUM(ts.prix) AS prix_sejour_3_jour
FROM ville v
JOIN hotel h ON h.ville_id=v.id
JOIN hotel_room hr ON hr.hotel_id=h.id
JOIN reservation r ON r.room_id=hr.id 
JOIN spectacle s ON s.ville_id=v.id
JOIN ticket_spectacle ts ON ts.spectacle_id=s.id WHERE r.date_reservation_fin-r.date_reservation_debut=3
AND s.date_spectacle BETWEEN r.date_reservation_debut AND r.date_reservation_fin
GROUP BY v.nom_ville, v.id) AS S
ORDER BY S.prix_sejour_3_jour DESC
LIMIT 1;


--5 les clients qui ont réservé pour au moins 600 Eur au total, et qui ne dépensent jamais moins de 100 Eur par nuit d'hôtel .
SELECT P.id, P.name_client, P.nbr_reserv, CONCAT_WS(' ', P.prix_sejour, '£') AS prix_sejour FROM (SELECT c.id, 
CONCAT_WS(' ', c.prenom, c.nom) AS name_client,
COUNT(r.client_id) AS nbr_reserv, SUM(hr.prix) AS prix_sejour
FROM client c JOIN reservation r ON r.client_id = c.id 
JOIN hotel_room hr ON r.room_id = hr.id
GROUP BY c.id, CONCAT_WS(' ', c.prenom, c.nom)) AS P

JOIN (SELECT r.room_id, r.client_id, hr.prix FROM client c 
JOIN reservation r ON r.client_id = c.id 
JOIN hotel_room hr ON r.room_id = hr.id
GROUP BY r.room_id, r.client_id) AS ch ON ch.client_id = P.id

WHERE P.prix_sejour >=600 AND ch.prix>100
GROUP BY P.id, P.name_client, P.nbr_reserv, P.prix_sejour;
