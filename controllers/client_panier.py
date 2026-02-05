#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session
import datetime #j'ai ajouté cet import pour obtenir la date quand on ajoute au panier


from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_chaussure = request.form.get('id_chaussure')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_chaussure=request.form.get('id_declinaison_chaussure',None)
    id_declinaison_chaussure = 1

# ajout dans le panier d'une déclinaison d'un chaussure (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_chaussure))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_chaussure = declinaisons[0]['id_declinaison_chaussure']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_chaussure))
    #     chaussure = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_chaussure.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , chaussure=chaussure)

# ajout dans le panier d'un chaussure
    sql='''SELECT * FROM ligne_panier
            WHERE ligne_panier.utilisateur_id=%s
            AND ligne_panier.chaussure_id=%s'''
    mycursor.execute(sql, (id_client, id_chaussure))
    article_panier=mycursor.fetchone()
    if (article_panier is not None and article_panier['quantite'] >=1):
        sql='''UPDATE ligne_panier 
                SET ligne_panier.quantite=ligne_panier.quantite+%s
                WHERE ligne_panier.utilisateur_id=%s
                AND ligne_panier.chaussure_id=%s'''
        mycursor.execute(sql, (quantite, id_client, id_chaussure))
        get_db().commit()
    else:
        date=datetime.datetime.now()
        dateSQL=date.strftime('%Y-%m-%d')
        tuple_param=(id_client, id_chaussure, quantite,dateSQL)
        sql='''INSERT INTO ligne_panier VALUES
                (%s,%s,%s,%s);'''
        mycursor.execute(sql, tuple_param)
        get_db().commit()

    return redirect('/client/chaussure/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_chaussure = request.form.get('id_chaussure','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'chaussure
    # id_declinaison_chaussure = request.form.get('id_declinaison_chaussure', None)

    sql = ''' selection de la ligne du panier pour la chaussure et l'utilisateur connecté'''
    chaussure_panier=[]

    if not(chaussure_panier is None) and chaussure_panier['quantite'] > 1:
        sql = ''' mise à jour de la quantité dans le panier => -1 chaussure '''
    else:
        sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'chaussure disponible
    get_db().commit()
    return redirect('/client/chaussure/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'chaussure pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'chaussure : stock = stock + qté de la ligne pour l'chaussure'''
        get_db().commit()
    return redirect('/client/chaussure/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_chaussure = request.form.get('id_declinaison_chaussure')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'chaussure : stock = stock + qté de la ligne pour l'chaussure'''

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
