#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql_commandes = '''  SELECT
    utilisateur.login,
    commande.id_commande,
    commande.date_achat,
    COUNT(ligne_commande.declinaison_chaussure_id) AS nbr_chaussures,
    SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total,
    etat.libelle AS libelle,
    commande.etat_id
FROM commande
JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
JOIN ligne_commande ON ligne_commande.commande_id = commande.id_commande
JOIN etat ON commande.etat_id = etat.id_etat
GROUP BY commande.id_commande, utilisateur.login, commande.date_achat, etat.libelle, commande.etat_id
ORDER BY commande.etat_id,commande.date_achat DESC;
 '''



    mycursor.execute(sql_commandes)
    commandes = mycursor.fetchall()

    chaussures_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande is not None:
        sql_details = '''   SELECT
                            chaussure.nom_chaussure AS nom,
                            ligne_commande.quantite,
                            ligne_commande.prix,
                            (ligne_commande.quantite * ligne_commande.prix) AS prix_ligne,
                            ligne_commande.commande_id AS id,
                            commande.etat_id,
                            taille.id_taille,
                            taille.libelle as libelle_taille,
                            couleur.id_couleur,
                            couleur.libelle as libelle_couleur,
                            (
                                SELECT COUNT(*) 
                                FROM declinaison_chaussure 
                                WHERE declinaison_chaussure.chaussure_id = chaussure.id_chaussure
                                AND declinaison_chaussure.disponible = TRUE
                            ) as nb_declinaisons
                            FROM ligne_commande 
                            JOIN commande ON ligne_commande.commande_id = commande.id_commande
                            JOIN declinaison_chaussure ON ligne_commande.declinaison_chaussure_id = declinaison_chaussure.id_declinaison_chaussure
                            JOIN chaussure ON declinaison_chaussure.chaussure_id = chaussure.id_chaussure
                            JOIN taille ON declinaison_chaussure.taille_id = taille.id_taille
                            JOIN couleur ON declinaison_chaussure.couleur_id = couleur.id_couleur
                            WHERE commande.id_commande = %s '''

        sql_adresse = '''          SELECT a1.nom as nom_livraison,
           a1.rue as rue_livraison,
           a1.code_postal as code_postal_livraison,
           a1.ville as ville_livraison,
           a2.nom as nom_facturation,
           a2.rue as rue_facturation,
           a2.code_postal as code_postal_facturation,
           a2.ville as ville_facturation
            FROM adresse a1
            JOIN commande ON commande.adresse_livraison_id = a1.id_adresse
             JOIN adresse a2 ON a2.id_adresse = commande.adresse_facturation_id
                                WHERE commande.id_commande = %s
                            '''

        mycursor.execute(sql_details, (id_commande,))
        chaussures_commande = mycursor.fetchall()

        mycursor.execute(sql_adresse, (id_commande,))
        commande_adresses = mycursor.fetchall()

    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , chaussures_commande=chaussures_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''      UPDATE commande
            SET etat_id = 2
            WHERE id_commande = %s;     '''
        mycursor.execute(sql, commande_id)
        get_db().commit()
        flash('Commande validée','success')
    return redirect('/admin/commande/show')
