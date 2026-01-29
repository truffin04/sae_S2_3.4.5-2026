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



INSERT INTO utilisateur (login,email,nom,password,role)
VALUES ('client1',NULL,
        NULL,
        'pbkdf2:sha256:1000000$fAvViQy457fTur0F$c3db8906c14da1af31fd17fae585c2f59b1dcc1a73ca754d58952dff10e0c4cc'
        ,'ROLE_client'
        ),
        ('client2',
           NULL,
           NULL,
           'pbkdf2:sha256:1000000$3WHRHX5U6wMYkJZj$7bc4cbcc391a299d9e14cf2efa4fb2df249464de3b7afe889baa4b78d3f5df3f'
        ,'ROLE_client');


INSERT INTO chaussure (id_chaussure, nom_chaussure, sexe, entretien, prix_chaussure, pointure_id, type_chaussure_id, fournisseur, marque, photo, stock)
VALUES (NULL,BasketViolette,femme,neuf,79.99,8,1,BFl,NILE,basket_f_violette_rose.jpg,50),
       (NULL,BasketAd, homme , neuf,49.99,6,1,BFL,Laco,basket_h_addidas.png,5),
       (NULL,BasketUni, unisex, neuf, 99.99,6,1,BFL,uni,basket_uni_blanche_noire.png,6),
       (NULL,BasketRose, femme, neuf,74.99,8,1,BFl,Laco,baskets_f_rose.jpg,4),
       (NULL,BotteMaron,femme,neuf,64.99,8,2,BOFL,bolt,botte_f_marron.jpg,7),
       (NULL,botteneuniBrune,unisex,neuf,74.99,6,2,BOLF,bolt,botte_uni_brune.png,3),
       (NULL,ChaussureClasN,femme,neuf,566.99,8,3,CHL,conver,chaussure_classique_f_noire.png,9),
       (NULL,ChaussureClasR,femme,neuf,249.99,8,3,CHL,conver,chaussure_classique_f_rouge.png,14),
       (NULL,ChaussureClasB,homme,neuf,290.99,6,3,CHL,conver,chaussure_classique_h_brune.png,25),
       (NULL,ChaussureCLassMF,homme,neuf,229.99,6,3,CHL,conver,chaussure_classique_h_maron_foncée.png,18),
       (NULL,ChaussureVilleN,femme,neuf,98.99,8,4,VHL,villy,chaussure_de_ville_f_noire.png,12),
       (NULL, ChaussureRandoR,femme,neuf,99.99,8,5,RHL,randim,chaussure_rando_f_rose.png,26),
       (NULL,ChaussureRandoN,homme,neuf,89.99,6,5,RHL,randim,chaussure_rando_h_noire.png,2),
       (NULL,ChaussureVilleB,unisex,neuf,79.69,6,4,VHL,villy,chaussure_ville_uni_bleue.png,41),
       (NULL,ChaussureVilleO,unisex,neuf,69.99,6,4,VHL,villy,chaussure_ville_uni_orange.png,9);


INSERT INTO pointure (id_pointure, libelle_pointure)
VALUES
    (NULL,45),
    (NULL,44),
    (NULL,43),
    (NULL,42),
    (NULL,41),
    (NULL,40),
    (NULL,39),
    (NULL,38),
    (NULL,37),
    (NULL,36),
    (NULL,35);

INSERT INTO type_chaussure (id_type_chaussure, libelle_type_chaussure)
VALUES (NULL,basket),
       (NULL,botte),
       (NULL,classique),
       (NULL,ville),
       (NULL,rando);

INSERT INTO ligne_commande (commande_id, chaussure_id, prix, quantite)
VALUES (NULL,NULL,64.99,1),
       (NULL,10,229.99,1);

INSERT INTO ligne_panier (utilisateur_id, chaussure_id, quantite, date_ajout)
VALUES (NULL,NULL,5,12/01/2026),
       (NULL,NULL,15,25/10/2025);







