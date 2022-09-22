# -*- coding: utf-8 -*-
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from config import app_active, app_config
from model.User import User

config = app_config[app_active]
db = SQLAlchemy(config.APP)

class Viatura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    active = db.Column(db.Boolean(), default=1, nullable=True)
    km_viatura = db.Column(db.Numeric(10,2), nullable=False)
    def __repr__(self):
        return '%s - %s - %s' % (self.id, self.name, self.km_viatura)

    def get_total_viatura(self):
        try:
            res = db.session.query(func.count(Viatura.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res