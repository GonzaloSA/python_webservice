import web
import json

urls = (
    '/', 'Index'
)
class Index:
    def GET(self):
        response =json.dumps( {
        'mensaje': 'Hola Mundo chido'
        })
        return response

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run(port=8800)
