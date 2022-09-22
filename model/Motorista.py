# -*- coding: utf-8 -*-
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form

from config import app_active, app_config

from model.User import User

config = app_config[app_active]
db = SQLAlchemy(config.APP)

class Motorista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    saram = db.Column(db.Integer,  nullable=False)
    om = db.Column(db.String(4),  nullable=False)
    validade_identidade_militar = db.Column(db.DateTime(8), default=db.func.current_timestamp(), nullable=False)
    categoria_veiculo = db.Column(db.Text(), nullable=False)


    def __repr__(self):
        return self.name

    def get_total_motorista(self):
        try:
            res = db.session.query(func.count(Motorista.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

    def get_motorista(self):
        try:
            res = db.session.query(Motorista).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res


