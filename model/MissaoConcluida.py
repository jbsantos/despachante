# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, asc, distinct, and_, or_


from config import app_active, app_config
from model.Missao import Missao
from model.Motorista import Motorista
from model.Status import Status
from model.Viatura import Viatura

config = app_config[app_active]
db = SQLAlchemy(config.APP)

class MissaoConcluida(Missao):

    # QUANTIDADE DE MISSOES CONCLUIDAS
    def get_total_missao_concluida(self):
        try:
            res = db.session.query(func.count(Missao.id)).filter(Missao.status == '2').first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            print(res)
            return res

    # MISSOES CONCLUIDAS
    def get_missao_concluida(self):
        try:
            res = db.session.query(Missao, Motorista, Viatura, Status).join(Motorista, Viatura, Status).filter(Missao.status == '2').all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            print(res)
            return res
