#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql_utilisateur = '''SELECT login, nom, email FROM utilisateur
                         WHERE id_utilisateur = %s'''
    mycursor.execute(sql_utilisateur, (id_client,))
    utilisateur = mycursor.fetchone()

    sql_adresse = '''SELECT a.id_adresse, a.nom, a.rue, a.code_postal, a.ville,
                            a.favori, a.valide,
                            (SELECT COUNT(*)
                             FROM commande
                             WHERE adresse_livraison_id = a.id_adresse
                                OR adresse_facturation_id = a.id_adresse) AS nbr_commande
                     FROM adresse a
                     WHERE a.utilisateur_id = %s
                     ORDER BY a.favori DESC, nbr_commande DESC'''
    mycursor.execute(sql_adresse, (id_client,))
    adresses = mycursor.fetchall()

    sql_nb = '''SELECT
                    SUM(CASE WHEN valide = 1 THEN 1 ELSE 0 END) AS nb_valides,
                    COUNT(*) AS nb_total
                FROM adresse
                WHERE utilisateur_id = %s'''
    mycursor.execute(sql_nb, (id_client,))
    compteur = mycursor.fetchone()
    nb_adresses_valides = compteur['nb_valides'] if compteur['nb_valides'] else 0
    nb_adresses_total   = compteur['nb_total']   if compteur['nb_total']   else 0

    return render_template('client/coordonnee/show_coordonnee.html',
                           utilisateur=utilisateur,
                           adresses=adresses,
                           nb_adresses=nb_adresses_valides,
                           nb_adresses_tot=nb_adresses_total)


@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT login, nom, email FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()
    return render_template('client/coordonnee/edit_coordonnee.html',
                           utilisateur=utilisateur)


@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom   = request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    sql_doublon = '''SELECT id_utilisateur FROM utilisateur
                     WHERE (login = %s OR email = %s)
                       AND id_utilisateur != %s'''
    mycursor.execute(sql_doublon, (login, email, id_client))
    doublon = mycursor.fetchone()

    if doublon:
        flash('Cet email ou ce login est deja utilise par un autre compte.', 'alert-warning')
        utilisateur = {'login': login, 'nom': nom, 'email': email}
        return render_template('client/coordonnee/edit_coordonnee.html',
                               utilisateur=utilisateur)

    sql_update = '''UPDATE utilisateur
                    SET nom = %s, login = %s, email = %s
                    WHERE id_utilisateur = %s'''
    mycursor.execute(sql_update, (nom, login, email, id_client))
    get_db().commit()
    session['login'] = login
    flash('Vos informations ont ete mises a jour.', 'alert-success')
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/add_adresse', methods=['GET'])
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT login, nom FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()
    return render_template('client/coordonnee/add_adresse.html',
                           utilisateur=utilisateur,
                           nom='', rue='', code_postal='', ville='')


@client_coordonnee.route('/client/coordonnee/add_adresse', methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom         = request.form.get('nom')
    rue         = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville       = request.form.get('ville')

    sql_proprio = '''SELECT id_utilisateur FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sql_proprio, (id_client,))
    proprio = mycursor.fetchone()
    if not proprio:
        flash('Probleme d\'autorisation : utilisateur non reconnu.', 'alert-warning')
        return redirect('/client/coordonnee/show')

    sql_cp = '''SELECT %s REGEXP '^[0-9]{5}$' AS cp_valide'''
    mycursor.execute(sql_cp, (code_postal,))
    res_cp = mycursor.fetchone()
    if not res_cp['cp_valide']:
        sql_u = '''SELECT login, nom FROM utilisateur WHERE id_utilisateur = %s'''
        mycursor.execute(sql_u, (id_client,))
        utilisateur = mycursor.fetchone()
        flash('Le code postal doit etre compose exactement de 5 chiffres.', 'alert-warning')
        return render_template('client/coordonnee/add_adresse.html',
                               utilisateur=utilisateur,
                               nom=nom, rue=rue, code_postal=code_postal, ville=ville)

    sql_max = '''SELECT COUNT(*) AS nb FROM adresse
                 WHERE utilisateur_id = %s AND valide = 1'''
    mycursor.execute(sql_max, (id_client,))
    nb = mycursor.fetchone()['nb']
    if nb >= 4:
        flash('Vous avez atteint le maximum de 4 adresses valides.', 'alert-warning')
        return redirect('/client/coordonnee/show')

    sql_unset_fav = '''UPDATE adresse SET favori = 0 WHERE utilisateur_id = %s'''
    mycursor.execute(sql_unset_fav, (id_client,))

    sql_insert = '''INSERT INTO adresse(nom, rue, code_postal, ville, utilisateur_id, valide, favori)
                    VALUES (%s, %s, %s, %s, %s, 1, 1)'''
    mycursor.execute(sql_insert, (nom, rue, code_postal, ville, id_client))
    get_db().commit()
    flash('Adresse ajoutee avec succes.', 'alert-success')
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/edit_adresse', methods=['GET'])
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client  = session['id_user']
    id_adresse = request.args.get('id_adresse')

    sql_check = '''SELECT a.id_adresse FROM adresse a
                   WHERE a.id_adresse = %s AND a.utilisateur_id = %s AND a.valide = 1'''
    mycursor.execute(sql_check, (id_adresse, id_client))
    adresse_check = mycursor.fetchone()
    if not adresse_check:
        flash('Probleme d\'autorisation : cette adresse ne vous appartient pas ou n\'est pas valide.', 'alert-warning')
        return redirect('/client/coordonnee/show')

    sql_adresse = '''SELECT * FROM adresse WHERE id_adresse = %s'''
    mycursor.execute(sql_adresse, (id_adresse,))
    adresse = mycursor.fetchone()

    sql_u = '''SELECT login, nom FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sql_u, (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/edit_adresse.html',
                           utilisateur=utilisateur,
                           adresse=adresse)


@client_coordonnee.route('/client/coordonnee/edit_adresse', methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client  = session['id_user']
    id_adresse  = request.form.get('id_adresse')
    nom         = request.form.get('nom')
    rue         = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville       = request.form.get('ville')

    sql_check = '''SELECT a.id_adresse, a.favori FROM adresse a
                   WHERE a.id_adresse = %s AND a.utilisateur_id = %s AND a.valide = 1'''
    mycursor.execute(sql_check, (id_adresse, id_client))
    adresse_check = mycursor.fetchone()
    if not adresse_check:
        flash('Probleme d\'autorisation : cette adresse ne vous appartient pas.', 'alert-warning')
        return redirect('/client/coordonnee/show')

    sql_cp = '''SELECT %s REGEXP '^[0-9]{5}$' AS cp_valide'''
    mycursor.execute(sql_cp, (code_postal,))
    res_cp = mycursor.fetchone()
    if not res_cp['cp_valide']:
        sql_adresse = '''SELECT * FROM adresse WHERE id_adresse = %s'''
        mycursor.execute(sql_adresse, (id_adresse,))
        adresse = mycursor.fetchone()
        sql_u = '''SELECT login, nom FROM utilisateur WHERE id_utilisateur = %s'''
        mycursor.execute(sql_u, (id_client,))
        utilisateur = mycursor.fetchone()
        flash('Le code postal doit etre compose exactement de 5 chiffres.', 'alert-warning')
        return render_template('client/coordonnee/edit_adresse.html',
                               utilisateur=utilisateur,
                               adresse=adresse)

    etait_favori = adresse_check['favori']

    sql_used = '''SELECT COUNT(*) AS nb FROM commande
                  WHERE adresse_livraison_id = %s OR adresse_facturation_id = %s'''
    mycursor.execute(sql_used, (id_adresse, id_adresse))
    nb_used = mycursor.fetchone()['nb']

    if nb_used > 0:
        sql_invalide = '''UPDATE adresse SET valide = 0, favori = 0 WHERE id_adresse = %s'''
        mycursor.execute(sql_invalide, (id_adresse,))

        sql_max = '''SELECT COUNT(*) AS nb FROM adresse
                     WHERE utilisateur_id = %s AND valide = 1'''
        mycursor.execute(sql_max, (id_client,))
        nb_val = mycursor.fetchone()['nb']
        if nb_val >= 4:
            get_db().commit()
            flash('Adresse invalidee mais impossible de creer le doublon : maximum de 4 adresses valides atteint.', 'alert-warning')
            return redirect('/client/coordonnee/show')

        if etait_favori:
            sql_unset = '''UPDATE adresse SET favori = 0 WHERE utilisateur_id = %s'''
            mycursor.execute(sql_unset, (id_client,))

        sql_insert = '''INSERT INTO adresse(nom, rue, code_postal, ville, utilisateur_id, valide, favori)
                        VALUES (%s, %s, %s, %s, %s, 1, %s)'''
        mycursor.execute(sql_insert, (nom, rue, code_postal, ville, id_client, etait_favori))
    else:
        if etait_favori:
            sql_unset = '''UPDATE adresse SET favori = 0 WHERE utilisateur_id = %s'''
            mycursor.execute(sql_unset, (id_client,))
        sql_update = '''UPDATE adresse
                        SET nom = %s, rue = %s, code_postal = %s, ville = %s, favori = %s
                        WHERE id_adresse = %s AND utilisateur_id = %s'''
        mycursor.execute(sql_update, (nom, rue, code_postal, ville, etait_favori, id_adresse, id_client))

    get_db().commit()
    flash('Adresse modifiee avec succes.', 'alert-success')
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse', methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client  = session['id_user']
    id_adresse = request.form.get('id_adresse')

    sql_check = '''SELECT a.id_adresse, a.favori FROM adresse a
                   WHERE a.id_adresse = %s AND a.utilisateur_id = %s AND a.valide = 1'''
    mycursor.execute(sql_check, (id_adresse, id_client))
    adresse_check = mycursor.fetchone()
    if not adresse_check:
        flash('Probleme d\'autorisation : cette adresse ne vous appartient pas.', 'alert-warning')
        return redirect('/client/coordonnee/show')

    etait_favori = adresse_check['favori']

    sql_used = '''SELECT COUNT(*) AS nb FROM commande
                  WHERE adresse_livraison_id = %s OR adresse_facturation_id = %s'''
    mycursor.execute(sql_used, (id_adresse, id_adresse))
    nb_used = mycursor.fetchone()['nb']

    if nb_used > 0:
        sql_invalide = '''UPDATE adresse SET valide = 0, favori = 0 WHERE id_adresse = %s'''
        mycursor.execute(sql_invalide, (id_adresse,))
    else:
        sql_delete = '''DELETE FROM adresse WHERE id_adresse = %s'''
        mycursor.execute(sql_delete, (id_adresse,))

    if etait_favori:
        sql_new_fav = '''SELECT a.id_adresse
                         FROM adresse a
                         JOIN commande c ON (c.adresse_livraison_id = a.id_adresse
                                          OR c.adresse_facturation_id = a.id_adresse)
                         WHERE a.utilisateur_id = %s AND a.valide = 1
                         ORDER BY c.date_achat DESC
                         LIMIT 1'''
        mycursor.execute(sql_new_fav, (id_client,))
        new_fav = mycursor.fetchone()
        if new_fav:
            sql_set_fav = '''UPDATE adresse SET favori = 1 WHERE id_adresse = %s'''
            mycursor.execute(sql_set_fav, (new_fav['id_adresse'],))
        else:
            sql_first_val = '''SELECT id_adresse FROM adresse
                               WHERE utilisateur_id = %s AND valide = 1
                               LIMIT 1'''
            mycursor.execute(sql_first_val, (id_client,))
            first_val = mycursor.fetchone()
            if first_val:
                sql_set_fav = '''UPDATE adresse SET favori = 1 WHERE id_adresse = %s'''
                mycursor.execute(sql_set_fav, (first_val['id_adresse'],))

    get_db().commit()
    flash('Adresse supprimee.', 'alert-success')
    return redirect('/client/coordonnee/show')