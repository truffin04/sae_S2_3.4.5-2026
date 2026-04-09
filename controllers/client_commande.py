#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/valide_refresh', methods=['GET'])
def client_commande_valide_refresh():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT ligne_panier.chaussure_id, ligne_panier.quantite, chaussure.prix_chaussure as prix, chaussure.nom_chaussure as nom FROM ligne_panier JOIN chaussure ON ligne_panier.chaussure_id = chaussure.id_chaussure WHERE ligne_panier.utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    chaussures_panier = mycursor.fetchall()
    if len(chaussures_panier) >= 1:
        sql2 = '''SELECT SUM(chaussure.prix_chaussure * ligne_panier.quantite) as prix_total FROM ligne_panier JOIN chaussure ON ligne_panier.chaussure_id = chaussure.id_chaussure WHERE ligne_panier.utilisateur_id = %s'''
        mycursor.execute(sql2, (id_client,))
        prix_dict = mycursor.fetchone()
        prix_total = prix_dict['prix_total']
    else:
        prix_total = 0
    sql3 = '''SELECT id_adresse, nom, rue, code_postal, ville, favori FROM adresse WHERE utilisateur_id = %s AND valide = 1 ORDER BY favori DESC'''
    mycursor.execute(sql3, (id_client,))
    adresses = mycursor.fetchall()
    sql4 = '''SELECT id_adresse FROM adresse WHERE utilisateur_id = %s AND valide = 1 AND favori = 1 LIMIT 1'''
    mycursor.execute(sql4, (id_client,))
    fav = mycursor.fetchone()
    id_adresse_fav = fav['id_adresse'] if fav else 0
    adresse_identique = request.args.get('identique', None)
    return render_template('client/boutique/panier_validation_adresses.html', adresses=adresses, chaussures_panier=chaussures_panier, prix_total=prix_total, validation=1, id_adresse_fav=id_adresse_fav, adresse_identique=adresse_identique)


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT ligne_panier.chaussure_id, ligne_panier.quantite,
                    chaussure.prix_chaussure as prix, chaussure.nom_chaussure as nom
             FROM ligne_panier
             JOIN chaussure ON ligne_panier.chaussure_id = chaussure.id_chaussure
             WHERE ligne_panier.utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    chaussures_panier = mycursor.fetchall()

    if len(chaussures_panier) >= 1:
        sql = '''SELECT SUM(chaussure.prix_chaussure * ligne_panier.quantite) as prix_total
                 FROM ligne_panier
                 JOIN chaussure ON ligne_panier.chaussure_id = chaussure.id_chaussure
                 WHERE ligne_panier.utilisateur_id = %s'''
        mycursor.execute(sql, (id_client,))
        prix_dict = mycursor.fetchone()
        prix_total = prix_dict['prix_total']
    else:
        prix_total = 0

    # Récupère uniquement les adresses valides
    sql = '''SELECT id_adresse, nom, rue, code_postal, ville, favori
             FROM adresse
             WHERE utilisateur_id = %s AND valide = 1
             ORDER BY favori DESC'''
    mycursor.execute(sql, (id_client,))
    adresses = mycursor.fetchall()

    # Récupère l'id de l'adresse favorite
    sql_fav = '''SELECT id_adresse FROM adresse
                 WHERE utilisateur_id = %s AND valide = 1 AND favori = 1
                 LIMIT 1'''
    mycursor.execute(sql_fav, (id_client,))
    fav = mycursor.fetchone()
    id_adresse_fav = fav['id_adresse'] if fav else 0

    # Gestion rechargement page si checkbox "adresse identique" cochée
    adresse_identique = request.form.get('adresse_identique')

    return render_template('client/boutique/panier_validation_adresses.html',
                           adresses=adresses,
                           chaussures_panier=chaussures_panier,
                           prix_total=prix_total,
                           validation=1,
                           id_adresse_fav=id_adresse_fav,
                           adresse_identique=adresse_identique)


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    id_adresse_livraison  = request.form.get('id_adresse_livraison')
    id_adresse_facturation = request.form.get('id_adresse_facturation')
    adresse_identique     = request.form.get('adresse_identique')

    if adresse_identique:
        id_adresse_facturation = id_adresse_livraison

    # Vérifie que les adresses appartiennent bien à l'utilisateur connecté (SQL)
    sql_check_liv = '''SELECT id_adresse FROM adresse
                       WHERE id_adresse = %s AND utilisateur_id = %s AND valide = 1'''
    mycursor.execute(sql_check_liv, (id_adresse_livraison, id_client))
    check_liv = mycursor.fetchone()

    sql_check_fac = '''SELECT id_adresse FROM adresse
                       WHERE id_adresse = %s AND utilisateur_id = %s AND valide = 1'''
    mycursor.execute(sql_check_fac, (id_adresse_facturation, id_client))
    check_fac = mycursor.fetchone()

    if not check_liv or not check_fac:
        flash('Probleme d\'autorisation avec les adresses selectionnees.', 'alert-warning')
        return redirect('/client/chaussure/show')

    sql = '''SELECT ligne_panier.chaussure_id, ligne_panier.quantite, chaussure.prix_chaussure
             FROM ligne_panier
             JOIN chaussure ON ligne_panier.chaussure_id = chaussure.id_chaussure
             WHERE ligne_panier.utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    date_today = datetime.now().strftime('%Y-%m-%d')
    sql = '''INSERT INTO commande(date_achat, utilisateur_id, etat_id, adresse_livraison_id, adresse_facturation_id)
             VALUES (%s, %s, %s, %s, %s)'''
    mycursor.execute(sql, (date_today, id_client, 1, id_adresse_livraison, id_adresse_facturation))

    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    last_id = mycursor.fetchone()
    id_nouvelle_commande = last_id['last_insert_id']

    # Supprime toutes les lignes du panier en une seule requete
    sql_del = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql_del, (id_client,))

    # Insere toutes les lignes de commande en une seule requete
    lignes = [(id_nouvelle_commande, item['chaussure_id'], item['prix_chaussure'], item['quantite'])
              for item in items_ligne_panier]
    sql_ins = '''INSERT INTO ligne_commande VALUES (%s, %s, %s, %s)'''
    mycursor.executemany(sql_ins, lignes)

    # L'adresse de livraison utilisée devient la favorite
    sql_unset = '''UPDATE adresse SET favori = 0 WHERE utilisateur_id = %s'''
    mycursor.execute(sql_unset, (id_client,))
    sql_set_fav = '''UPDATE adresse SET favori = 1 WHERE id_adresse = %s'''
    mycursor.execute(sql_set_fav, (id_adresse_livraison,))

    get_db().commit()
    flash('Commande passee avec succes !', 'alert-success')
    return redirect('/client/chaussure/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT commande.id_commande, commande.date_achat, commande.etat_id,
                    etat.libelle,
                    SUM(ligne_commande.quantite) AS nbr_chaussures,
                    SUM(ligne_commande.quantite * ligne_commande.prix) AS prix_total
             FROM commande
             JOIN etat ON commande.etat_id = etat.id_etat
             JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
             WHERE commande.utilisateur_id = %s
             GROUP BY commande.id_commande, commande.date_achat, commande.etat_id, etat.libelle
             ORDER BY commande.etat_id, commande.date_achat DESC'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    chaussures_commande = None
    commande_adresses   = None
    id_commande = request.args.get('id_commande', None)

    if id_commande is not None:
        sql = '''SELECT chaussure.nom_chaussure AS nom,
                        ligne_commande.quantite,
                        ligne_commande.prix,
                        ligne_commande.quantite * ligne_commande.prix AS prix_ligne
                 FROM ligne_commande
                 JOIN chaussure ON ligne_commande.chaussure_id = chaussure.id_chaussure
                 JOIN commande  ON ligne_commande.commande_id = commande.id_commande
                 WHERE ligne_commande.commande_id = %s
                   AND commande.utilisateur_id = %s'''
        mycursor.execute(sql, (id_commande, id_client))
        chaussures_commande = mycursor.fetchall()

        # Récupère les adresses de livraison et de facturation de la commande
        sql_adr = '''SELECT
                         al.nom AS liv_nom, al.rue AS liv_rue,
                         al.code_postal AS liv_cp, al.ville AS liv_ville,
                         af.nom AS fac_nom, af.rue AS fac_rue,
                         af.code_postal AS fac_cp, af.ville AS fac_ville,
                         commande.adresse_livraison_id,
                         commande.adresse_facturation_id
                     FROM commande
                     LEFT JOIN adresse al ON commande.adresse_livraison_id  = al.id_adresse
                     LEFT JOIN adresse af ON commande.adresse_facturation_id = af.id_adresse
                     WHERE commande.id_commande = %s
                       AND commande.utilisateur_id = %s'''
        mycursor.execute(sql_adr, (id_commande, id_client))
        commande_adresses = mycursor.fetchone()

    return render_template('client/commandes/show.html',
                           commandes=commandes,
                           chaussures_commande=chaussures_commande,
                           commande_adresses=commande_adresses)