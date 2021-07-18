# -*- coding: utf-8 -*-
"""Clase para proporcioar webservice de tipo de cambio USD a MXN de los ultimos 5 dias
    de tres fuentes diferentes, FIXER, BANXICO, Diario Oficial de la Federacion
Code by Gonzalo Serna (June, 2021)
"""

import web  #Servico web
import fuentes_bx #libreria de funciones

#Indica donde se encuentra la aplicacion
urls = (
    '/', 'Index'
)
class Index:
    def GET(self):
        """ Esta opcion sera llamada ada que se haga una solicitud
        """
        response =fuentes_bx.consulta()
        return response

if __name__ == "__main__":
    """Comienza el servicio de la aplicacion
    """
    app = web.application(urls, globals())
    app.run()
