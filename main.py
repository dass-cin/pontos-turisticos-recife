## Consumo dos dados da API de dados abertos do Recife

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import xml.etree.ElementTree as ET

e = create_engine('sqlite:///museus.db')

app = Flask(__name__)
api = Api(app)


class Museus_Meta(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute('select * from museus')
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result

class Pontos_Turisticos_Meta(Resource):
    def get(self):
        tree = ET.parse('datasets-pe/EMPETUR_PontosTuristicosPE_dado.xml')
        root = tree.getroot()
        data = []
        for child in root.iter('registros'):
            for registro in child.iter('registro'):
                for attr in registro.attrib:
                    data.append({attr:  registro.get(attr)})
        return { 'data' : data }


api.add_resource(Museus_Meta, '/museus/')
api.add_resource(Pontos_Turisticos_Meta, '/pontosTuristicos/')


if (not app.debug):
    import logging
    from logging import FileHandler
    file_handler = FileHandler('app.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()