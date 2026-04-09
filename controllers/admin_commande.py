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


@admin_commande.route('/admin/commande/show', methods=['GET', 'POST'])
def admin_commande_show():
    mycursor = get_db().cursor()

    sql_commandes = '''SELECT
        utilisateur.login,
        commande.id_commande,
        commande.date_achat,
        COUNT(ligne_commande.chaussure_id) AS nbr_chaussures,
        SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total,
        etat.libelle AS libelle,
        commande.etat_id
    FROM commande
    JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
    JOIN ligne_commande ON ligne_commande.commande_id = commande.id_commande
    JOIN etat ON commande.etat_id = etat.id_etat
    GROUP BY commande.id_commande, utilisateur.login, commande.date_achat, etat.libelle, commande.etat_id
    ORDER BY commande.date_achat DESC'''

    mycursor.execute(sql_commandes)
    commandes = mycursor.fetchall()

    chaussures_commande = None
    commande_adresses   = None
    id_commande = request.args.get('id_commande', None)

    if id_commande is not None:
        sql_details = '''SELECT
                c.nom_chaussure AS nom,
                lc.quantite,
                lc.prix,
                (lc.quantite * lc.prix) AS prix_ligne,
                lc.commande_id AS id,
                commande.etat_id,
                c.id_chaussure
            FROM ligne_commande lc
            JOIN commande ON lc.commande_id = commande.id_commande
            JOIN chaussure c ON lc.chaussure_id = c.id_chaussure
            WHERE commande.id_commande = %s
            GROUP BY lc.chaussure_id, lc.quantite, lc.prix, commande.id_commande,
                     commande.etat_id, c.nom_chaussure, c.id_chaussure'''
        mycursor.execute(sql_details, (id_commande,))
        chaussures_commande = mycursor.fetchall()

        # Récupère les adresses de livraison et facturation de la commande
        sql_adr = '''SELECT
                         al.nom       AS liv_nom,
                         al.rue       AS liv_rue,
                         al.code_postal AS liv_cp,
                         al.ville     AS liv_ville,
                         af.nom       AS fac_nom,
                         af.rue       AS fac_rue,
                         af.code_postal AS fac_cp,
                         af.ville     AS fac_ville,
                         commande.adresse_livraison_id,
                         commande.adresse_facturation_id
                     FROM commande
                     LEFT JOIN adresse al ON commande.adresse_livraison_id  = al.id_adresse
                     LEFT JOIN adresse af ON commande.adresse_facturation_id = af.id_adresse
                     WHERE commande.id_commande = %s'''
        mycursor.execute(sql_adr, (id_commande,))
        commande_adresses = mycursor.fetchone()

    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           chaussures_commande=chaussures_commande,
                           commande_adresses=commande_adresses)


@admin_commande.route('/admin/commande/valider', methods=['GET', 'POST'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id is not None:
        sql = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s'''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
        flash('Commande validée', 'success')
    return redirect('/admin/commande/show')