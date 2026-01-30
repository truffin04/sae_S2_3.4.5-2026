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
    mycursor.execute("DROP TABLE IF EXISTS ligne_panier")
    mycursor.execute("DROP TABLE IF EXISTS ligne_commande")
    mycursor.execute("DROP TABLE IF EXISTS commande")
    mycursor.execute("DROP TABLE IF EXISTS utilisateur")
    mycursor.execute("DROP TABLE IF EXISTS chaussure")
    mycursor.execute("DROP TABLE IF EXISTS pointure")
    mycursor.execute("DROP TABLE IF EXISTS type_chaussure")
    mycursor.execute("DROP TABLE IF EXISTS etat")

    sql='''
CREATE TABLE utilisateur(
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT ,
    login VARCHAR(20),
    email VARCHAR(100),
    nom varchar(256),
    password VARCHAR(1000),
    role VARCHAR(20)
     ) DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql='''
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
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

    sql=''' 
        CREATE TABLE type_chaussure(
            id_type_chaussure INT PRIMARY KEY AUTO_INCREMENT,
            libelle_type_chaussure VARCHAR(128)
        );
    '''
    mycursor.execute(sql)
    sql='''
        INSERT INTO type_chaussure (libelle_type_chaussure)
        VALUES ('basket'),
               ('botte'),
               ('classique'),
               ('ville'),
               ('rando');
    '''
    mycursor.execute(sql)
    sql='''CREATE TABLE pointure(
    id_pointure INT PRIMARY KEY AUTO_INCREMENT,
    libelle_pointure VARCHAR(128)
           );
    '''
    mycursor.execute(sql)
    sql = '''
        INSERT INTO pointure (libelle_pointure)
        VALUES
            (45),
            (44),
            (43),
            (42),
            (41),
            (40),
            (39),
            (38),
            (37),
            (36),
            (35);
         '''
    mycursor.execute(sql)



    sql=''' 
     CREATE TABLE etat(
     id_etat INT PRIMARY KEY AUTO_INCREMENT,
     libelle VARCHAR(20)
     ) DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
    sql = '''
        INSERT INTO etat (etat.libelle)
        VALUES
        ('en attente'),
        ('expédié'),
        ('validé'),
        ('confirmé')
        ;
     '''
    mycursor.execute(sql)

    sql = ''' 
            CREATE TABLE chaussure(
                id_chaussure INT PRIMARY KEY AUTO_INCREMENT,
                nom_chaussure VARCHAR(64),
                sexe VARCHAR(8),
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

     '''
    mycursor.execute(sql)
    sql = '''
INSERT INTO chaussure (nom_chaussure, sexe, entretien, prix_chaussure, pointure_id, type_chaussure_id, fournisseur, marque, photo, stock)
VALUES
( 'Basket violette', 'femme', 'neuf', 79.99, 8, 1, 'BFl', 'NILE', 'basket_f_violette_rose.jpg', 50),
( 'Basket Adidas', 'homme', 'neuf', 49.99, 6, 1, 'BFL', 'Laco', 'basket_h_addidas.png', 5),
( 'Basket unisexe', 'unisexe', 'neuf', 99.99, 6, 1, 'BFL', 'uni', 'basket_uni_blanche_noire.png', 6),
('Basket rose', 'femme', 'neuf', 74.99, 8, 1, 'BFl', 'Laco', 'baskets_f_rose.jpg', 4),
( 'Botte marron', 'femme', 'neuf', 64.99, 8, 2, 'BOFL', 'bolt', 'botte_f_marron.jpg', 7),
( 'Botte brune unisexe', 'unisexe', 'neuf', 74.99, 6, 2, 'BOLF', 'bolt', 'botte_uni_brune.png', 3),
( 'Chaussure classique noire', 'femme', 'neuf', 566.99, 8, 3, 'CHL', 'conver', 'chaussure_classique_f_noire.jpg', 9),
( 'Chaussure classique rouge', 'femme', 'neuf', 249.99, 8, 3, 'CHL', 'conver', 'chaussure_classique_f_rouge.png', 14),
( 'Chaussure classique brune', 'homme', 'neuf', 290.99, 6, 3, 'CHL', 'conver', 'chaussure_classique_h_brune.png', 25),
( 'Chaussure classique marron foncé', 'homme', 'neuf', 229.99, 6, 3, 'CHL', 'conver', 'chaussure_classique_h_maron_foncée.png', 18),
( 'Chaussure de ville noire', 'femme', 'neuf', 98.99, 8, 4, 'VHL', 'villy', 'chaussure_de_ville_f_noire.png', 12),
( 'Chaussure de randonnée rose', 'femme', 'neuf', 99.99, 8, 5, 'RHL', 'randim', 'chaussure_rando_f_rose.png', 26),
( 'Chaussure de randonnée noire', 'homme', 'neuf', 89.99, 6, 5, 'RHL', 'randim', 'chaussure_rando_h_noire.png', 2),
('Chaussure de ville bleue', 'unisexe', 'neuf', 79.69, 6, 4, 'VHL', 'villy', 'chaussure_ville_uni_bleue.png', 41),
( 'Chaussure de ville orange', 'unisexe', 'neuf', 69.99, 6, 4, 'VHL', 'villy', 'chaussure_ville_uni_orange.png', 9);
         '''
    mycursor.execute(sql)

    sql = ''' 
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
        CREATE TABLE ligne_commande \
        (
            commande_id  INT,
            chaussure_id INT,
            prix         NUMERIC(10, 2),
            quantite     INT,
            constraint fk_commande
                FOREIGN KEY (commande_id) REFERENCES commande (id_commande),
            constraint fk_chaussure
                FOREIGN KEY (chaussure_id) REFERENCES chaussure (id_chaussure),
            PRIMARY KEY (commande_id, chaussure_id) \
        );
         '''
    mycursor.execute(sql)
    sql = '''
        INSERT INTO ligne_commande (commande_id, chaussure_id, prix, quantite) VALUES
        (1, 1, 79.99, 1),
        (1, 4, 74.99, 2),
        (2, 2, 49.99, 1),
        (3, 11, 98.99, 1),
        (3, 12, 99.99, 1),
        (4, 14, 79.69, 1),
        (4, 15, 69.99, 1);
         '''
    mycursor.execute(sql)


    sql = ''' 
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
         '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
