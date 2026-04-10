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

    sql=''' SELECT COUNT(*) as nb FROM ligne_panier
            JOIN declinaison_chaussure 
            ON ligne_panier.declinaison_chaussure_id=declinaison_chaussure.id_declinaison_chaussure
            WHERE declinaison_chaussure.disponible=FALSE'''
    mycursor.execute(sql)
    if mycursor.fetchone()['nb']>0:
        flash("une des déclinaisons de chaussure que vous avez selectionné n'est plus dispoible", "alert-warning")
        return redirect("/client/chaussure/show")
    sql = '''   SELECT ligne_panier.declinaison_chaussure_id, ligne_panier.quantite, declinaison_chaussure.prix_declinaison as prix, chaussure.nom_chaussure  as nom 
                FROM ligne_panier 
                JOIN declinaison_chaussure 
                ON ligne_panier.declinaison_chaussure_id  = declinaison_chaussure.id_declinaison_chaussure
                JOIN chaussure on declinaison_chaussure.chaussure_id = chaussure.id_chaussure
                WHERE ligne_panier.utilisateur_id = %s'''

    mycursor.execute(sql, (id_client,))
    chaussures_panier = mycursor.fetchall()
    print(chaussures_panier)
    if len(chaussures_panier) >= 1:
        sql = '''   SELECT SUM(declinaison_chaussure.prix_declinaison * ligne_panier.quantite) as prix_total FROM ligne_panier
                    JOIN declinaison_chaussure 
                    ON ligne_panier.declinaison_chaussure_id  = declinaison_chaussure.id_declinaison_chaussure
                    WHERE ligne_panier.utilisateur_id = %s
                    '''
        mycursor.execute(sql, (id_client,))
        prix_dict = mycursor.fetchone()
        print(prix_dict)
        prix_total = prix_dict["prix_total"]
    else:
        prix_total = 0
        flash("erreur, panier vide")
        redirect('/client/chaussure/show')
    # etape 2 : selection des adresses
    sql='''SELECT * from adresse where adresse.utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    adresses=mycursor.fetchall()
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
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
    sql = '''   SELECT ligne_panier.declinaison_chaussure_id, ligne_panier.quantite, declinaison_chaussure.prix_declinaison
                FROM ligne_panier
                JOIN declinaison_chaussure 
                ON ligne_panier.declinaison_chaussure_id  = declinaison_chaussure.id_declinaison_chaussure
                WHERE ligne_panier.utilisateur_id = %s;'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'P\'chaussures dans le ligne_panier', 'alert-warning')
        return redirect('/client/chaussure/show')
                                               # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    a = datetime.now()

    sql = ''' INSERT INTO commande(date_achat, utilisateur_id, etat_id) VALUES (%s, %s, %s)'''
    mycursor.execute(sql, (a, id_client, 1))

    sql = ''' SELECT last_insert_id() as last_insert_id '''
    mycursor.execute(sql)
    last_id = mycursor.fetchone()
    id_nouvelle_commande = last_id['last_insert_id']

    for item in items_ligne_panier:


        # sql = '''   SELECT chaussure.nom_chaussure as nom, ligne_commande.quantite, ligne_commande.prix, ligne_commande.quantite * ligne_commande.prix as prix_ligne
        #             FROM ligne_commande
        #             JOIN declinaison_chaussure on ligne_commande.declinaison_chaussure_id = declinaison_chaussure.id_declinaison_chaussure
        #             JOIN chaussure ON declinaison_chaussure.chaussure_id = chaussure.id_chaussure
        #             JOIN commande ON ligne_commande.commande_id = commande.id_commande
        #             WHERE utilisateur_id = %s AND declinaison_chaussure_id = %s'''
        # mycursor.execute(sql, (id_client, item['declinaison_chaussure_id']))


        sql = "  INSERT INTO ligne_commande VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (id_nouvelle_commande, item['declinaison_chaussure_id'], item['prix_declinaison'], item['quantite']))

    sql=''' DELETE FROM ligne_panier
            where utilisateur_id=%s
            '''
    mycursor.execute(sql, (id_client,))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/chaussure/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''  SELECT commande.id_commande, commande.date_achat, commande.etat_id,
                      etat.libelle, SUM(ligne_commande.quantite) as nbr_chaussures, 
                      SUM(ligne_commande.quantite * ligne_commande.prix) as prix_total
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
        sql = '''   SELECT chaussure.nom_chaussure as nom, 
                    ligne_commande.quantite, 
                    ligne_commande.prix, 
                    ligne_commande.quantite * ligne_commande.prix as prix_ligne,
                    declinaison_chaussure.couleur_id,
                    couleur.libelle as libelle_couleur,
                    declinaison_chaussure.taille_id,
                    taille.libelle as libelle_taille,
                    (
                        SELECT COUNT(d2.id_declinaison_chaussure) 
                        FROM declinaison_chaussure AS d2
                        WHERE d2.chaussure_id = chaussure.id_chaussure
                        AND d2.disponible=TRUE
                    ) as nb_declinaisons
                    FROM ligne_commande
                    JOIN declinaison_chaussure on ligne_commande.declinaison_chaussure_id = declinaison_chaussure.id_declinaison_chaussure
                    JOIN chaussure ON declinaison_chaussure.chaussure_id = chaussure.id_chaussure
                    JOIN commande ON ligne_commande.commande_id = commande.id_commande
                    JOIN couleur ON declinaison_chaussure.couleur_id = couleur.id_couleur
                    JOIN taille ON declinaison_chaussure.taille_id = taille.id_taille
                    WHERE ligne_commande.commande_id = %s
                    AND commande.utilisateur_id = %s
            
        '''

        mycursor.execute(sql, (id_commande,id_client))
        chaussures_commande = mycursor.fetchall()

        if len(chaussures_commande) == 0:
            flash("commande non existante ou commande ne vous appartenant pas", "alert-warning")

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , chaussures_commande=chaussures_commande
                           , commande_adresses=commande_adresses
                           )
