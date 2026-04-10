#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_chaussure = Blueprint('admin_declinaison_chaussure', __name__,
                         template_folder='templates')


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/add')
def add_declinaison_chaussure():
    id_chaussure=request.args.get('id_chaussure')
    mycursor = get_db().cursor()





    sql=''' SELECT chaussure.id_chaussure,
            chaussure.photo as image
            FROM chaussure
            WHERE chaussure.id_chaussure=%s'''
    mycursor.execute(sql, (id_chaussure,))
    chaussure=mycursor.fetchone()



    sql = '''   SELECT COUNT(*) as nb
                FROM declinaison_chaussure
                JOIN taille ON declinaison_chaussure.taille_id = taille.id_taille
                WHERE declinaison_chaussure.chaussure_id = %s
                AND taille.id_taille = 1
                AND declinaison_chaussure.disponible=TRUE'''
    mycursor.execute(sql, (id_chaussure,))
    d_taille_uniq = 1 if mycursor.fetchone()['nb'] > 0 else 0


    sql = '''   SELECT COUNT(*) as nb
                FROM declinaison_chaussure
                JOIN couleur ON declinaison_chaussure.couleur_id = couleur.id_couleur
                WHERE declinaison_chaussure.chaussure_id = %s
                AND couleur.id_couleur = 1
                AND declinaison_chaussure.disponible=TRUE'''
    mycursor.execute(sql, (id_chaussure,))
    d_couleur_uniq = 1 if mycursor.fetchone()['nb'] > 0 else 0

    sql=''' SELECT COUNT(id_declinaison_chaussure) as nbr
            FROM declinaison_chaussure 
            WHERE declinaison_chaussure.chaussure_id=%s
            AND disponible=TRUE'''
    mycursor.execute(sql,(id_chaussure,))
    nbr_declinaisons=mycursor.fetchone()['nbr']





    sql=''' SELECT id_couleur,
            libelle 
            FROM couleur
            '''

    if  nbr_declinaisons!=0 and d_couleur_uniq!=1:
        sql+=" WHERE id_couleur != 1"
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()

    print(sql)
    sql=''' SELECT id_taille,
            libelle 
            FROM taille
        '''

    if  nbr_declinaisons!=0 and d_taille_uniq!=1:
        sql+=" WHERE id_taille != 1"

    mycursor.execute(sql)
    tailles=mycursor.fetchall()





    return render_template('admin/chaussure/add_declinaison_chaussure.html'
                           , chaussure=chaussure
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/add', methods=['POST'])
def valid_add_declinaison_chaussure():
    mycursor = get_db().cursor()

    id_chaussure = request.form.get('id_chaussure')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')

    sql=''' SELECT declinaison_chaussure.id_declinaison_chaussure
            FROM declinaison_chaussure
            WHERE declinaison_chaussure.taille_id=%s 
            AND declinaison_chaussure.couleur_id=%s
            AND declinaison_chaussure.chaussure_id=%s
            AND declinaison_chaussure.disponible=TRUE'''
    mycursor.execute(sql,(taille,couleur,id_chaussure))
    doublon=mycursor.fetchall()
    if len(doublon)>=1:



        sql=''' UPDATE declinaison_chaussure
                SET declinaison_chaussure.stock=%s
                WHERE declinaison_chaussure.couleur_id=%s 
                AND declinaison_chaussure.taille_id=%s
                AND declinaison_chaussure.chaussure_id=%s
                AND declinaison_chaussure.disponible=TRUE'''
        mycursor.execute(sql, (stock,couleur,taille,id_chaussure))
        flash('déclinaison déja existante, seul le stock de la déclinaison a été modifié', 'alert-warning')
    else:

        sql=''' SELECT prix_chaussure 
                FROM chaussure
                WHERE chaussure.id_chaussure=%s'''
        mycursor.execute(sql,(id_chaussure,))
        prix=mycursor.fetchone()['prix_chaussure']


        sql=''' INSERT INTO declinaison_chaussure (stock,chaussure_id,taille_id,couleur_id,prix_declinaison)
                VALUES (%s,%s,%s,%s,%s)'''
        mycursor.execute(sql, (stock,id_chaussure,taille,couleur,prix))
        flash('déclinaison ajoutée, taille_id = '+str(taille)+' - couleur_id : '+str(couleur)+' - stock : '+str(stock), 'alert-success')

    get_db().commit()
    return redirect('/admin/chaussure/edit?id_chaussure=' + id_chaussure)


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/edit', methods=['GET'])
def edit_declinaison_chaussure():
    id_declinaison_chaussure = request.args.get('id_declinaison_chaussure')
    mycursor = get_db().cursor()

    sql=''' SELECT declinaison_chaussure.id_declinaison_chaussure,
            declinaison_chaussure.chaussure_id,
            declinaison_chaussure.stock,
            declinaison_chaussure.taille_id,
            declinaison_chaussure.couleur_id,
            chaussure.nom_chaussure as nom,
            chaussure.photo as image_chaussure
            FROM declinaison_chaussure
            JOIN chaussure 
            ON declinaison_chaussure.chaussure_id=chaussure.id_chaussure
            WHERE declinaison_chaussure.id_declinaison_chaussure=%s
            AND declinaison_chaussure.disponible=TRUE'''
    mycursor.execute(sql,(id_declinaison_chaussure,))
    declinaison_chaussure=mycursor.fetchone()


    d_taille_uniq=1 if declinaison_chaussure['taille_id']==1 else 0
    d_couleur_uniq=1 if declinaison_chaussure['couleur_id']==1 else 0


    sql=''' SELECT COUNT(id_declinaison_chaussure) as nbr
            FROM declinaison_chaussure
            WHERE declinaison_chaussure.chaussure_id=(  SELECT d2.chaussure_id
                                                        FROM declinaison_chaussure AS d2
                                                        WHERE d2.id_declinaison_chaussure=%s
            )
            AND disponible=TRUE'''
    mycursor.execute(sql,(id_declinaison_chaussure,))
    nbr_declinaisons=mycursor.fetchone()['nbr']

    print(nbr_declinaisons," ",str(d_taille_uniq),"-"*100)

    sql=''' SELECT id_couleur,
            libelle 
            FROM couleur
            '''

    if d_couleur_uniq==0 and nbr_declinaisons>1:
        sql+=" WHERE id_couleur != 1"
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()

    sql=''' SELECT id_taille,
            libelle 
            FROM taille
        '''

    if d_taille_uniq==0 and nbr_declinaisons>1:
        sql+=" WHERE id_taille != 1"
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    print(declinaison_chaussure)


    return render_template('admin/chaussure/edit_declinaison_chaussure.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_chaussure=declinaison_chaussure
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/edit', methods=['POST'])
def valid_edit_declinaison_chaussure():
    id_declinaison_chaussure = request.form.get('id_declinaison_chaussure','')
    id_chaussure = request.form.get('id_chaussure','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    sql = '''SELECT COUNT(*) as nb 
             FROM ligne_commande
             WHERE declinaison_chaussure_id = %s
             '''
    mycursor.execute(sql, (id_declinaison_chaussure,))
    compte = mycursor.fetchone()['nb']

    sql='''SELECT COUNT(*) as nb FROM ligne_panier
            WHERE ligne_panier.declinaison_chaussure_id=%s'''
    mycursor.execute(sql, (id_declinaison_chaussure,))
    compte+= int(mycursor.fetchone()['nb'] )
    if compte==0:

        sql=''' UPDATE declinaison_chaussure
                SET declinaison_chaussure.disponible=FALSE
                WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''

        mycursor.execute(sql, (id_declinaison_chaussure,))

        sql = '''INSERT INTO declinaison_chaussure (stock, taille_id, couleur_id, chaussure_id, disponible)
                 VALUES (%s, %s, %s, %s, TRUE)'''
        mycursor.execute(sql, (stock, taille_id, couleur_id, id_chaussure))


        flash(u'declinaison déja commandée, l\'ancienne déclinaison a été rendu indisponible, id_declinaison_chaussure : ' + str(id_declinaison_chaussure), 'alert-success')
    else:
        sql = '''   UPDATE declinaison_chaussure
                    SET stock = %s, 
                    taille_id = %s, 
                    couleur_id = %s
                    WHERE id_declinaison_chaussure = %s'''
        mycursor.execute(sql, (stock, taille_id, couleur_id, id_declinaison_chaussure))
        message = u'declinaison_chaussure modifié , id:' + str(id_declinaison_chaussure) + '- stock :' + str(
            stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
        flash(message, 'alert-success')
    get_db().commit()
    return redirect('/admin/chaussure/edit?id_chaussure=' + str(id_chaussure))


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/delete', methods=['GET'])
def admin_delete_declinaison_chaussure():
    id_declinaison_chaussure = request.args.get('id_declinaison_chaussure','')
    id_chaussure = request.args.get('id_chaussure','')
    mycursor = get_db().cursor()

    sql=''' SELECT COUNT(*) as nb FROM ligne_commande
            WHERE ligne_commande.declinaison_chaussure_id=%s'''

    mycursor.execute(sql, (id_declinaison_chaussure,))
    compte = int(mycursor.fetchone()['nb'] )

    sql='''SELECT COUNT(*) as nb FROM ligne_panier
            WHERE ligne_panier.declinaison_chaussure_id=%s'''
    mycursor.execute(sql, (id_declinaison_chaussure,))
    compte+= int(mycursor.fetchone()['nb'] )

    if compte==0:
        sql=''' DELETE FROM declinaison_chaussure
                WHERE declinaison_chaussure.id_declinaison_chaussure=%s '''
        flash(u'declinaison supprimée, id_declinaison_chaussure : ' + str(id_declinaison_chaussure), 'alert-success')
        mycursor.execute(sql,(id_declinaison_chaussure,))
    else:
        sql='''UPDATE declinaison_chaussure
               SET declinaison_chaussure.disponible=FALSE
                WHERE declinaison_chaussure.id_declinaison_chaussure=%s '''
        mycursor.execute(sql,(id_declinaison_chaussure,))
        flash(u'declinaison déja dans une commande ou dans une ligne de panier, la déclinaison a été rendu indispoible, id_declinaison_chaussure : ' + str(id_declinaison_chaussure), 'alert-success')

    get_db().commit()


    return redirect('/admin/chaussure/edit?id_chaussure=' + str(id_chaussure))
