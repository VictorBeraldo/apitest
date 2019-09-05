from sql_alchemy import banco


class HotelModel(banco.Model):
    """Classe para referenciar os hoteis"""

    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80)) # 80 tamanho sting
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    audio = banco.Column(banco.String(8000))
    # construtor
    def __init__(self,hotel_id,nome,estrelas,diaria,cidade,audio):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.audio = audio
    # metodo de classe pois le não vai acessar nenhum atributos do objeto, apenas id, que sera passado por argumento
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() # SELECT * FROM hoteis WHERE hotel_id = $hotel_id LIMIT 1
        if hotel:
            return hotel
        return  None
    def save_hotel(self):
        #salva pro db , sabendo os argumentos do obj
        banco.session.add(self)
        banco.session.commit()
    
    def update_hotel(self, nome, estrelas, diaria,cidade,audio): # atributos vindo do **dados
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade   
        self.audio = audio 
    
    def delete_hotel(self):
        """deleta hotel"""
        #recebe o objeto e deleta do banco
        banco.session.delete(self)
        banco.session.commit()

    def json(self):
        """metodo que transforma objeto em json"""
        return {
            'hotel_id' : self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'audio':self.audio
        }