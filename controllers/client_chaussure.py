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


    # utilisation du filtre
    list_param = []
    condition_and = ""
    print(session)
    if (session.get('filter_word',None) or session.get('filter_prix_min',None) or session.get('filter_prix_max',None) or session.get('filter_types',None)):
        sql+=" WHERE "
        if session.get('filter_word',None):
            sql+="chaussure.nom_chaussure LIKE %s"
            filter_word = session['filter_word']
            list_param.append(('%'+filter_word+'%'))
            condition_and = " AND "
        if session.get('filter_prix_min',None):
            list_param.append(session['filter_prix_min'])
            sql+=condition_and+"chaussure.prix_chaussure>=%s"
            condition_and = " AND "
        if session.get('filter_prix_max',None):
            list_param.append(session['filter_prix_max'])
            sql+=condition_and+"chaussure.prix_chaussure<=%s"
            condition_and = " AND "
        if session.get('filter_types',None):
            liste_types =session['filter_types']
            sql+=condition_and+"( "
            for i in range(len(liste_types)):
                sql+="chaussure.type_chaussure_id=%s"
                list_param.append(liste_types[i])
                if (i<len(liste_types)-1):
                    sql+=" OR "
            sql+=")"

    print(sql)
    print(tuple(list_param))
    print(session)

    mycursor.execute(sql, tuple(list_param))
    chaussures = mycursor.fetchall()


    sql3=''' SELECT chaussure'''
    # chaussures =[]


    # pour le filtre
    sql = '''SELECT type_chaussure.id_type_chaussure,
    type_chaussure.libelle_type_chaussure as libelle FROM type_chaussure'''
    mycursor.execute(sql)
    types_chaussure = mycursor.fetchall()

    sql='''SELECT ligne_panier.utilisateur_id,
                ligne_panier.chaussure_id,
                ligne_panier.quantite,
                ligne_panier.date_ajout,
                chaussure.prix_chaussure as prix,
                chaussure.nom_chaussure as nom
                FROM ligne_panier
                JOIN chaussure
                ON ligne_panier.chaussure_id = chaussure.id_chaussure
                WHERE ligne_panier.utilisateur_id=%s;'''

    mycursor.execute(sql,(id_client,))
    chaussures_panier = mycursor.fetchall()

    if len(chaussures_panier) >= 1:
        sql = ''' SELECT SUM(ligne_panier.quantite*chaussure.prix_chaussure) as prix_total
           FROM ligne_panier
            JOIN chaussure
            ON ligne_panier.chaussure_id=chaussure.id_chaussure
            WHERE ligne_panier.utilisateur_id=%s;'''
        mycursor.execute(sql,(id_client,))

        prix_total = mycursor.fetchone()["prix_total"]
    else:
        prix_total = None
    return render_template('client/boutique/panier_chaussure.html'
                           , chaussures=chaussures
                           , chaussures_panier=chaussures_panier
                           , prix_total=prix_total
                           , items_filtre=types_chaussure
                           )
