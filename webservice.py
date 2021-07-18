import web
import json
import fuentes_bx

urls = (
    '/', 'Index'
)
class Index:
    def GET(self):
        response =fuentes_bx.consulta()
        return response

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
