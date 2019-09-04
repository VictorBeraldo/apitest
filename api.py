from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)

#RASTRAR MODIFICAÇÕES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#caminho do banco, para raiz e criar um banco do tipo sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
api = Api(app)

#Decorador para função ser executada apenas na primeira requisição, cria banco se não existir
@app.before_first_request
def cria_banco():
    banco.create_all()

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') # hotel_id será inscrito junto da url

# importar bibliotecas apenas quando for executar o app.py
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

