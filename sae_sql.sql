    DROP TABLE IF EXISTS note;
    DROP TABLE IF EXISTS commentaire;
    DROP TABLE IF EXISTS ligne_panier;
    DROP TABLE IF EXISTS ligne_commande;
    DROP TABLE IF EXISTS commande;
    DROP TABLE IF EXISTS adresse;
    DROP TABLE IF EXISTS declinaison_chaussure;
    DROP TABLE IF EXISTS taille;
    DROP TABLE IF EXISTS couleur;
    DROP TABLE IF EXISTS chaussure;
    DROP TABLE IF EXISTS type_chaussure;
    DROP TABLE IF EXISTS etat;
    DROP TABLE IF EXISTS utilisateur;

    CREATE TABLE utilisateur(
        id_utilisateur INT PRIMARY KEY AUTO_INCREMENT ,
        login VARCHAR(20),
        email VARCHAR(100),
        nom varchar(256),
        password VARCHAR(1000),
        role VARCHAR(20)
    );

    create table adresse (
    id_adresse int primary key auto_increment,
    nom varchar(255),
    rue varchar(255),
    code_postal varchar(255),
    ville varchar(255),
    date_utilisation varchar(255),
    utilisateur_id INT,
    valide BOOLEAN DEFAULT TRUE,
    favori BOOLEAN DEFAULT FALSE,
    constraint fr_utilisateur_adresse
                     foreign key (utilisateur_id) references utilisateur(id_utilisateur)
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
        adresse_livraison_id INT,
        adresse_facturation_id INT,
        constraint fk_utilisateur
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        constraint fk_etat
            FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
        CONSTRAINT fk_adresse_livraison
            FOREIGN KEY (adresse_livraison_id) REFERENCES adresse(id_adresse),
        CONSTRAINT fk_adresse_facturation
            FOREIGN KEY (adresse_facturation_id) REFERENCES adresse(id_adresse)
    );




    -- chaussure(id_chaussure, nom_chaussure, sexe, entretien, prix_chaussure, pointure_id, type_chaussure_id, fournisseur, marque, photo, stock )
    -- pointure (id_pointure, libelle_pointure)
    -- type_chaussure (id_type_chaussure, libelle_type_chaussure)

    CREATE TABLE taille(
        id_taille INT PRIMARY KEY AUTO_INCREMENT,
        libelle VARCHAR(128),
        code_taille INT
    );

    CREATE TABLE couleur(
        id_couleur INT PRIMARY KEY AUTO_INCREMENT,
        libelle VARCHAR(128),
        code_couleur INT
    );

    CREATE TABLE type_chaussure(
        id_type_chaussure INT PRIMARY KEY AUTO_INCREMENT,
        libelle_type_chaussure VARCHAR(128)
    );

    CREATE TABLE chaussure(
        id_chaussure INT PRIMARY KEY AUTO_INCREMENT,
        nom_chaussure VARCHAR(64),
        sexe VARCHAR(8),
        entretien VARCHAR(20),
        prix_chaussure NUMERIC(10,2),
        type_chaussure_id INT NOT NULL,
        fournisseur VARCHAR(100),
        marque VARCHAR(30),
        photo VARCHAR(256),
        descrption TEXT,
        constraint fk_type_chaussure
            foreign key (type_chaussure_id) REFERENCES type_chaussure(id_type_chaussure)
    );


    CREATE TABLE declinaison_chaussure(
        id_declinaison_chaussure INT PRIMARY KEY AUTO_INCREMENT,
        stock INT,
        prix_declinaison NUMERIC(10,2),
        chausssure_id INT,
        taille_id INT,
        couleur_id INT,
        FOREIGN KEY (chausssure_id) REFERENCES chaussure(id_chaussure),
        FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
        FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur)
    );

    CREATE TABLE ligne_commande(
        commande_id INT NOT NULL,
        declinaison_chaussure_id INT NOT NULL,
        prix NUMERIC(10,2),
        quantite INT,
        constraint fk_commande
            FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        constraint fk_declinaison_chaussufe
            FOREIGN KEY (declinaison_chaussure_id) REFERENCES declinaison_chaussure(id_declinaison_chaussure),
        PRIMARY KEY (commande_id,declinaison_chaussure_id)

    );

    CREATE TABLE ligne_panier(
        utilisateur_id INT NOT NULL,
        declinaison_chaussure_id INT NOT NULL,
        quantite INT,
        date_ajout date,
        constraint fk_utilisateur_panier
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        constraint fk_declinaison_chaussure_panier
            FOREIGN KEY (declinaison_chaussure_id) REFERENCES declinaison_chaussure(id_declinaison_chaussure),
        PRIMARY KEY (utilisateur_id,declinaison_chaussure_id)
    );






    CREATE TABLE commentaire (
        id_commentaire INT PRIMARY KEY AUTO_INCREMENT,
        commentaire TEXT,
        utilisateur_id INT,
        chaussure_id INT,
        date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
        valider BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (chaussure_id) REFERENCES chaussure(id_chaussure)
    );

    CREATE TABLE note (
        id_note INT PRIMARY KEY AUTO_INCREMENT,
        note DECIMAL(3,1),
        utilisateur_id INT,
        chaussure_id INT,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (chaussure_id) REFERENCES chaussure(id_chaussure)
    );


    INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom) VALUES
    (1,'admin','admin@admin.fr','scrypt:32768:8:1$irSP6dJEjy1yXof2$56295be51bb989f467598b63ba6022405139656d6609df8a71768d42738995a21605c9acbac42058790d30fd3adaaec56df272d24bed8385e66229c81e71a4f4','ROLE_admin','admin'),
    (2,'client','client@client.fr','scrypt:32768:8:1$iFP1d8bdBmhW6Sgc$7950bf6d2336d6c9387fb610ddaec958469d42003fdff6f8cf5a39cf37301195d2e5cad195e6f588b3644d2a9116fa1636eb400b0cb5537603035d9016c15910','ROLE_client','client'),
    (3,'client2','client2@client2.fr','scrypt:32768:8:1$l3UTNxiLZGuBKGkg$ae3af0d19f0d16d4a495aa633a1cd31ac5ae18f98a06ace037c0f4fb228ed86a2b6abc64262316d0dac936eb72a67ae82cd4d4e4847ee0fb0b19686ee31194b3','ROLE_client','client2');

    INSERT INTO taille (libelle, code_taille) VALUES
    ('taille unique', 0),('35', 35), ('36', 36), ('37', 37), ('38', 38), ('39', 39),
    ('40', 40), ('41', 41), ('42', 42), ('43', 43), ('44', 44), ('45', 45);

    INSERT INTO couleur (libelle, code_couleur) VALUES
    ('couleur unique', 0)('violet', 2), ('blanc', 3), ('rose', 4), ('marron', 5),
    ('brun', 6), ('noir', 7), ('rouge', 8), ('bleu', 9), ('orange', 10);

    INSERT INTO type_chaussure (libelle_type_chaussure) VALUES
    ('basket'), ('botte'), ('classique'), ('ville'), ('rando');

    -- Plus de pointure_id, plus de stock dans chaussure
    INSERT INTO chaussure (nom_chaussure, sexe, entretien, prix_chaussure, type_chaussure_id, fournisseur, marque, photo) VALUES
    ('Basket violette',              'femme',   'neuf', 79.99,  1, 'BFl',  'NILE',   'basket_f_violette_rose.jpg'),
    ('Basket Adidas',                'homme',   'neuf', 49.99,  1, 'BFL',  'Laco',   'basket_h_addidas.png'),
    ('Basket unisexe',               'unisexe', 'neuf', 99.99,  1, 'BFL',  'uni',    'basket_uni_blanche_noire.png'),
    ('Basket rose',                  'femme',   'neuf', 74.99,  1, 'BFl',  'Laco',   'baskets_f_rose.jpg'),
    ('Botte marron',                 'femme',   'neuf', 64.99,  2, 'BOFL', 'bolt',   'botte_f_marron.jpg'),
    ('Botte brune unisexe',          'unisexe', 'neuf', 74.99,  2, 'BOLF', 'bolt',   'botte_uni_brune.png'),
    ('Chaussure classique noire',    'femme',   'neuf', 566.99, 3, 'CHL',  'conver', 'chaussure_classique_f_noire.jpg'),
    ('Chaussure classique rouge',    'femme',   'neuf', 249.99, 3, 'CHL',  'conver', 'chaussure_classique_f_rouge.png'),
    ('Chaussure classique brune',    'homme',   'neuf', 290.99, 3, 'CHL',  'conver', 'chaussure_classique_h_brune.png'),
    ('Chaussure classique marron',   'homme',   'neuf', 229.99, 3, 'CHL',  'conver', 'chaussure_classique_h_maron_foncée.png'),
    ('Chaussure de ville noire',     'femme',   'neuf', 98.99,  4, 'VHL',  'villy',  'chaussure_de_ville_f_noire.png'),
    ('Chaussure de randonnée rose',  'femme',   'neuf', 99.99,  5, 'RHL',  'randim', 'chaussure_rando_f_rose.png'),
    ('Chaussure de randonnée noire', 'homme',   'neuf', 89.99,  5, 'RHL',  'randim', 'chaussure_rando_h_noire.png'),
    ('Chaussure de ville bleue',     'unisexe', 'neuf', 79.69,  4, 'VHL',  'villy',  'chaussure_ville_uni_bleue.png'),
    ('Chaussure de ville orange',    'unisexe', 'neuf', 69.99,  4, 'VHL',  'villy',  'chaussure_ville_uni_orange.png');

    -- Stock + taille + couleur sont maintenant ici
    -- taille_id : les ids correspondent aux INSERT taille (1=35 ... 7=41 ... 11=45)
    DROP TABLE IF EXISTS note;
    DROP TABLE IF EXISTS commentaire;
    DROP TABLE IF EXISTS ligne_panier;
    DROP TABLE IF EXISTS ligne_commande;
    DROP TABLE IF EXISTS commande;
    DROP TABLE IF EXISTS adresse;
    DROP TABLE IF EXISTS declinaison_chaussure;
    DROP TABLE IF EXISTS taille;
    DROP TABLE IF EXISTS couleur;
    DROP TABLE IF EXISTS chaussure;
    DROP TABLE IF EXISTS type_chaussure;
    DROP TABLE IF EXISTS etat;
    DROP TABLE IF EXISTS utilisateur;

    CREATE TABLE utilisateur(
        id_utilisateur INT PRIMARY KEY AUTO_INCREMENT ,
        login VARCHAR(20),
        email VARCHAR(100),
        nom varchar(256),
        password VARCHAR(1000),
        role VARCHAR(20)
    );

    create table adresse (
    id_adresse int primary key auto_increment,
    nom varchar(255),
    rue varchar(255),
    code_postal varchar(255),
    ville varchar(255),
    date_utilisation varchar(255),
    utilisateur_id INT,
    valide BOOLEAN DEFAULT TRUE,
    favori BOOLEAN DEFAULT FALSE,
    constraint fr_utilisateur_adresse
                     foreign key (utilisateur_id) references utilisateur(id_utilisateur)
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
        adresse_livraison_id INT,
        adresse_facturation_id INT,
        constraint fk_utilisateur
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        constraint fk_etat
            FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
        CONSTRAINT fk_adresse_livraison
            FOREIGN KEY (adresse_livraison_id) REFERENCES adresse(id_adresse),
        CONSTRAINT fk_adresse_facturation
            FOREIGN KEY (adresse_facturation_id) REFERENCES adresse(id_adresse)
    );




    -- chaussure(id_chaussure, nom_chaussure, sexe, entretien, prix_chaussure, pointure_id, type_chaussure_id, fournisseur, marque, photo, stock )
    -- pointure (id_pointure, libelle_pointure)
    -- type_chaussure (id_type_chaussure, libelle_type_chaussure)

    CREATE TABLE taille(
        id_taille INT PRIMARY KEY AUTO_INCREMENT,
        libelle VARCHAR(128),
        code_taille INT
    );

    CREATE TABLE couleur(
        id_couleur INT PRIMARY KEY AUTO_INCREMENT,
        libelle VARCHAR(128),
        code_couleur INT
    );

    CREATE TABLE type_chaussure(
        id_type_chaussure INT PRIMARY KEY AUTO_INCREMENT,
        libelle_type_chaussure VARCHAR(128)
    );

    CREATE TABLE chaussure(
        id_chaussure INT PRIMARY KEY AUTO_INCREMENT,
        nom_chaussure VARCHAR(64),
        sexe VARCHAR(8),
        entretien VARCHAR(20),
        prix_chaussure NUMERIC(10,2),
        type_chaussure_id INT NOT NULL,
        fournisseur VARCHAR(100),
        marque VARCHAR(30),
        photo VARCHAR(256),
        descrption TEXT,
        constraint fk_type_chaussure
            foreign key (type_chaussure_id) REFERENCES type_chaussure(id_type_chaussure)
    );


    CREATE TABLE declinaison_chaussure(
        id_declinaison_chaussure INT PRIMARY KEY AUTO_INCREMENT,
        stock INT,
        prix_declinaison NUMERIC(10,2),
        chausssure_id INT,
        taille_id INT,
        couleur_id INT,
        FOREIGN KEY (chausssure_id) REFERENCES chaussure(id_chaussure),
        FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
        FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur)
    );

    CREATE TABLE ligne_commande(
        commande_id INT NOT NULL,
        declinaison_chaussure_id INT NOT NULL,
        prix NUMERIC(10,2),
        quantite INT,
        constraint fk_commande
            FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        constraint fk_declinaison_chaussufe
            FOREIGN KEY (declinaison_chaussure_id) REFERENCES declinaison_chaussure(id_declinaison_chaussure),
        PRIMARY KEY (commande_id,declinaison_chaussure_id)

    );

    CREATE TABLE ligne_panier(
        utilisateur_id INT NOT NULL,
        declinaison_chaussure_id INT NOT NULL,
        quantite INT,
        date_ajout date,
        constraint fk_utilisateur_panier
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        constraint fk_declinaison_chaussure_panier
            FOREIGN KEY (declinaison_chaussure_id) REFERENCES declinaison_chaussure(id_declinaison_chaussure),
        PRIMARY KEY (utilisateur_id,declinaison_chaussure_id)
    );






    CREATE TABLE commentaire (
        id_commentaire INT PRIMARY KEY AUTO_INCREMENT,
        commentaire TEXT,
        utilisateur_id INT,
        chaussure_id INT,
        date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
        valider BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (chaussure_id) REFERENCES chaussure(id_chaussure)
    );

    CREATE TABLE note (
        id_note INT PRIMARY KEY AUTO_INCREMENT,
        note DECIMAL(3,1),
        utilisateur_id INT,
        chaussure_id INT,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (chaussure_id) REFERENCES chaussure(id_chaussure)
    );


    INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom) VALUES
    (1,'admin','admin@admin.fr','scrypt:32768:8:1$irSP6dJEjy1yXof2$56295be51bb989f467598b63ba6022405139656d6609df8a71768d42738995a21605c9acbac42058790d30fd3adaaec56df272d24bed8385e66229c81e71a4f4','ROLE_admin','admin'),
    (2,'client','client@client.fr','scrypt:32768:8:1$iFP1d8bdBmhW6Sgc$7950bf6d2336d6c9387fb610ddaec958469d42003fdff6f8cf5a39cf37301195d2e5cad195e6f588b3644d2a9116fa1636eb400b0cb5537603035d9016c15910','ROLE_client','client'),
    (3,'client2','client2@client2.fr','scrypt:32768:8:1$l3UTNxiLZGuBKGkg$ae3af0d19f0d16d4a495aa633a1cd31ac5ae18f98a06ace037c0f4fb228ed86a2b6abc64262316d0dac936eb72a67ae82cd4d4e4847ee0fb0b19686ee31194b3','ROLE_client','client2');

    INSERT INTO taille (libelle, code_taille) VALUES
    ('taille unique', 0),('35', 35), ('36', 36), ('37', 37), ('38', 38), ('39', 39),
    ('40', 40), ('41', 41), ('42', 42), ('43', 43), ('44', 44), ('45', 45);

    INSERT INTO couleur (libelle, code_couleur) VALUES
    ('couleur unique', 0),('violet', 1), ('blanc', 2), ('rose', 3), ('marron', 4),
    ('brun', 5), ('noir', 6), ('rouge', 7), ('bleu', 8), ('orange', 9);

    INSERT INTO type_chaussure (libelle_type_chaussure) VALUES
    ('basket'), ('botte'), ('classique'), ('ville'), ('rando');

    -- Plus de pointure_id, plus de stock dans chaussure
    INSERT INTO chaussure (nom_chaussure, sexe, entretien, prix_chaussure, type_chaussure_id, fournisseur, marque, photo) VALUES
    ('Basket violette',              'femme',   'neuf', 79.99,  1, 'BFl',  'NILE',   'basket_f_violette_rose.jpg'),
    ('Basket Adidas',                'homme',   'neuf', 49.99,  1, 'BFL',  'Laco',   'basket_h_addidas.png'),
    ('Basket unisexe',               'unisexe', 'neuf', 99.99,  1, 'BFL',  'uni',    'basket_uni_blanche_noire.png'),
    ('Basket rose',                  'femme',   'neuf', 74.99,  1, 'BFl',  'Laco',   'baskets_f_rose.jpg'),
    ('Botte marron',                 'femme',   'neuf', 64.99,  2, 'BOFL', 'bolt',   'botte_f_marron.jpg'),
    ('Botte brune unisexe',          'unisexe', 'neuf', 74.99,  2, 'BOLF', 'bolt',   'botte_uni_brune.png'),
    ('Chaussure classique noire',    'femme',   'neuf', 566.99, 3, 'CHL',  'conver', 'chaussure_classique_f_noire.jpg'),
    ('Chaussure classique rouge',    'femme',   'neuf', 249.99, 3, 'CHL',  'conver', 'chaussure_classique_f_rouge.png'),
    ('Chaussure classique brune',    'homme',   'neuf', 290.99, 3, 'CHL',  'conver', 'chaussure_classique_h_brune.png'),
    ('Chaussure classique marron',   'homme',   'neuf', 229.99, 3, 'CHL',  'conver', 'chaussure_classique_h_maron_foncée.png'),
    ('Chaussure de ville noire',     'femme',   'neuf', 98.99,  4, 'VHL',  'villy',  'chaussure_de_ville_f_noire.png'),
    ('Chaussure de randonnée rose',  'femme',   'neuf', 99.99,  5, 'RHL',  'randim', 'chaussure_rando_f_rose.png'),
    ('Chaussure de randonnée noire', 'homme',   'neuf', 89.99,  5, 'RHL',  'randim', 'chaussure_rando_h_noire.png'),
    ('Chaussure de ville bleue',     'unisexe', 'neuf', 79.69,  4, 'VHL',  'villy',  'chaussure_ville_uni_bleue.png'),
    ('Chaussure de ville orange',    'unisexe', 'neuf', 69.99,  4, 'VHL',  'villy',  'chaussure_ville_uni_orange.png');

    -- Stock + taille + couleur sont maintenant ici
    -- taille_id : les ids correspondent aux INSERT taille (1=35 ... 7=41 ... 11=45)
    INSERT INTO declinaison_chaussure (stock, prix_declinaison, chausssure_id, taille_id, couleur_id) VALUES
    -- Basket violette (id 1) - taille ET couleur unique
    (50, 79.99, 1, 1, 1),  -- violet

    -- Basket Adidas (id 2) - taille ET couleur unique
    (5, 49.99, 2, 1, 1),   -- noir

    -- Basket unisexe (id 3) - taille ET couleur unique
    (6, 99.99, 3, 1, 1),   -- blanc

    -- Basket rose (id 4) - taille ET couleur unique
    (4, 74.99, 4, 1, 1),   -- rose

    -- Botte marron (id 5) - taille ET couleur unique
    (7, 64.99, 5, 1, 1),   -- marron

    -- Botte brune unisexe (id 6) - taille ET couleur unique
    (3, 74.99, 6, 1, 1),   -- brun

    -- Classique noire (id 7) - taille ET couleur unique
    (9, 566.99, 7, 1, 1),  -- noir

    -- Classique rouge (id 8) - taille ET couleur unique
    (14, 249.99, 8, 1, 1), -- rouge

    -- Classique brune (id 9) - taille ET couleur unique
    (25, 290.99, 9, 1, 5), -- brun

    -- Classique marron (id 10) - taille ET couleur unique
    (18, 229.99, 10, 1, 4), -- marron

    -- Ville noire (id 11) - plusieurs COULEURS, taille unique
    (12, 98.99, 11, 1, 6),  -- noir
    (8,  98.99, 11, 1, 8),  -- bleu
    (5,  98.99, 11, 1, 4),  -- marron

    -- Rando rose (id 12) - plusieurs TAILLES, couleur unique
    (26, 99.99, 12, 3, 3),  -- taille 37, rose
    (14, 99.99, 12, 4, 3),  -- taille 38, rose
    (8,  99.99, 12, 5, 3),  -- taille 39, rose

    -- Rando noire (id 13) - taille ET couleur unique
    (2, 89.99, 13, 1, 6),   -- noir

    -- Ville bleue (id 14) - taille ET couleur unique
    (41, 79.69, 14, 1, 8),  -- bleu

    -- Ville orange (id 15) - déclinaison TAILLE + COULEUR
    (9,  69.99, 15, 6, 9),  -- taille 40, orange
    (4,  69.99, 15, 7, 9),  -- taille 41, orange
    (11, 69.99, 15, 6, 6),  -- taille 40, noir
    (6,  69.99, 15, 7, 6);  -- taille 41, noir

    INSERT INTO etat (libelle) VALUES
    ('en attente'), ('expédié'), ('validé'), ('confirmé');

    INSERT INTO commande (date_achat, utilisateur_id, etat_id) VALUES
    ('2024-01-10', 2, 1),
    ('2024-01-12', 2, 3),
    ('2024-01-15', 3, 2),
    ('2024-01-20', 3, 4);

    -- chaussure_id remplacé par declinaison_chaussure_id
    INSERT INTO ligne_commande (commande_id, declinaison_chaussure_id, prix, quantite) VALUES
    (1, 1,  79.99, 1),
    (1, 4,  74.99, 2),
    (2, 2,  49.99, 1),
    (3, 11, 98.99, 1),
    (3, 12, 99.99, 1),
    (4, 14, 79.69, 1),
    (4, 15, 69.99, 1);

    -- idem pour ligne_panier
    INSERT INTO ligne_panier (utilisateur_id, declinaison_chaussure_id, quantite, date_ajout) VALUES
    (2, 3, 1, '2024-02-01'),
    (2, 5, 2, '2024-02-02'),
    (3, 7, 1, '2024-02-03');


