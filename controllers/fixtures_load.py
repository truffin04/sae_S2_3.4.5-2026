#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    mycursor.execute("DROP TABLE IF EXISTS note")
    mycursor.execute("DROP TABLE IF EXISTS commentaire")
    mycursor.execute("DROP TABLE IF EXISTS ligne_panier")
    mycursor.execute("DROP TABLE IF EXISTS ligne_commande")
    mycursor.execute("DROP TABLE IF EXISTS commande")
    mycursor.execute("DROP TABLE IF EXISTS adresse")
    mycursor.execute("DROP TABLE IF EXISTS declinaison_chaussure")
    mycursor.execute("DROP TABLE IF EXISTS taille")
    mycursor.execute("DROP TABLE IF EXISTS couleur")
    mycursor.execute("DROP TABLE IF EXISTS chaussure")
    mycursor.execute("DROP TABLE IF EXISTS type_chaussure")
    mycursor.execute("DROP TABLE IF EXISTS etat")
    mycursor.execute("DROP TABLE IF EXISTS utilisateur")

    sql = '''
        CREATE TABLE utilisateur(
            id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
            login VARCHAR(20),
            email VARCHAR(100),
            nom VARCHAR(256),
            password VARCHAR(1000),
            role VARCHAR(20)
        ) DEFAULT CHARSET utf8;
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom) VALUES
        (1,'admin','admin@admin.fr',
            'scrypt:32768:8:1$irSP6dJEjy1yXof2$56295be51bb989f467598b63ba6022405139656d6609df8a71768d42738995a21605c9acbac42058790d30fd3adaaec56df272d24bed8385e66229c81e71a4f4',
            'ROLE_admin','admin'),
        (2,'client','client@client.fr',
            'scrypt:32768:8:1$iFP1d8bdBmhW6Sgc$7950bf6d2336d6c9387fb610ddaec958469d42003fdff6f8cf5a39cf37301195d2e5cad195e6f588b3644d2a9116fa1636eb400b0cb5537603035d9016c15910',
            'ROLE_client','client'),
        (3,'client2','client2@client2.fr',
            'scrypt:32768:8:1$l3UTNxiLZGuBKGkg$ae3af0d19f0d16d4a495aa633a1cd31ac5ae18f98a06ace037c0f4fb228ed86a2b6abc64262316d0dac936eb72a67ae82cd4d4e4847ee0fb0b19686ee31194b3',
            'ROLE_client','client2');
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE adresse (
            id_adresse INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(255),
            rue VARCHAR(255),
            code_postal VARCHAR(255),
            ville VARCHAR(255),
            date_utilisation VARCHAR(255),
            utilisateur_id INT,
            valide BOOLEAN DEFAULT TRUE,
            favori BOOLEAN DEFAULT FALSE,
            CONSTRAINT fr_utilisateur_adresse
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
        );
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE etat(
            id_etat INT PRIMARY KEY AUTO_INCREMENT,
            libelle VARCHAR(20)
        ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO etat (libelle) VALUES
        ('en attente'),
        ('expédié'),
        ('validé'),
        ('confirmé');
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE commande(
            id_commande INT PRIMARY KEY AUTO_INCREMENT,
            date_achat DATE,
            utilisateur_id INT,
            etat_id INT,
            adresse_livraison_id INT,
            adresse_facturation_id INT,
            CONSTRAINT fk_utilisateur
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
            CONSTRAINT fk_etat
                FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
            CONSTRAINT fk_adresse_livraison
                FOREIGN KEY (adresse_livraison_id) REFERENCES adresse(id_adresse),
            CONSTRAINT fk_adresse_facturation
                FOREIGN KEY (adresse_facturation_id) REFERENCES adresse(id_adresse)
        );
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO commande (date_achat, utilisateur_id, etat_id) VALUES
        ('2024-01-10', 2, 1),
        ('2024-01-12', 2, 3),
        ('2024-01-15', 3, 2),
        ('2024-01-20', 3, 4);
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE taille(
            id_taille INT PRIMARY KEY AUTO_INCREMENT,
            libelle VARCHAR(128),
            code_taille INT
        );
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO taille (libelle, code_taille) VALUES
        ('taille unique', 0),
        ('35', 35), ('36', 36), ('37', 37), ('38', 38), ('39', 39),
        ('40', 40), ('41', 41), ('42', 42), ('43', 43), ('44', 44), ('45', 45);
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE couleur(
            id_couleur INT PRIMARY KEY AUTO_INCREMENT,
            libelle VARCHAR(128),
            code_couleur INT
        );
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO couleur (libelle, code_couleur) VALUES
        ('couleur unique', 0),
        ('violet', 1), ('blanc', 2), ('rose', 3), ('marron', 4),
        ('brun', 5), ('noir', 6), ('rouge', 7), ('bleu', 8), ('orange', 9);
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE type_chaussure(
            id_type_chaussure INT PRIMARY KEY AUTO_INCREMENT,
            libelle_type_chaussure VARCHAR(128)
        );
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO type_chaussure (libelle_type_chaussure) VALUES
        ('basket'), ('botte'), ('classique'), ('ville'), ('rando');
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE chaussure(
            id_chaussure INT PRIMARY KEY AUTO_INCREMENT,
            nom_chaussure VARCHAR(64),
            sexe VARCHAR(8),
            entretien VARCHAR(20),
            prix_chaussure NUMERIC(10,2),
            type_chaussure_id INT NOT NULL,
            fournisseur VARCHAR(100),
            marque VARCHAR(30),
            disponible BOOLEAN DEFAULT TRUE,
            photo VARCHAR(256),
            descrption TEXT,
            CONSTRAINT fk_type_chaussure
                FOREIGN KEY (type_chaussure_id) REFERENCES type_chaussure(id_type_chaussure)
        );
    '''
    mycursor.execute(sql)

    sql = '''
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
    '''
    mycursor.execute(sql)

    sql = '''
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
    '''
    mycursor.execute(sql)

    # couleur_id : 1=couleur unique, 2=violet, 3=blanc, 4=rose, 5=marron, 6=brun, 7=noir, 8=rouge, 9=bleu, 10=orange
    # taille_id  : 1=taille unique, 2=35, 3=36, 4=37, 5=38, 6=39, 7=40, 8=41, ...
    sql = '''
        INSERT INTO declinaison_chaussure (stock, prix_declinaison, chausssure_id, taille_id, couleur_id) VALUES
        (50, 79.99,  1, 1, 1),   -- Basket violette        : taille unique, violet
        (5,  49.99,  2, 1, 1),   -- Basket Adidas          : taille unique, noir
        (6,  99.99,  3, 1, 1),   -- Basket unisexe         : taille unique, blanc
        (4,  74.99,  4, 1, 1),   -- Basket rose            : taille unique, rose
        (7,  64.99,  5, 1, 1),   -- Botte marron           : taille unique, marron
        (3,  74.99,  6, 1, 1),   -- Botte brune            : taille unique, brun
        (9,  566.99, 7, 1, 1),   -- Classique noire        : taille unique, noir
        (14, 249.99, 8, 1, 1),   -- Classique rouge        : taille unique, rouge
        (25, 290.99, 9, 1, 1),   -- Classique brune        : taille unique, brun
        (18, 229.99, 10, 1, 1),  -- Classique marron       : taille unique, marron
        (12, 98.99,  11, 1, 1),  -- Ville noire            : taille unique, noir
        (8,  98.99,  11, 1, 1),  -- Ville noire            : taille unique, bleu
        (5,  98.99,  11, 1, 1),  -- Ville noire            : taille unique, marron
        (26, 99.99,  12, 4, 1),  -- Rando rose taille 37   : couleur unique
        (14, 99.99,  12, 5, 1),  -- Rando rose taille 38   : couleur unique
        (8,  99.99,  12, 6, 1),  -- Rando rose taille 39   : couleur unique
        (2,  89.99,  13, 1, 7),  -- Rando noire            : taille unique, noir
        (41, 79.69,  14, 1, 9),  -- Ville bleue            : taille unique, bleu
        (9,  69.99,  15, 7, 10), -- Ville orange taille 40 : orange
        (4,  69.99,  15, 8, 10), -- Ville orange taille 41 : orange
        (11, 69.99,  15, 7, 7),  -- Ville orange taille 40 : noir
        (6,  69.99,  15, 8, 7);  -- Ville orange taille 41 : noir
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE ligne_commande(
            commande_id INT NOT NULL,
            declinaison_chaussure_id INT NOT NULL,
            prix NUMERIC(10,2),
            quantite INT,
            CONSTRAINT fk_commande
                FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
            CONSTRAINT fk_declinaison_chaussure
                FOREIGN KEY (declinaison_chaussure_id) REFERENCES declinaison_chaussure(id_declinaison_chaussure),
            PRIMARY KEY (commande_id, declinaison_chaussure_id)
        );
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO ligne_commande (commande_id, declinaison_chaussure_id, prix, quantite) VALUES
        (1, 1,  79.99, 1),
        (1, 4,  74.99, 2),
        (2, 2,  49.99, 1),
        (3, 11, 98.99, 1),
        (3, 14, 99.99, 1),
        (4, 18, 79.69, 1),
        (4, 19, 69.99, 1);
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE ligne_panier(
            utilisateur_id INT NOT NULL,
            declinaison_chaussure_id INT NOT NULL,
            quantite INT,
            date_ajout DATE,
            CONSTRAINT fk_utilisateur_panier
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
            CONSTRAINT fk_declinaison_chaussure_panier
                FOREIGN KEY (declinaison_chaussure_id) REFERENCES declinaison_chaussure(id_declinaison_chaussure),
            PRIMARY KEY (utilisateur_id, declinaison_chaussure_id)
        );
    '''
    mycursor.execute(sql)

    sql = '''
        INSERT INTO ligne_panier (utilisateur_id, declinaison_chaussure_id, quantite, date_ajout) VALUES
        (2, 3, 1, '2024-02-01'),
        (2, 5, 2, '2024-02-02'),
        (3, 7, 1, '2024-02-03');
    '''
    mycursor.execute(sql)

    sql = '''
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
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE note (
            id_note INT PRIMARY KEY AUTO_INCREMENT,
            note DECIMAL(3,1),
            utilisateur_id INT,
            chaussure_id INT,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
            FOREIGN KEY (chaussure_id) REFERENCES chaussure(id_chaussure)
        );
    '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')