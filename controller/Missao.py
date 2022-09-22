from datetime import datetime

from model.Missao import Missao
from model.Motorista import Motorista
class MissaoController():
    def __init__(self):
        self.missao_model = Missao()
        self.motorista_model = Motorista()
    def get_missao(self):
        result = []
        try:
            res = self.missao_model.get_missao_motorista_all()

            print(res, 'teste....')

            for r in res:
                missao = r[0]
                motorista = r[1]
                viatura = r[2]

                result.append({
                    'id' : missao.id,
                     'viatura': missao.viatura,
                     'missao': missao.natureza_servico,
                     'km_saida': str(missao.km_saida),
                     'km_chegada': str(missao.km_chegada),
                     'ficha': missao.ficha,
                     #: datetime.strptime(r.data_saida, "%d/%m/%Y"),
                     'data_saida': missao.data_saida.strftime('%d/%m/%Y  %H:%M'),
                     'data_chegada': missao.data_chegada.strftime('%d/%m/%Y  %H:%M'),
                     'motorista': motorista,
                     'viatura': viatura,


                })
            status = 200

        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }


        
    def get_missao_by_id(self, missao_id):
        result = {}
        try:
            self.missao_model.id = missao_id
            res = self.missao_model.get_missao_by_id()

            for r in res:
                missao = r[0]
                motorista = r[1]
                print(motorista)
                viatura = r[2]

            
            result = {
                'id' : res.id,
                'viatura': res.viatura,
                'missao': res.natureza_servico,
                'km_saida': str(res.km_saida),
                'km_chegada': str(res.km_chegada),
                'ficha': res.ficha,
                'data_saida': res.data_saida.strftime('%d/%m/%Y  %H:%M'),
                'data_chegada': res.data_chegada.strftime('%d/%m/%Y  %H:%M'),
                'motorista': motorista,
                'viatura': viatura,

            }

            status = 200
        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }