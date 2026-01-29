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
    # sql='''
    # INSERT INTO utilisateur
    # '''
    # mycursor.execute(sql)

    sql=''' 
        CREATE TABLE type_chaussure(
            id_type_chaussure INT PRIMARY KEY AUTO_INCREMENT,
            libelle_type_chaussure VARCHAR(128)
        );
    '''
    mycursor.execute(sql)
#     sql='''
# INSERT INTO type_article
#     '''
#     mycursor.execute(sql)
    sql='''CREATE TABLE pointure(
    id_pointure INT PRIMARY KEY AUTO_INCREMENT,
    libelle_pointure VARCHAR(128)
           );
    '''
    mycursor.execute(sql)
    #     sql = '''
    # INSERT INTO pointure
    #      '''
    #     mycursor.execute(sql)



    sql=''' 
     CREATE TABLE etat(
     id_etat INT PRIMARY KEY AUTO_INCREMENT,
     libelle VARCHAR(20)
     ) DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
#     sql = '''
# INSERT INTO etat
#      '''
#     mycursor.execute(sql)

    sql = ''' 
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

     '''
    mycursor.execute(sql)
    # sql = '''
    # INSERT INTO article (
    #
    #      '''
    # mycursor.execute(sql)

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
    # sql = '''
    # INSERT INTO commande
    #              '''
    # mycursor.execute(sql)

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
    # sql = '''
    # INSERT INTO ligne_commande
    #      '''
    # mycursor.execute(sql)


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
