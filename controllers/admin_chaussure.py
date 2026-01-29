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
    sql = '''  requête admin_chaussure_1
    '''
    mycursor.execute(sql)
    chaussures = mycursor.fetchall()
    return render_template('admin/chaussure/show_chaussure.html', chaussures=chaussures)


@admin_chaussure.route('/admin/chaussure/add', methods=['GET'])
def add_chaussure():
    mycursor = get_db().cursor()

    return render_template('admin/chaussure/add_chaussure.html'
                           #,types_chaussure=type_chaussure,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_chaussure.route('/admin/chaussure/add', methods=['POST'])
def valid_add_chaussure():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_chaussure_id = request.form.get('type_chaussure_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_chaussure_2 '''

    tuple_add = (nom, filename, prix, type_chaussure_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'chaussure ajouté , nom: ', nom, ' - type_chaussure:', type_chaussure_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'chaussure ajouté , nom:' + nom + '- type_chaussure:' + type_chaussure_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/chaussure/show')


@admin_chaussure.route('/admin/chaussure/delete', methods=['GET'])
def delete_chaussure():
    id_chaussure=request.args.get('id_chaussure')
    mycursor = get_db().cursor()
    sql = ''' requête admin_chaussure_3 '''
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
    requête admin_chaussure_6    
    '''
    mycursor.execute(sql, id_chaussure)
    chaussure = mycursor.fetchone()
    print(chaussure)
    sql = '''
    requête admin_chaussure_7
    '''
    mycursor.execute(sql)
    types_chaussure = mycursor.fetchall()

    # sql = '''
    # requête admin_chaussure_6
    # '''
    # mycursor.execute(sql, id_chaussure)
    # declinaisons_chaussure = mycursor.fetchall()

    return render_template('admin/chaussure/edit_chaussure.html'
                           ,chaussure=chaussure
                           ,types_chaussure=types_chaussure
                         #  ,declinaisons_chaussure=declinaisons_chaussure
                           )


@admin_chaussure.route('/admin/chaussure/edit', methods=['POST'])
def valid_edit_chaussure():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_chaussure = request.form.get('id_chaussure')
    image = request.files.get('image', '')
    type_chaussure_id = request.form.get('type_chaussure_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_chaussure_8
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

    sql = '''  requête admin_chaussure_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_chaussure_id, description, id_chaussure))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'chaussure modifié , nom:' + nom + '- type_chaussure :' + type_chaussure_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
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
