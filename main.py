## Consumo dos dados da API de dados abertos do Recife

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import xml.etree.ElementTree as ET
import json

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
                item = {}
                for attr in registro.attrib:
                    schema = ['id', 'nome', 'codigocategoria', 'latitude', 'longitude', 'altitude', 'categoria', 'descricao', 'idioma', 'logradouro', 'municipio']
                    item[schema[int(attr.replace("campo",""))-1]] =  registro.get(attr)
                data.append(item)
        return { 'data' : data }

api.add_resource(Museus_Meta, '/museus/')
api.add_resource(Pontos_Turisticos_Meta, '/pontosTuristicos/')

class Importacao(object):
    def importPontos(self):
        e = create_engine('sqlite:///pontos_turisticos.db')
        conn = e.connect()

        JSON_FILE = "datasets-pe/pontos-turisticos.json"
        rawdata = json.load(open(JSON_FILE))
        parsed = rawdata['data']
        dataset = json.loads(json.dumps(parsed))

        for data in dataset:
            id = int(data['id']) if data['id'] is not None else None
            codigocategoria = None
            altitude = None
            longitude = None
            latitude = None
            if data['codigocategoria'] != '': codigocategoria = int(data['codigocategoria'])
            conn.execute('INSERT INTO pontos_turisticos_normal VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)', id, data['nome'], codigocategoria, altitude, data['categoria'], data['descricao'], data['idioma'], data['logradouro'], data['municipio'], latitude, longitude )

if (not app.debug):
    import logging
    from logging import FileHandler
    file_handler = FileHandler('app.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    #i = Importacao()
    #i.importPontos()
    app.run()
