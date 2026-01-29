#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_chaussure = Blueprint('client_chaussure', __name__,
                        template_folder='templates')

@client_chaussure.route('/client/index')
@client_chaussure.route('/client/chaussure/show')              # remplace /client
def client_chaussure_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''   selection des chaussures   '''
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    chaussures =[]


    # pour le filtre
    types_chaussure = []


    chaussures_panier = []

    if len(chaussures_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_chaussure.html'
                           , chaussures=chaussures
                           , chaussures_panier=chaussures_panier
                           #, prix_total=prix_total
                           , items_filtre=types_chaussure
                           )
