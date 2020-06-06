import wptools
import sqlite3
from zipfile import ZipFile
import json
import re

def get_info(country):
    with ZipFile('europe.zip','r') as z:
        return json.loads(z.read('{}.json'.format(country)).decode())

def get_conventional_name(country):
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
        
        # Le nom de la capitale peut comporter des lettres, espaces ou un des caractères: ',.()|- compris entre crochets [[...]]
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
        
# On obtient un résultat ressemblant à 'President of France | President'. Or, on souhaite avoir uniquement 'President'. On utilise donc la fonction split pour récupérer cette information.
        leader_titre=leader_titre.split("|")
        return leader_titre[1]
    
    # En cas d'échec
    print('Impossible de trouver le leader')
    return None

def get_leader_name(country):
    info=get_info(country)
    if 'leader_name1' in info:
        leader_name=info['leader_name1'].replace('\n',' ')
        m = re.match(".*?\[\[([\w\s',(.)|-]+)\]\]",leader_name)
        leader_name=m.group(1)
        
        leader_name=leader_name.split('|')
        return leader_name[0]
    
    # En cas d'échec
    print('Impossible de trouver le leader')
    return None

def get_population(country):
    info=get_info(country)
    if country=='Armenia':
        return(3021324)
    if country=='Denmark':
        return(5814461)
    if country=='Moldova':
        return(2681735)
    if country=='Russia':
        return(146793744)
    if country=='Turkey':
        return(82003882)
    
    if 'population_census' in info:
        population=info["population_census"].replace(',','')
        population=population.split('}} ')
        if len(population)==1:
            population[0]=population[0].split(' {{')
            return int(population[0][0])
        return int(population[1])
    
    if 'population_estimate' in info:
        population=info["population_estimate"].replace(',','')
        population=population.split('}} ')
        if len(population)==1:
            population[0]=population[0].split(' {{')
            return int(population[0][0])
        population[1]=population[1].split(' {{')
        return int(population[1][0])
        
    # En cas d'échec
    print('Impossible de trouver le nombre d\'habitants')
    return None

def get_monnaie(country):
    info=get_info(country)
    if "currency" in info:
        currency=info['currency'].replace('\n',' ')
        m = re.match(".*?\[\[([\w\s',(.)|-]+)\]\]",currency)
        currency=m.group(1)
        currency=currency.split('|')
        return currency[0]
    
    # En cas d'échec
    print('Impossible de trouver la monnaie')
    return None

def get_coords(country):
    info=get_info(country)
    if 'coordinates' in info:
        coord=info['coordinates']
        m=re.match('(?i).*{{coord\s*\|([^}]*)}}',coord)
        
        if m == None:
            print('Impossible d\'afficher proprement les coordonnées :'+coord)
            return None
        coord=m.group(1)
        if coord[0:1] in '0123456789':
            return cv_coords(coord)
    
    # En cas d'échec
    print('Impossible de trouver les coordonnées')
    return None

def cv_coords(str_coords):
    # on découpe au niveau des "|" 
    c = str_coords.split('|')

    # on extrait la latitude en tenant compte des divers formats
    lat = float(c.pop(0))
    if (c[0] == 'N'):
        c.pop(0)
    elif ( c[0] == 'S' ):
        lat = -lat
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'N' ):
        lat += float(c.pop(0))/60
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'S' ):
        lat += float(c.pop(0))/60
        lat = -lat
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'N' ):
        lat += float(c.pop(0))/60
        lat += float(c.pop(0))/3600
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'S' ):
        lat += float(c.pop(0))/60
        lat += float(c.pop(0))/3600
        lat = -lat
        c.pop(0)

    # on fait de même avec la longitude
    lon = float(c.pop(0))
    if (c[0] == 'W'):
        lon = -lon
        c.pop(0)
    elif ( c[0] == 'E' ):
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'W' ):
        lon += float(c.pop(0))/60
        lon = -lon
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'E' ):
        lon += float(c.pop(0))/60
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'W' ):
        lon += float(c.pop(0))/60
        lon += float(c.pop(0))/3600
        lon = -lon
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'E' ):
        lon += float(c.pop(0))/60
        lon += float(c.pop(0))/3600
        c.pop(0)
    
    # on renvoie un dictionnaire avec les deux valeurs
    return {'lat':lat, 'lon':lon }

def get_PIB(country):
    info=get_info(country)
    if "GDP_nominal" in info:
        PIB=info["GDP_nominal"].replace('&nbsp;',' ')
        PIB=PIB.split('|')
        if len(PIB)==1:
            return PIB[0]
        return PIB[1]
    
    # En cas d'échec
    print('Impossible de  trouver le PIB')
    return None










conn = sqlite3.connect('base_donnees.sqlite')

def add_country(country):
    # préparation de la commande SQL
    c = conn.cursor()
    sql = 'INSERT OR REPLACE INTO countries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

    # les infos à enregistrer
    conv_name = get_conventional_name(country)
    leader_t=get_leader_titre(country)
    leader_n=get_leader_name(country)
    capital = get_capital(country)
    pop=get_population(country)
    currency=get_monnaie(country)
    coords = get_coords(country)
    

    # soumission de la commande (noter que le second argument est un tuple)
    c.execute(sql,(country, conv_name, leader_t, leader_n, capital, pop, currency, coords['lat'],coords['lon']))
    conn.commit()