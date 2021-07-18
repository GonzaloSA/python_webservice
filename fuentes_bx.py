# -*- coding: utf-8 -*-

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import json

fin = datetime.datetime.today()
inicio  = fin - datetime.timedelta(days=5)
fecha_inicio = inicio.strftime("%Y-%m-%d")
fecha_fin = fin.strftime("%Y-%m-%d")




def descarga_serie_banxico():
    token = 'c131c9273fcbcdb402c79d6aedfa75958f738b3f8f9bcd44820f93c13856b56e'
    serie = 'SF43718'
    url_base = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'+serie+'/datos/'+fecha_inicio+'/'+fecha_fin
    #print(url_base)
    header = { 'Bmx-Token' : token  }
    response = requests.get(url_base,headers=header)
    status = response.status_code
    if status != 200:
        return 'Ha ocurrido un error en la consulta'
    raw_data = response.json()
    bx = raw_data['bmx']['series'][0]
    data= {}
    data['banxico'] = []

    for inf in bx['datos']:
        data["banxico"].append({"Fecha":inf['fecha'], "Valor":inf['dato']})
    #resp = json.dumps(data)
    return data

def descarga_serie_fixer():
    key = '4d8bd26cdc483c10f32c9c5bcf549f7b'
    url_f = 'http://data.fixer.io/api/'+fecha_fin+'?access_key='+key+'&symbols=MXN,USD'
    print(url_f)
    response = requests.get(url_f)
    status = response.status_code
    if status != 200:
        return 'Ha ocurrido un error en la consulta'
    raw_data1 = response.json()
    return raw_data1


def descargaScrapper():
    url = 'https://www.banxico.org.mx/tipcamb/tipCamMIAction.do'
    html = urlopen(url)
    res = BeautifulSoup(html.read(),"html5lib")
    links = res.find_all('tr', {'class':['renglonNon','renglonPar']})
    data= {}
    data['DOF'] = []
    for tds in links:
        texto = tds.contents
        format = "%d/%m/%Y"
        if datetime.datetime.strptime(texto[1].string.strip(), format) >= inicio and datetime.datetime.strptime(texto[1].string.strip(), format) <= fin:
            data["DOF"].append({"Fecha":texto[1].string.strip(), "Valor":texto[5].string.strip()})
    #resp = json.dumps(data)
    return data

def consulta():
    dt = {}
    dt['tarifas'] = []
    dt['tarifas'].append(descargaScrapper())
    dt['tarifas'].append(descarga_serie_banxico())
    
    resp = json.dumps(dt,  indent=4)
    return resp

#print(consulta())

"""
print('Datos BANXICO')
mis_datos = descarga_serie_banxico()
print(mis_datos)
print('Datos DOF')
datos_DOF = descargaScrapper()
print(datos_DOF)


print('Datos FIXER')
datos_fixer = descarga_serie_fixer()
print(datos_fixer)


"""