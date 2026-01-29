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
    chaussure=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
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
    # attention au doublon
    get_db().commit()
    return redirect('/admin/chaussure/edit?id_chaussure=' + id_chaussure)


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/edit', methods=['GET'])
def edit_declinaison_chaussure():
    id_declinaison_chaussure = request.args.get('id_declinaison_chaussure')
    mycursor = get_db().cursor()
    declinaison_chaussure=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
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

    message = u'declinaison_chaussure modifié , id:' + str(id_declinaison_chaussure) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/chaussure/edit?id_chaussure=' + str(id_chaussure))


@admin_declinaison_chaussure.route('/admin/declinaison_chaussure/delete', methods=['GET'])
def admin_delete_declinaison_chaussure():
    id_declinaison_chaussure = request.args.get('id_declinaison_chaussure','')
    id_chaussure = request.args.get('id_chaussure','')

    flash(u'declinaison supprimée, id_declinaison_chaussure : ' + str(id_declinaison_chaussure),  'alert-success')
    return redirect('/admin/chaussure/edit?id_chaussure=' + str(id_chaussure))
