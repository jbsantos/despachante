from flask_admin import Admin
# Capítulo 10 - Remover
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from model.Role import Role
from model.User import User
from model.MissaoConcluida import MissaoConcluida
from model.Motorista import Motorista
from model.Viatura import Viatura
from model.Status import Status
from model.Product import Product
from model.Missao import Missao
from admin.Views import UserView, HomeView, RoleView, CategoryView, ProductView, MissaoView, MotoristaView, ViaturaView, StatusView, MissaoConcluidaView

def start_views(app, db):
    admin = Admin(app, name='MISSÕES STS-DESPACHO', base_template='admin/base.html', template_mode='bootstrap3', index_view=HomeView())

    admin.add_view(RoleView(Role, db.session, "Funções",  category="Usuários"))
    admin.add_view(UserView(User, db.session, "Usuários", category="Usuários"))
    #admin.add_view(CategoryView(Category, db.session, 'Categorias', category="Produtos"))
    #admin.add_view(ProductView(Product, db.session, "Produtos", category="Produtos"))
    admin.add_view(ViaturaView(Viatura, db.session, 'Viatura', category="Missão"))
    admin.add_view(MotoristaView(Motorista, db.session, 'Motorista', category="Missão"))
    admin.add_view(StatusView(Status, db.session, 'Status', category="Missão"))

    admin.add_view(MissaoView(Missao, db.session, "Missão", category="Missão"))
    admin.add_view(MissaoConcluidaView(MissaoConcluida, db.session, "Missão Concluida", category="Missão"))

    admin.add_link(MenuLink(name='Logout', url='/logout'))