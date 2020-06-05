# import du module d'accès à la base de données
import sqlite3
# Ouverture d'une connexion avec la base de données
from zipfile import ZipFile
import json

def get_info_zip(country):
    with ZipFile('{}.zip'.format('europe'),'r') as z:
    
        # infobox du pays
        return json.loads(z.read('{}.json'.format(country)))

conn = sqlite3.connect('base_donnees.sqlite')

def add_country(conn,country):
    # préparation de la commande SQL
    c = conn.cursor()
    sql = 'INSERT OR REPLACE INTO countries VALUES (?, ?, ?, ?, ?)'
    info=get_info_zip(country)

    # les infos à enregistrer
    name = get_name(info)
    capital = get_capital(info)
    coords = get_coords(info)

    # soumission de la commande (noter que le second argument est un tuple)
    c.execute(sql,(country, name, capital, coords['lat'],coords['lon']))
    conn.commit()
