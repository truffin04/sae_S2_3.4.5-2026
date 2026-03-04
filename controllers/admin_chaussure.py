#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_chaussure = Blueprint('admin_chaussure', __name__,
                          template_folder='templates')


@admin_chaussure.route('/admin/chaussure/show')
def show_chaussure():
    mycursor = get_db().cursor()
    sql = '''   SELECT chaussure.id_chaussure,
                chaussure.nom_chaussure as nom,
                type_chaussure.libelle_type_chaussure as libelle,
                chaussure.pointure_id,
                pointure.libelle_pointure as  libelle_pointure,
                chaussure.type_chaussure_id,
                chaussure.prix_chaussure as prix,
                chaussure.stock,
                chaussure.photo as image
                FROM chaussure
                JOIN type_chaussure
                on chaussure.type_chaussure_id=type_chaussure.id_type_chaussure
                JOIN pointure 
                ON chaussure.pointure_id=pointure.id_pointure
                
    '''
    mycursor.execute(sql)
    chaussures = mycursor.fetchall()
    return render_template('admin/chaussure/show_chaussure.html', chaussures=chaussures)


@admin_chaussure.route('/admin/chaussure/add', methods=['GET'])
def add_chaussure():
    mycursor = get_db().cursor()
    sql=''' SELECT type_chaussure.id_type_chaussure,
            type_chaussure.libelle_type_chaussure as libelle
            FROM type_chaussure
        '''
    mycursor.execute(sql)
    type_chaussure = mycursor.fetchall()

    # pointures ================================

    sql=''' SELECT pointure.id_pointure,
            pointure.libelle_pointure FROM pointure'''
    mycursor.execute(sql)
    pointures = mycursor.fetchall()

    #===========================================


    return render_template('admin/chaussure/add_chaussure.html'
                           ,types_chaussure=type_chaussure,
                           pointures=pointures,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_chaussure.route('/admin/chaussure/add', methods=['POST'])
def valid_add_chaussure():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_chaussure_id = request.form.get('type_chaussure_id', '')
    pointure_id = request.form.get('pointure_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')
    stock=request.form.get('stock', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''   INSERT INTO chaussure(nom_chaussure, photo, prix_chaussure,  type_chaussure_id, pointure_id, stock, description)
                VALUES (%s,%s,%s,%s,%s,%s,%s)'''

    tuple_add = (nom, filename, prix, type_chaussure_id,pointure_id, stock, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'chaussure ajouté , nom: ', nom, ' - type_chaussure:', type_chaussure_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'chaussure ajouté , nom:' + nom + '- type_chaussure:' + type_chaussure_id + ' - pointure id:' + pointure_id + ' - prix:' + prix + ' - description:' + description  + ' - stock:'+stock+ ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/chaussure/show')


@admin_chaussure.route('/admin/chaussure/delete', methods=['GET'])
def delete_chaussure():
    id_chaussure=request.args.get('id_chaussure')
    mycursor = get_db().cursor()
    sql = ''' '''
    mycursor.execute(sql, id_chaussure)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet chaussure : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_chaussure_4 '''
        mycursor.execute(sql, id_chaussure)
        chaussure = mycursor.fetchone()
        print(chaussure)
        image = chaussure['image']

        sql = ''' requête admin_chaussure_5  '''
        mycursor.execute(sql, id_chaussure)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un chaussure supprimé, id :", id_chaussure)
        message = u'un chaussure supprimé, id : ' + id_chaussure
        flash(message, 'alert-success')

    return redirect('/admin/chaussure/show')


@admin_chaussure.route('/admin/chaussure/edit', methods=['GET'])
def edit_chaussure():
    id_chaussure=request.args.get('id_chaussure')
    mycursor = get_db().cursor()
    sql = '''
     SELECT chaussure.id_chaussure,
                chaussure.nom_chaussure as nom,
                type_chaussure.libelle_type_chaussure as libelle,
                chaussure.type_chaussure_id,
                chaussure.prix_chaussure as prix,
                chaussure.pointure_id,
                chaussure.stock,
                chaussure.photo as image,
                chaussure.description
                FROM chaussure
                JOIN type_chaussure
                on chaussure.type_chaussure_id=type_chaussure.id_type_chaussure 
                WHERE chaussure.id_chaussure=%s
                
    '''
    mycursor.execute(sql, id_chaussure)
    chaussure = mycursor.fetchone()
    print(chaussure)
    sql = '''
    SELECT type_chaussure.id_type_chaussure,
            type_chaussure.libelle_type_chaussure as libelle
            FROM type_chaussure
    '''
    mycursor.execute(sql)
    types_chaussure = mycursor.fetchall()


    # pointures ================================

    sql=''' SELECT pointure.id_pointure,
            pointure.libelle_pointure FROM pointure'''
    mycursor.execute(sql)
    pointures = mycursor.fetchall()

    #============================================




    # sql = '''
    # requête admin_chaussure_6
    # '''
    # mycursor.execute(sql, id_chaussure)
    # declinaisons_chaussure = mycursor.fetchall()

    return render_template('admin/chaussure/edit_chaussure.html'
                           ,chaussure=chaussure
                           ,types_chaussure=types_chaussure,
                           pointures=pointures
                         #  ,declinaisons_chaussure=declinaisons_chaussure
                           )


@admin_chaussure.route('/admin/chaussure/edit', methods=['POST'])
def valid_edit_chaussure():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_chaussure = request.form.get('id_chaussure')
    image = request.files.get('image', '')
    type_chaussure_id = request.form.get('type_chaussure_id', '')

    pointure_id = request.form.get('pointure_id', '')

    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description')
    sql = '''
        SELECT chaussure.photo as image
        FROM chaussure
        WHERE chaussure.id_chaussure=%s
       '''
    mycursor.execute(sql, id_chaussure)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''   UPDATE chaussure
                SET chaussure.nom_chaussure = %s,
                chaussure.photo = %s ,
                chaussure.prix_chaussure = %s ,
                chaussure.type_chaussure_id = %s ,
                chaussure.pointure_id = %s ,
                chaussure.description = %s,
                chaussure.stock = %s
                WHERE chaussure.id_chaussure = %s'''
    mycursor.execute(sql, (nom, image_nom, prix, type_chaussure_id, pointure_id, description,stock, id_chaussure))

    get_db().commit()
    if image_nom is None:
        image_nom = ''

    message = u'chaussure modifié , nom:' + nom + '- type_chaussure:' + type_chaussure_id + ' - pointure id:'+ pointure_id+  ' - prix:' + prix  + ' - image:' + image_nom + ' - description:' + description + ' - stock:'+stock
    flash(message, 'alert-success')
    return redirect('/admin/chaussure/show')







@admin_chaussure.route('/admin/chaussure/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    chaussure=[]
    commentaires = {}
    return render_template('admin/chaussure/show_avis.html'
                           , chaussure=chaussure
                           , commentaires=commentaires
                           )


@admin_chaussure.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    chaussure_id = request.form.get('idchaussure', None)
    userId = request.form.get('idUser', None)

    return admin_avis(chaussure_id)
