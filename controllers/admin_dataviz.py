#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, session
from connexion_db import get_db

admin_datavis = Blueprint('admin_datavis', __name__, template_folder='templates')

@admin_datavis.route('/admin/datavis/show')
def show_datavis():
    mycursor = get_db().cursor()

    sql = '''
        SELECT 
            LEFT(a.code_postal, 2) AS departement,
            COUNT(c.id_commande) AS nb_ventes,
            SUM(lc.prix * lc.quantite) AS chiffre_affaire
        FROM commande c
        JOIN adresse a ON c.adresse_livraison_id = a.id_adresse
        JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        GROUP BY departement
        ORDER BY chiffre_affaire DESC
    '''
    mycursor.execute(sql)
    stats_dep = mycursor.fetchall()

    labels = [str(d['departement']) for d in stats_dep]
    data_ventes = [d['nb_ventes'] for d in stats_dep]
    data_ca = [float(d['chiffre_affaire']) for d in stats_dep]

    return render_template('admin/datavis/dataviz_adresse.html',
                           stats_dep=stats_dep,
                           labels=labels,
                           data_ventes=data_ventes,
                           data_ca=data_ca)