#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session
import datetime #j'ai ajouté cet import pour obtenir la date quand on ajoute au panier

from networkx.algorithms.operators.binary import difference

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    db= get_db()
    mycursor = db.cursor()
    id_client = session['id_user']
    id_chaussure = request.form.get('id_chaussure')
    quantite = request.form.get('quantite')
    date_ajout = datetime.datetime.now()

    id_declinaison_chaussure=request.form.get('id_declinaison_chaussure',None)

    if not id_declinaison_chaussure:

        sql = '''  SELECT declinaison_chaussure.id_declinaison_chaussure, \
                           declinaison_chaussure.couleur_id as id_couleur, \
                           couleur.libelle                  as libelle_couleur, \
                           declinaison_chaussure.taille_id  as id_taille, \
                           taille.libelle                   as libelle_taille, \
                           declinaison_chaussure.stock
                    FROM declinaison_chaussure
                             JOIN couleur
                                  ON declinaison_chaussure.couleur_id = couleur.id_couleur
                             JOIN taille
                                  ON declinaison_chaussure.taille_id = taille.id_taille
                    WHERE declinaison_chaussure.chaussure_id = %s'''

        mycursor.execute(sql, (id_chaussure,))

        declinaisons=mycursor.fetchall()
        if len(declinaisons) == 1:
            id_declinaison_chaussure = declinaisons[0]['id_declinaison_chaussure']

        elif len(declinaisons) == 0:
            abort("pb nb de declinaison")
        else:
            sql = '''
                    SELECT
                    chaussure.id_chaussure,
                    chaussure.nom_chaussure as nom,
                    chaussure.prix_chaussure as prix,
                    chaussure.photo as image
                    FROM chaussure
                    WHERE chaussure.id_chaussure=%s
                  '''


            mycursor.execute(sql, (id_chaussure,))
            chaussure = mycursor.fetchone()

            return render_template('client/boutique/declinaison_chaussure.html'
                                       , declinaisons=declinaisons
                                       , quantite=quantite
                                       , chaussure=chaussure)



    sql='''SELECT declinaison_chaussure.stock-%s as difference
            FROM declinaison_chaussure
            WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''
    mycursor.execute(sql, (quantite, id_declinaison_chaussure))
    difference=mycursor.fetchone()["difference"]
    if (difference>=0):

        requete = '''   SELECT * 
                        FROM ligne_panier
                        WHERE ligne_panier.declinaison_chaussure_id=%s
                        AND ligne_panier.utilisateur_id=%s'''

        mycursor.execute(requete,(id_declinaison_chaussure,id_client))
        panier=mycursor.fetchall()
        if (len(panier)>=1):
            sql='''UPDATE ligne_panier
                    SET ligne_panier.quantite=ligne_panier.quantite+%s
                    WHERE ligne_panier.declinaison_chaussure_id=%s
                    AND ligne_panier.utilisateur_id=%s'''
            mycursor.execute(sql,(quantite,id_declinaison_chaussure, id_client))
        else:
            sql='''INSERT INTO ligne_panier(utilisateur_id,declinaison_chaussure_id,quantite,date_ajout) 
                   VALUES (%s,%s,%s,%s)
                    '''
            mycursor.execute(sql, (id_client,id_declinaison_chaussure,quantite,date_ajout))

        sql2='''UPDATE declinaison_chaussure
                SET declinaison_chaussure.stock = declinaison_chaussure.stock - %s 
                WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''
        mycursor.execute(sql2, (quantite,id_declinaison_chaussure))
        db.commit()
        return redirect('/client/chaussure/show')
    else:
        flash('article indisponible en cette quantité')
        return redirect('/client/chaussure/show')







@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    id_chaussure = request.form.get('id_chaussure','')
    print("id client : ",id_client," - id_chaussure ",id_chaussure)
    quantite = 1



    # ---------
    # partie 2 : on supprime une déclinaison de la chaussure
    id_declinaison_chaussure = request.form.get('id_declinaison_chaussure', None)

    sql = '''   SELECT ligne_panier.declinaison_chaussure_id, ligne_panier.utilisateur_id, ligne_panier.quantite
                FROM ligne_panier
                WHERE ligne_panier.utilisateur_id=%s
                AND ligne_panier.declinaison_chaussure_id=%s'''
    tuple_param=(id_client,id_declinaison_chaussure)
    mycursor.execute(sql,tuple_param)
    chaussure_panier=mycursor.fetchone()
    print("chaussures panier ",chaussure_panier,id_client," ",id_chaussure)


    if not (chaussure_panier is None) and chaussure_panier['quantite'] > 1:
        sql = ''' UPDATE ligne_panier 
                  SET ligne_panier.quantite=ligne_panier.quantite - 1
                    WHERE ligne_panier.utilisateur_id=%s
                    AND ligne_panier.declinaison_chaussure_id=%s'''
        mycursor.execute(sql, tuple_param)

    else:
        sql='''DELETE FROM ligne_panier
            WHERE ligne_panier.utilisateur_id=%s
            AND ligne_panier.declinaison_chaussure_id=%s'''
        mycursor.execute(sql,tuple_param)

    # mise à jour du stock de l'chaussure disponible
    sql='''UPDATE declinaison_chaussure 
            SET declinaison_chaussure.stock=declinaison_chaussure.stock+1
            WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''
    mycursor.execute(sql, (id_declinaison_chaussure,))
    get_db().commit()
    return redirect('/client/chaussure/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * from ligne_panier WHERE ligne_panier.utilisateur_id=%s'''
    mycursor.execute(sql,(client_id,))
    items_panier = mycursor.fetchall()


    for item in items_panier:
        sql = '''   DELETE FROM ligne_panier
                    WHERE ligne_panier.utilisateur_id=%s
                    AND ligne_panier.declinaison_chaussure_id=%s'''



        sql2='''    UPDATE declinaison_chaussure
                    SET declinaison_chaussure.stock=declinaison_chaussure.stock+%s
                    WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''
        mycursor.execute(sql, (client_id, item['declinaison_chaussure_id']) )

        mycursor.execute(sql2, (item['quantite'],item['declinaison_chaussure_id']) )
        get_db().commit()
    return redirect('/client/chaussure/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_chaussure=request.form.get('id_chaussure', ' ')
    #id_declinaison_chaussure = request.form.get('id_declinaison_chaussure')

    tuple_param=(id_client,id_chaussure)
    sql = ''' SELECT ligne_panier.utilisateur_id,
            ligne_panier.chaussure_id, 
            ligne_panier.quantite
            FROM ligne_panier
            WHERE ligne_panier.utilisateur_id=%s
            AND ligne_panier.chaussure_id=%s'''


    mycursor.execute(sql, tuple_param)
    quantite = mycursor.fetchone()['quantite']


    sql = ''' DELETE FROM ligne_panier
              WHERE ligne_panier.utilisateur_id=%s
              AND ligne_panier.declinaison_chaussure_id=%s'''
    mycursor.execute(sql, tuple_param)


    sql2='''UPDATE chaussure
            SET chaussure.stock=chaussure.stock+%s
            WHERE chaussure.id_chaussure=%s'''

    mycursor.execute(sql2, (quantite,id_chaussure))

    get_db().commit()
    return redirect('/client/chaussure/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():


    filter_word = request.form.get('filter_word', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    if filter_word != None or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash("Le mot recherché ne doit etre composé que de lettres !")
        else:
            if len(filter_word) == 1:
                flash("le mot recherché doit contenir au moins 2 lettres !")
            else:
                session.pop('filter_word', None)
    if filter_prix_max or filter_prix_min:
        filter_prix_min = str(filter_prix_min).replace(' ', '').replace(',', '.')
        filter_prix_max= str(filter_prix_max).replace(' ', '').replace(',', '.')
        if filter_prix_min.replace('.', '', 1).isdigit() and filter_prix_max.replace('.', '', 1).isdigit():
            if float(filter_prix_max) > float(filter_prix_min):
                session['filter_prix_max'] = filter_prix_max
                session['filter_prix_min'] = filter_prix_min
            else:
                flash("le maximum doit être supérieur au minimum")
        else:
            flash("min et max doivent être des numériques")
    else:
        session.pop('filter_prix_max', None)
        session.pop('filter_prix_min', None)
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types
    else:
        session.pop('filter_types', None)
    return redirect('/client/chaussure/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    return redirect('/client/chaussure/show')