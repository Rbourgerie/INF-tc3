import wptools
import sqlite3
from zipfile import ZipFile
import json

def get_info(country):
    with ZipFile('{}.zip'.format('europe'),'r') as z:
        # infobox du pays
        return json.loads(z.read('{}.json'.format(country)))

def get_name(country):
    info=get_info(country)
    if 'conventional_long_name' in info:
        name=info['conventional_long_name']
        return name
    if 'common_name' in info and info['common_name'] == 'Singapore':
        return 'Republic of Singapore'
    
    if 'common_name' in info:
        name=info['common_name']
        print('Using common name :'+name)
        return name
    
    # En cas d'échec
    print('Le nom du pays n\'a pas été trouvé')
    return None

def get_capital(country):
    info=get_info(country)
    if 'capital' in info:
        capital=info['capital'].replace('\n',' ')
        
        # Le nom de la capitale peut comporter des lettres, espaces
        # ou un des caractères: ',.()|- compris entre crochets [[...]]
        m = re.match(".*?\[\[([\w\s',(.)|-]+)\]\]",capital)
        capital=m.group(1)
        
        return capital
    
    # En cas d'échec
    print('Impossible de trouver la capitale')
    return None

def get_leader_titre(country):
    info=get_info(country)
    if 'leader_title1' in info:
        leader_titre=info['leader_title1'].replace('\n',' ')
        m = re.match(".*?\[\[([\w\s',(.)|-]+)\]\]",leader_titre)
        leader_titre=m.group(1)
        
        return leader_titre
    
    # En cas d'échec
    print('Impossible de trouver le leader')
    return None

def get_leader_name(country):
    info=get_info(country)
    if 'leader_name1' in info:
        leader_name=info['leader_name1'].replace('\n',' ')
        m = re.match(".*?\[\[([\w\s',(.)|-]+)\]\]",leader_name)
        leader_name=m.group(1)
        
        return leader_name
    
    # En cas d'échec
    print('Impossible de trouver le leader')
    return None
















# 
# conn = sqlite3.connect('base_donnees.sqlite')
# 
# def add_country(conn,country):
#     # préparation de la commande SQL
#     c = conn.cursor()
#     sql = 'INSERT OR REPLACE INTO countries VALUES (?, ?, ?, ?, ?)'
#     info=get_info(country)
# 
#     # les infos à enregistrer
#     name = get_name(info)
#     capital = get_capital(info)
#     coords = get_coords(info)
# 
#     # soumission de la commande (noter que le second argument est un tuple)
#     c.execute(sql,(country, name, capital, coords['lat'],coords['lon']))
#     conn.commit()