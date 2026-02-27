#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, abort, flash, session

from connexion_db import get_db

client_commentaire = Blueprint('client_commentaire', __name__, template_folder='templates')

@client_commentaire.route('/client/chaussure/details', methods=['GET'])
def client_chaussure_details():
    mycursor = get_db().cursor()
    id_chaussure = request.args.get('id_chaussure', None)
    id_client = session['id_user']

    # Récupérer les informations de la chaussure
    sql_chaussure = '''
        SELECT c.id_chaussure, c.nom_chaussure AS nom, c.prix_chaussure AS prix, c.photo AS image, c.description
        FROM chaussure c
        WHERE c.id_chaussure = %s
    '''
    mycursor.execute(sql_chaussure, (id_chaussure,))
    chaussure = mycursor.fetchone()

    if chaussure is None:
        abort(404, "Problème avec l'ID de la chaussure")

    # Récupérer les commentaires de la chaussure
    sql_commentaires = '''
        SELECT u.nom, u.id_utilisateur, c.commentaire, c.date_publication, c.valider
        FROM commentaire c
        JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
        WHERE c.chaussure_id = %s
        ORDER BY c.date_publication DESC
    '''
    mycursor.execute(sql_commentaires, (id_chaussure,))
    commentaires = mycursor.fetchall()

    # Récupérer le nombre de commandes de cette chaussure par le client
    sql_commandes_chaussures = '''
        SELECT COUNT(lc.chaussure_id) AS nb_commandes_chaussure
        FROM ligne_commande lc
        JOIN commande co ON lc.commande_id = co.id_commande
        WHERE co.utilisateur_id = %s AND lc.chaussure_id = %s
    '''
    mycursor.execute(sql_commandes_chaussures, (id_client, id_chaussure))
    commandes_chaussures = mycursor.fetchone()

    # Récupérer la note du client pour cette chaussure
    sql_note = '''
        SELECT note
        FROM note
        WHERE utilisateur_id = %s AND chaussure_id = %s
    '''
    mycursor.execute(sql_note, (id_client, id_chaussure))
    note = mycursor.fetchone()
    if note:
        note = note['note']

    # Récupérer le nombre de commentaires (total, utilisateur, validés)
    sql_nb_commentaires = '''
        SELECT
            (SELECT COUNT(*) FROM commentaire WHERE chaussure_id = %s) AS nb_commentaires_total,
            (SELECT COUNT(*) FROM commentaire WHERE utilisateur_id = %s AND chaussure_id = %s) AS nb_commentaires_utilisateur,
            (SELECT COUNT(*) FROM commentaire WHERE valider = 1 AND chaussure_id = %s) AS nb_commentaires_total_valide,
            (SELECT COUNT(*) FROM commentaire WHERE utilisateur_id = %s AND chaussure_id = %s AND valider = 1) AS nb_commentaires_utilisateur_valide
    '''
    mycursor.execute(sql_nb_commentaires, (id_chaussure, id_client, id_chaussure, id_chaussure, id_client, id_chaussure))
    nb_commentaires = mycursor.fetchone()

    return render_template('client/chaussure_info/chaussure_details.html',
                           chaussure=chaussure,
                           commentaires=commentaires,
                           commandes_chaussures=commandes_chaussures,
                           note=note,
                           nb_commentaires=nb_commentaires)

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_chaussure = request.form.get('id_chaussure', None)

    if commentaire == '':
        flash(u'Commentaire non pris en compte')
        return redirect('/client/chaussure/details?id_chaussure=' + id_chaussure)

    if commentaire is not None and len(commentaire) > 0 and len(commentaire) < 3:
        flash(u'Le commentaire doit contenir plus de 2 caractères', 'alert-warning')
        return redirect('/client/chaussure/details?id_chaussure=' + id_chaussure)

    tuple_insert = (commentaire, id_client, id_chaussure)
    sql = '''
        INSERT INTO commentaire (commentaire, utilisateur_id, chaussure_id, date_publication, valider)
        VALUES (%s, %s, %s, NOW(), 0)
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/chaussure/details?id_chaussure=' + id_chaussure)

@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_chaussure = request.form.get('id_chaussure', None)
    date_publication = request.form.get('date_publication', None)

    sql = '''
        DELETE FROM commentaire
        WHERE utilisateur_id = %s AND chaussure_id = %s AND date_publication = %s
    '''
    tuple_delete = (id_client, id_chaussure, date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/chaussure/details?id_chaussure=' + id_chaussure)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_chaussure = request.form.get('id_chaussure', None)

    tuple_insert = (note, id_client, id_chaussure)
    sql = '''
        INSERT INTO note (note, utilisateur_id, chaussure_id)
        VALUES (%s, %s, %s)
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/chaussure/details?id_chaussure=' + id_chaussure)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_chaussure = request.form.get('id_chaussure', None)

    tuple_update = (note, id_client, id_chaussure)
    sql = '''
        UPDATE note
        SET note = %s
        WHERE utilisateur_id = %s AND chaussure_id = %s
    '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/chaussure/details?id_chaussure=' + id_chaussure)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_chaussure = request.form.get('id_chaussure', None)

    tuple_delete = (id_client, id_chaussure)
    sql = '''
        DELETE FROM note
        WHERE utilisateur_id = %s AND chaussure_id = %s
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/chaussure/details?id_chaussure=' + id_chaussure)
