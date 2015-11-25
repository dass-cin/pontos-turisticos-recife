## Consumo dos dados da API de dados abertos do Recife

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine

e = create_engine('sqlite:///museus.db')

app = Flask(__name__)
api = Api(app)


class Museus_Meta(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute('select * from museus')
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result


api.add_resource(Museus_Meta, '/museus/')

if __name__ == '__main__':
    app.run()