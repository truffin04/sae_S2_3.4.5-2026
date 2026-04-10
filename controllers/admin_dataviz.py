#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_chaussure_stock():
    mycursor = get_db().cursor()
    sql = '''   SELECT type_chaussure.libelle_type_chaussure as libelle,
                type_chaussure.id_type_chaussure,
                COUNT(chaussure.id_chaussure) as nbr_chaussures,
                SUM(declinaison_chaussure.stock) as nbr_chaussures_stock
                FROM type_chaussure
                LEFT JOIN chaussure
                ON type_chaussure.id_type_chaussure = chaussure.type_chaussure_id
                JOIN declinaison_chaussure
                ON chaussure.id_chaussure=declinaison_chaussure.chaussure_id
                GROUP BY type_chaussure.id_type_chaussure, type_chaussure.libelle_type_chaussure
                ORDER BY nbr_chaussures DESC
           '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['libelle']) for row in datas_show]
    values = [int(row['nbr_chaussures']) for row in datas_show]

    print(datas_show)

    sql = '''   SELECT chaussure.nom_chaussure, SUM(ligne_commande.quantite) as total_vendu FROM chaussure
                JOIN declinaison_chaussure ON chaussure.id_chaussure = declinaison_chaussure.chaussure_id
                JOIN ligne_commande ON declinaison_chaussure.id_declinaison_chaussure = ligne_commande.declinaison_chaussure_id
                GROUP BY chaussure.nom_chaussure
                HAVING total_vendu> (
                SELECT AVG(vente_par_chaussure)
                FROM (
                         SELECT SUM(ligne_commande.quantite) AS vente_par_chaussure
                         FROM chaussure
                                  JOIN declinaison_chaussure
                                       ON chaussure.id_chaussure = declinaison_chaussure.chaussure_id
                                  JOIN ligne_commande
                                       ON declinaison_chaussure.id_declinaison_chaussure = ligne_commande.declinaison_chaussure_id
                         GROUP BY chaussure.id_chaussure
                     ) as moyenne_ventes_chaussure)
                ORDER BY total_vendu DESC
           '''
    mycursor.execute(sql)
    datas_show2=mycursor.fetchall()

    labels2 = [str(row['nom_chaussure']) for row in datas_show2]
    values2 = [float(row['total_vendu']) for row in datas_show2]


    sql=''''''

    print(len(labels2), len(values2))

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , types_chaussures_nb=datas_show
                           , labels=labels
                           , values=values
                           , labels2=labels2,
                            values2=values2)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


