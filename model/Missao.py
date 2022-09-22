

# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, asc, distinct, and_, or_
from sqlalchemy.orm import relationship


from config import app_active, app_config
from model.User import User
from model.Category import Category
from model.Motorista import Motorista
from model.Viatura import Viatura
from model.Status import Status
from datetime import datetime
#from controller.Missao import MissaoController
config = app_config[app_active]
db = SQLAlchemy(config.APP)

def logado():
    from admin.Views import User
    return User

class Missao(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    ficha = db.Column(db.Integer, autoincrement=True, unique=True,  nullable=True)
    siloms = db.Column(db.Integer, unique=True, nullable=False)
    viatura = db.Column(db.String(50), unique=True, nullable=False)
    km_viatura = db.Column(db.Numeric(10,2), nullable=False)
    natureza_servico = db.Column(db.Text(), nullable=False)
    km_saida = db.Column(db.Numeric(10,2), nullable=True)
    km_chegada = db.Column(db.Numeric(10,2), nullable=True)
    data_saida = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    data_chegada = db.Column(db.DateTime(8), default=db.func.current_timestamp(), nullable=True)
    # status = db.Column(db.Integer, default=1, nullable=True)
    observacao = db.Column(db.Text(500), nullable=True)
    user_created = db.Column(db.Integer,db.ForeignKey(User.id), bake_queries=False, nullable=False)
    motorista = db.Column(db.Integer, db.ForeignKey(Motorista.id), nullable=False)
    ultimo_motorista = db.Column(db.Integer, nullable=True)
    #motorista_final = db.Column(db.Integer, nullable=True)
    viatura = db.Column(db.Integer, db.ForeignKey(Viatura.id), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey(Status.id), nullable=False)

    usuario = relationship(User)
    motoristas = relationship(Motorista)
    viaturas = relationship(Viatura)
    status_ = relationship(Status)
    #missao_controller = MissaoController()
    def get_all(self, limit):
        try:
            if limit is None:
                res = db.session.query(Missao).all()
            else:
                res = db.session.query(Missao).order_by(Missao.data_saida).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()

            return res

    def get_missao_motorista_all(self):
        try:
            res = db.session.query(Missao, Motorista, Viatura, Status).join(Motorista, Viatura, Status).filter(
               Missao.status != '2').all()  # ULTIMAS MISSAO EM ANDAMENTO
            print(res)
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()

            return res

    def get_total_missao(self):
        try:
            res = db.session.query(func.count(Missao.id)).filter(Missao.status == '1').first()  # MISSAO EM ANDAMENTO
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            print(res)
            return res

    def get_last_missao(self):
        try:
            res = db.session.query(Missao, Motorista, Viatura).join(Motorista, Viatura).filter(
                Missao.motorista == Motorista.id).all()
            print(res)
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

    def get_missao_by_id(self, id):
        try:
            res = db.session.query(Missao).filter_by(id=id).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res
    def get_viatura_by_id(self, id):
        try:
            res = db.session.query(Viatura).filter_by(id=id).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res
    def missao_motorista(self):
        try:
            res = []
            res = db.session.query(Motorista) \
                .with_entities(
                # Missao.motorista,
                # Missao.motorista_final,
                Motorista.id,
                Motorista.name,

            ). \
                distinct(Motorista.id)
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res