<<<<<<< Updated upstream
import json

def application(environ, start_response):
    header = [('Content-type', 'application/json')]
    start_response('200 ok', header)
    response =json.dumps( {
        'mensaje': 'Hola Mundo chido'
    })
=======
import json

def application(environ, start_response):
    header = [('Content-type', 'application/json')]
    start_response('200 ok', header)
    response =json.dumps( {
        'mensaje': 'Hola Mundo chido'
    })
>>>>>>> Stashed changes
    return [response]