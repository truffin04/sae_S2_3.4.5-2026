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
        pointure_id INT NOT NULL,
        type_chaussure_id INT NOT NULL,
        fournisseur VARCHAR(100),
        marque VARCHAR(30),
        photo VARCHAR(256),
        descrption varchar(255),
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

