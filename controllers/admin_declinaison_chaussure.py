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

    sql=''' SELECT id_couleur,
            libelle 
            FROM couleur
            '''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()

    sql=''' SELECT id_taille,
            libelle 
            FROM taille
        '''
    mycursor.execute(sql)
    tailles=mycursor.fetchall()

    sql = '''   SELECT COUNT(*) as nb
                FROM declinaison_chaussure
                JOIN taille ON declinaison_chaussure.taille_id = taille.id_taille
                WHERE declinaison_chaussure.chaussure_id = %s
                AND taille.id_taille = 1'''
    mycursor.execute(sql, (id_chaussure,))
    d_taille_uniq = 1 if mycursor.fetchone()['nb'] > 0 else None


    sql = '''   SELECT COUNT(*) as nb
                FROM declinaison_chaussure
                JOIN couleur ON declinaison_chaussure.couleur_id = couleur.id_couleur
                WHERE declinaison_chaussure.chaussure_id = %s
                AND couleur.id_couleur = 1'''
    mycursor.execute(sql, (id_chaussure,))
    d_couleur_uniq = 1 if mycursor.fetchone()['nb'] > 0 else None


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
            AND declinaison_chaussure.chaussure_id=%s'''
    mycursor.execute(sql,(taille,couleur,id_chaussure))
    doublon=mycursor.fetchall()
    if len(doublon)>=1:
        sql=''' UPDATE declinaison_chaussure
                SET declinaison_chaussure.stock=%s
                WHERE declinaison_chaussure.couleur_id=%s 
                AND declinaison_chaussure.taille_id=%s
                AND declinaison_chaussure.chaussure_id=%s'''
        mycursor.execute(sql, (stock,couleur,taille,id_chaussure))
        flash('déclinaison déja existante, seul le stock de la déclinaison a été modifié', 'alert-warning')
    else:
        sql=''' INSERT INTO declinaison_chaussure (stock,chaussure_id,taille_id,couleur_id)
                VALUES (%s,%s,%s,%s)'''
        mycursor.execute(sql, (stock,id_chaussure,taille,couleur))

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
            WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''
    mycursor.execute(sql,(id_declinaison_chaussure,))
    declinaison_chaussure=mycursor.fetchone()

    sql=''' SELECT id_couleur,
            libelle 
            FROM couleur
            '''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()

    sql=''' SELECT id_taille,
            libelle
            FROM taille'''
    mycursor.execute(sql)
    tailles=mycursor.fetchall()

    print(declinaison_chaussure)

    d_taille_uniq=1 if declinaison_chaussure['taille_id']==1 else 0
    d_couleur_uniq=1 if declinaison_chaussure['couleur_id']==1 else 0
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

    if taille_id and couleur_id:
        sql=''' UPDATE declinaison_chaussure
                SET declinaison_chaussure.stock=%s
                ,declinaison_chaussure.taille_id=%s,
                declinaison_chaussure.couleur_id=%s
                WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''
        mycursor.execute(sql,(stock,taille_id,couleur_id,id_declinaison_chaussure))
    else:
        sql=''' UPDATE declinaison_chaussure
                SET declinaison_chaussure.stock=%s
                WHERE declinaison_chaussure.id_declinaison_chaussure=%s'''
        mycursor.execute(sql,(stock,id_declinaison_chaussure))
    get_db().commit()

    message = u'declinaison_chaussure modifié , id:' + str(id_declinaison_chaussure) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/chaussure/edit?id_chaussure=' + str(id_chaussure))


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/delete', methods=['GET'])
def admin_delete_declinaison_chaussure():
    id_declinaison_chaussure = request.args.get('id_declinaison_chaussure','')
    id_chaussure = request.args.get('id_chaussure','')

    flash(u'declinaison supprimée, id_declinaison_chaussure : ' + str(id_declinaison_chaussure),  'alert-success')
    return redirect('/admin/chaussure/edit?id_chaussure=' + str(id_chaussure))
