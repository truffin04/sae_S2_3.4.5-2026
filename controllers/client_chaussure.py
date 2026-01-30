#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_chaussure = Blueprint('client_chaussure', __name__,
                        template_folder='templates')

@client_chaussure.route('/client/index')
@client_chaussure.route('/client/chaussure/show')              # remplace /client
def client_chaussure_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
          SELECT
              chaussure.id_chaussure,
              chaussure.nom_chaussure as nom, 
              chaussure.sexe,
              chaussure.entretien,
              chaussure.prix_chaussure as prix,
              chaussure.type_chaussure_id,
              chaussure.fournisseur,
              chaussure.marque,
              chaussure.photo as image,
              chaussure.stock
     FROM chaussure'''
    mycursor.execute(sql)

    chaussures = mycursor.fetchall()
    print(chaussures)

    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    # chaussures =[]


    # pour le filtre
    sql = '''SELECT type_chaussure.id_type_chaussure,
    type_chaussure.libelle_type_chaussure as libelle FROM type_chaussure'''
    mycursor.execute(sql)
    types_chaussure = mycursor.fetchall()


    chaussures_panier = []

    if len(chaussures_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_chaussure.html'
                           , chaussures=chaussures
                           , chaussures_panier=chaussures_panier
                           #, prix_total=prix_total
                           , items_filtre=types_chaussure
                           )
