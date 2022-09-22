
from model.MissaoConcluida import MissaoConcluida
from model.Motorista import Motorista

class MissaoConcluidaController():
    def __init__(self):
        self.missaoconcluida_model = MissaoConcluida()
        self.motorista_model = Motorista()

    def get_missao_concluida(self):
        result = []
        try:
            res = self.missaoconcluida_model.get_missao_concluida()

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
                     'data_saida': missao.data_saida.strftime('%d/%m/%Y  %H:%M'),
                     'data_chegada': missao.data_chegada.strftime('%d/%m/%Y  %H:%M'),
                     'motorista': motorista,
                     'viatura': viatura,


                })
            status = 200

        except Exception as e:
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }


        
