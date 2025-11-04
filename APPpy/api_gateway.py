from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests

app = Flask(__name__)
api = Api(app)

SERVICIOS = {
    'servidor': 'http://localhost:8001',
    'iot': 'http://localhost:8002',
    'cliente': 'http://localhost:8003'
}

class GatewayResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Authorization', location='headers')
    
    def get(self, servicio, ruta=None):
        return self._forward_request(servicio, ruta)
    
    def post(self, servicio, ruta=None):
        return self._forward_request(servicio, ruta)
    
    def put(self, servicio, ruta=None):
        return self._forward_request(servicio, ruta)
    
    def delete(self, servicio, ruta=None):
        return self._forward_request(servicio, ruta)
    
    def _forward_request(self, servicio, ruta):
        if servicio not in SERVICIOS:
            return {'error': 'Servicio no encontrado'}, 404
        
        url_base = SERVICIOS[servicio]
        url_completa = f"{url_base}/{ruta}" if ruta else url_base
        
        # Forward the request
        response = requests.request(
            method=request.method,
            url=url_completa,
            headers=dict(request.headers),
            json=request.get_json(),
            params=request.args
        )
        
        return response.json(), response.status_code

# Configurar rutas del gateway
api.add_resource(GatewayResource, '/api/<string:servicio>', '/api/<string:servicio>/<path:ruta>')



