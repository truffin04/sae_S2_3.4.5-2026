DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS chaussure;
DROP TABLE IF EXISTS pointure;
DROP TABLE IF EXISTS type_chaussure;
DROP TABLE IF EXISTS etat;

CREATE TABLE utilisateur(
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT ,
    login VARCHAR(20),
    email VARCHAR(100),
    nom varchar(256),
    password VARCHAR(1000),
    role VARCHAR(20)
);
CREATE TABLE etat(
    id_etat INT PRIMARY KEY AUTO_INCREMENT,
    libelle VARCHAR(20)
);

CREATE TABLE commande(
    id_commande INT PRIMARY KEY AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    constraint fk_utilisateur
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    constraint fk_etat
        FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
);




-- chaussure(id_chaussure, nom_chaussure, sexe, entretien, prix_chaussure, pointure_id, type_chaussure_id, fournisseur, marque, photo, stock )
-- pointure (id_pointure, libelle_pointure)
-- type_chaussure (id_type_chaussure, libelle_type_chaussure)

CREATE TABLE pointure(
    id_pointure INT PRIMARY KEY AUTO_INCREMENT,
    libelle_pointure VARCHAR(128)
);

CREATE TABLE type_chaussure(
    id_type_chaussure INT PRIMARY KEY AUTO_INCREMENT,
    libelle_type_chaussure VARCHAR(128)
);

CREATE TABLE chaussure(
    id_chaussure INT PRIMARY KEY AUTO_INCREMENT,
    nom_chaussure VARCHAR(64),
    sexe VARCHAR(5),
    entretien VARCHAR(20),
    prix_chaussure NUMERIC(10,2),
    pointure_id INT,
    type_chaussure_id INT,
    fournisseur VARCHAR(100),
    marque VARCHAR(30),
    photo VARCHAR(256),
    stock INT,
    constraint fk_type_chaussure
        foreign key (type_chaussure_id) REFERENCES type_chaussure(id_type_chaussure),
    constraint fk_pointure
        foreign key (pointure_id) REFERENCES pointure(id_pointure)
);

CREATE TABLE ligne_commande(
    commande_id INT,
    chaussure_id INT,
    prix NUMERIC(10,2),
    quantite INT,
    constraint fk_commande
        FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    constraint fk_chaussure
        FOREIGN KEY (chaussure_id) REFERENCES chaussure(id_chaussure),
    PRIMARY KEY (commande_id,chaussure_id)

);

CREATE TABLE ligne_panier(
    utilisateur_id INT,
    chaussure_id INT,
    quantite INT,
    date_ajout date,
    constraint fk_utilisateur_panier
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    constraint fk_chaussure_panier
        FOREIGN KEY (chaussure_id) REFERENCES chaussure(id_chaussure),
    PRIMARY KEY (utilisateur_id,chaussure_id)

);





