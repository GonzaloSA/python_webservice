# -*- coding: utf-8 -*-
"""Metodos para solicitar y presentar datos de cambio USD a MXN de los ultimos 5 dias
Code by Gonzalo Serna (June, 2021)
"""

import requests     #Controlar solicitudes HTTP
from urllib.request import urlopen      #Abrir URL
from bs4 import BeautifulSoup       #Lectura de documentos html
import datetime     #Controlar fechas
import json         #Manejo de archivos en formato json

class Solicitudes:
    """Clase para realizar las solicitudes web y formatear archivos devueltos
    
    Atributos:
        fin [datetime]   :   fecha final del periodo solicitado
        inicio  [datetime]  :   fecha inicial del periodo solicitado
        fecha_inicio  [str] :   fecha de inicio en el formato necesario para las solicitudes
        fecha_fin  [str] :   fecha de final en el formato necesario para las solicitudes


    Funciones:
        descarga_serie_banxico
        descarga_serie_fixer
        descarga_Scrapper_DOF

    """
    def __init__(self):

        self.fin = datetime.datetime.today()
        self.inicio  = self.fin - datetime.timedelta(days=5)
        self.fecha_inicio = self.inicio.strftime("%Y-%m-%d")
        self.fecha_fin = self.fin.strftime("%Y-%m-%d")


    def descarga_serie_banxico(self):
        token = 'c131c9273fcbcdb402c79d6aedfa75958f738b3f8f9bcd44820f93c13856b56e'
        serie = 'SF43718'
        url_base = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'+serie+'/datos/'+self.fecha_inicio+'/'+self.fecha_fin
        header = { 'Bmx-Token' : token  }
        #Se hace la solicitud de datos
        response = requests.get(url_base,headers=header)
        status = response.status_code
        #Se verifica si no hay error
        if status != 200:
            return 'Ha ocurrido un error en la consulta'
        raw_data = response.json()
        bx = raw_data['bmx']['series'][0]
        #Variable para almacenar los datos de interes
        data= {}
        data['banxico'] = []
        for inf in bx['datos']:
            #Se escribe el archivo json
            data["banxico"].append({"Fecha":inf['fecha'], "Valor":float(inf['dato'])})
        return data

    def descarga_serie_fixer(self):
        key = '4d8bd26cdc483c10f32c9c5bcf549f7b'
        #Se calculas nas fechas de los ultims 5 dias
        lista_fechas = [self.inicio + datetime.timedelta(days=d) for d in range((self.fin - self.inicio).days + 1)] 
        #Variable para almacenar los datos de interes
        data= {}
        data['fixer'] = []
        #se solicita 1 dato por dia, por configuracion de cueta Fixer no permite hacer consultas extendidas
        for dia in lista_fechas:
            d =dia.strftime("%Y-%m-%d")
            url_f = 'http://data.fixer.io/api/'+d+'?access_key='+key+'&symbols=MXN,USD'
            response = requests.get(url_f).json()
            status = response['success']
            if status != True:
                return 'Ha ocurrido un error en la consulta--' + response['error']['type']+'--'
            #Se calcula el tipo de cambio con los valores devueltos,  por configuracion de cueta Fixer no permite utilizar el parametro base
            cambio = float(response['rates']['MXN'])/float(response['rates']['USD'])
            #Se escribe el archivo json
            data["fixer"].append({"Fecha":dia.strftime("%d-%m-%Y"), "Valor":round(cambio,4)})
        return data


    def descarga_Scrapper_DOF(self):
        url = 'https://www.banxico.org.mx/tipcamb/tipCamMIAction.do'
        #Se hace la solicitud de datos
        html = urlopen(url)
        res = BeautifulSoup(html.read(),"html5lib")
        # Se obtienen las etiquetas que contienen los datos necesarios
        links = res.find_all('tr', {'class':['renglonNon','renglonPar']})
        #Variable para almacenar los datos de interes
        data= {}
        data['DOF'] = []
        for tds in links:
            texto = tds.contents
            format = "%d/%m/%Y"
            #Se seleccionan solo los registros de los ultimos 5 dias
            if datetime.datetime.strptime(texto[1].string.strip(), format) >= self.inicio and datetime.datetime.strptime(texto[1].string.strip(), format) <= self.fin:
                #Se escribe el archivo json
                data["DOF"].append({"Fecha":texto[1].string.strip(), "Valor":texto[5].string.strip()})
        return data

def consulta():
    """Funcion que solicita los datos desde la aplicacion y genera el formato json con los valores completos 

    """
    dt = {}
    dt['tarifas'] = []
    dt['tarifas'].append(Solicitudes().descarga_Scrapper_DOF())
    dt['tarifas'].append(Solicitudes().descarga_serie_banxico())
    dt['tarifas'].append(Solicitudes().descarga_serie_fixer())
    
    resp = json.dumps(dt,  indent=2)
    return resp

