#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_chaussure = Blueprint('admin_type_chaussure', __name__,
                        template_folder='templates')

@admin_type_chaussure.route('/admin/type-chaussure/show')
def show_type_chaussure():
    mycursor = get_db().cursor()
    # sql = '''         '''
    # mycursor.execute(sql)
    # types_chaussure = mycursor.fetchall()
    types_chaussure=[]
    return render_template('admin/type_chaussure/show_type_chaussure.html', types_chaussure=types_chaussure)

@admin_type_chaussure.route('/admin/type-chaussure/add', methods=['GET'])
def add_type_chaussure():
    return render_template('admin/type_chaussure/add_type_chaussure.html')

@admin_type_chaussure.route('/admin/type-chaussure/add', methods=['POST'])
def valid_add_type_chaussure():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''         '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-chaussure/show') #url_for('show_type_chaussure')

@admin_type_chaussure.route('/admin/type-chaussure/delete', methods=['GET'])
def delete_type_chaussure():
    id_type_chaussure = request.args.get('id_type_chaussure', '')
    mycursor = get_db().cursor()

    flash(u'suppression type chaussure , id : ' + id_type_chaussure, 'alert-success')
    return redirect('/admin/type-chaussure/show')

@admin_type_chaussure.route('/admin/type-chaussure/edit', methods=['GET'])
def edit_type_chaussure():
    id_type_chaussure = request.args.get('id_type_chaussure', '')
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, (id_type_chaussure,))
    type_chaussure = mycursor.fetchone()
    return render_template('admin/type_chaussure/edit_type_chaussure.html', type_chaussure=type_chaussure)

@admin_type_chaussure.route('/admin/type-chaussure/edit', methods=['POST'])
def valid_edit_type_chaussure():
    libelle = request.form['libelle']
    id_type_chaussure = request.form.get('id_type_chaussure', '')
    tuple_update = (libelle, id_type_chaussure)
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type chaussure modifié, id: ' + id_type_chaussure + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-chaussure/show')








