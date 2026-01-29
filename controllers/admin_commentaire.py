#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/chaussure/commentaires', methods=['GET'])
def admin_chaussure_details():
    mycursor = get_db().cursor()
    id_chaussure =  request.args.get('id_chaussure', None)
    sql = '''    requête admin_type_chaussure_1    '''
    commentaires = {}
    sql = '''   requête admin_type_chaussure_1_bis   '''
    chaussure = []
    sql = '''   requête admin_type_chaussure_1_3   '''
    nb_commentaires = []
    return render_template('admin/chaussure/show_chaussure_commentaires.html'
                           , commentaires=commentaires
                           , chaussure=chaussure
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/chaussure/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_chaussure = request.form.get('id_chaussure', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_chaussure_2   '''
    tuple_delete=(id_utilisateur,id_chaussure,date_publication)
    get_db().commit()
    return redirect('/admin/chaussure/commentaires?id_chaussure='+id_chaussure)


@admin_commentaire.route('/admin/chaussure/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_chaussure = request.args.get('id_chaussure', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/chaussure/add_commentaire.html',id_utilisateur=id_utilisateur,id_chaussure=id_chaussure,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_chaussure = request.form.get('id_chaussure', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_chaussure_3   '''
    get_db().commit()
    return redirect('/admin/chaussure/commentaires?id_chaussure='+id_chaussure)


@admin_commentaire.route('/admin/chaussure/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_chaussure = request.args.get('id_chaussure', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_chaussure_4   '''
    get_db().commit()
    return redirect('/admin/chaussure/commentaires?id_chaussure='+id_chaussure)