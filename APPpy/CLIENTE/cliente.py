from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

#ENDPOINTS: Mobile(cliente)
@app.route('/cliente/inicio/')
def InicioSeccion():
    #Post

    return render_template('inicio_seccion.html')

@app.route('/cliente/demo')
def crear_CodigoMaestro():
    codigo_maestro = "6416245"
    pass