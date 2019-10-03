from flask_restful import Resource, reqparse
from models.hotel import HotelModel
import numpy as np
hoteis = [
        {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
        },
        {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
        },
        {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina'
        }
]
class Hoteis(Resource):
    def get(self):
        # hotel.query.all retorna todos elementos do banco de dados SELECT * FROM hoteis
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    import werkzeug
    argumentos = reqparse.RequestParser()
    # não pode deixar nome em branco
    argumentos.add_argument('nome', type =str, required=True, help="This field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True,help="This field 'estrelas' cannot be left blank"  )
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('audio', type = bytes)
        




    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            # Se achar retorne o json do objeto 
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 # not found

    def post(self, hotel_id):
        # criar apenas se existir
        if HotelModel.find_hotel(hotel_id):
            return {'message':"Hotel id {} already exists.".format(hotel_id)}, 400 # Bad Request
        # captura atributos
        dados = self.argumentos.parse_args()
        
        ## TODO trocar aqui por um d_vector
        ## usar array.tobytes() e depois np.frombuffer(s)
        dados['audio'] = np.random.randn(10).tobytes()
        # instanciando  novo hotel
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'},500 # Internal Server Error
        return hotel.json()
        

    def put(self, hotel_id):
        """Se existe hotel cria se nao altera"""
        dados = self.argumentos.parse_args() # captura os dados
        #modo antigo
        #novo_hotel = {'hotel_id': hotel_id, **dados} #** desempacota todos argumentos definidos no contrutor se for chave-valor
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        # existir update, se nao cria
        if hotel_encontrado:
            # apenas atualiza os dados, não o resto como o id
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel() # salvar no banco
            return hotel_encontrado.json(),200  # OK
        # Instancia novo objeto apenas se não encontrar
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'},500 # Internal Server Error 
        return hotel.json(),201 # criado        


        
    def delete(self, hotel_id):
        # usar global para referenciar a lista de hoteis definida globalmente
        #global hoteis
        #atualizar hoteis, com todos menos o hotel_id que será deletado
        #hoteis = [hotel for hotel in hoteis if hotel['hotel_id']  != hotel_id]
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500                
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404 
       