#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' selection des chaussures d'un panier 
    '''
    chaussures_panier = []
    if len(chaussures_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , chaussures_panier=chaussures_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' SELECT ligne_panier.chaussure_id, ligne_panier.quantite, chaussure.prix_chaussure
              FROM ligne_panier
              JOIN chaussure ON ligne_panier.chaussure_id = chaussure.id_chaussure
              WHERE ligne_panier.utilisateur_id = %s;'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    # if items_ligne_panier is None or len(items_ligne_panier) < 1:
    #     flash(u'Pas d\'chaussures dans le ligne_panier', 'alert-warning')
    #     return redirect('/client/chaussure/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")

    sql = ''' INSERT INTO commande(date_achat, utilisateur_id, etat_id) VALUES (%s, %s, %s)'''
    date_today = datetime.now().strftime('%Y-%m-%d')
    mycursor.execute(sql, (date_today, id_client, 1))

    sql = ''' SELECT last_insert_id() as last_insert_id '''
    mycursor.execute(sql)
    last_id = mycursor.fetchone()
    id_nouvelle_commande = last_id['last_insert_id']


    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = ''' DELETE FROM ligne_panier 
                    WHERE utilisateur_id = %s AND chaussure_id = %s'''
        mycursor.execute(sql, (id_client, item['chaussure_id']))

        sql = "  INSERT INTO ligne_commande VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (id_nouvelle_commande, item['chaussure_id'], item['prix_chaussure'], item['quantite']))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/chaussure/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''  SELECT commande.id_commande, commande.date_achat, commande.etat_id,
                      etat.libelle, SUM(ligne_commande.quantite) as nbr_chaussures, 
                      SUM(ligne_commande.prix) as prix_total
                FROM commande
                JOIN etat ON commande.etat_id = etat.id_etat
                JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
                WHERE commande.utilisateur_id = %s
                GROUP BY  commande.id_commande, commande.date_achat, commande.etat_id, etat.libelle
                ORDER BY commande.etat_id, commande.date_achat DESC;'''

    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    chaussures_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' selection du détails d'une commande '''

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , chaussures_commande=chaussures_commande
                           , commande_adresses=commande_adresses
                           )

