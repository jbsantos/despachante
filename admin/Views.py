# -*- coding: utf-8 -*-
from wtforms.validators import DataRequired

import app
from flask_admin import AdminIndexView, expose
import datetime

from flask_admin.form import rules
from wtforms import Form, SelectField


from flask_admin.contrib.sqla import ModelView

# Capítulo 10
from flask_admin.helpers import get_redirect_target, get_form_data, is_form_submitted
from flask_login import current_user
from flask import redirect, url_for

from config import app_config, app_active

from model.User import User
from model.Category import Category
from model.Motorista import Motorista

from model.Viatura import Viatura, db

from model.Product import Product
from model.Missao import Missao
from model.MissaoConcluida import MissaoConcluida
from datetime import datetime

from controller.Missao import MissaoController
from controller.MissaoConcluida import MissaoConcluidaController

config = app_config[app_active]


class HomeView(AdminIndexView):

    extra_css = [config.URL_MAIN + 'static/css/home.css',
                 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']

    @expose('/')
    def index(self):
        self.usuario_logado = current_user

        user_model = User()
        category_model = Category()
        motorista_model = Motorista()
        viatura_model = Viatura()
        missao_controller = MissaoController()

        product_model = Product()
        missao_model = Missao()

        users = user_model.get_total_users()
        categories = category_model.get_total_categories()
        motorista = motorista_model.get_total_motorista()
        viatura = viatura_model.get_total_viatura()

        products = product_model.get_total_products()
        missao = missao_model.get_total_missao()
        last_products = product_model.get_last_products()
        last_missao = missao_model.get_last_missao()
        missao_controller = missao_controller.get_missao()
        print(missao_controller)
        return self.render('home_admin.html', report={
            'users': users[0],
            'categories': categories[0],
            'motorista': motorista[0],
            'products': products[0],
            'missao': missao[0],
            'viatura': viatura[0]

        }, last_products=last_products, last_missao=last_missao, missao_controller=missao_controller)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

def user_formatar(self, request, motorista, *args):
    data_pt = datetime.strftime(motorista.validade_identidade_militar, "%d/%m/%y")
    return data_pt

class UserView(ModelView):

    column_formatters = {'validade_identidade_militar': user_formatar}

    column_labels = {
        'funcao': 'Função',
        'username': 'Nome de usuário',
        'email': 'E-mail',
        'date_created': 'Data de Criação',
        'last_update': 'Última atualização',
        'active': 'Estado',
        'password': 'Senha',
    }

    column_descriptions = {
        'funcao': 'Função no painel administrativo',
        'username': 'Nome de usuário no sistema',
        'email': 'E-mail do usuário no sistema',
        'date_created': 'Data de Criação do usuário no sistema',
        'last_update': 'Última atualização desse usuário no sistema',
        'active': 'Estado ativo ou inativo no sistema',
        'password': 'Senha do usuário no sistema',
    }

    column_exclude_list = ['password', 'recovery_code']
    form_excluded_columns = ['last_update', 'recovery_code']

    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }

    can_set_page_size = True
    can_view_details = True
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'funcao']
    create_modal = True
    edit_modal = True
    can_export = True
    column_editable_list = ['username', 'email', 'funcao', 'active']
    column_sortable_list = ['username']
    column_default_sort = [('username', True), ('date_created', True)]
    column_details_exclude_list = ['password', 'recovery_code']
    column_export_exclude_list = ['password', 'recovery_code']

    export_types = ['json', 'yaml', 'csv', 'xls', 'df']

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password

    # Capítulo 10
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


# Capítulo 10
class RoleView(ModelView):
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class CategoryView(ModelView):
    can_view_details = True

    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class ProductView(ModelView):
    can_view_details = True

    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        elif role == 3:
            self.can_create = True
            self.can_edit = True
            self.can_delete = False

        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


def formatar_data_idt(self, request, motorista, *args):
    data_pt = datetime.strftime(motorista.validade_identidade_militar, "%d/%m/%y")
    return data_pt


class MotoristaView(ModelView):
    can_view_details = True
    column_editable_list = ['name']
    # column_exclude_list = ['description']
    create_modal = True
    edit_modal = True

    column_formatters = {'validade_identidade_militar': formatar_data_idt}
    form_excluded_columns = ['ultimo_motorista']
    column_labels = {
        'name': 'Motorista',
        'saram': 'Nº Ordem',
        'om': 'Org. Militar',
        'validadade_identidade_militar': 'Validade de Identidade',
        'categoria_veiculo': 'Categoria do Veiculo'
    }

    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class ViaturaView(ModelView):
    can_view_details = True

    column_labels = {
        'name': 'Registro FAB',
        'description': 'Viatura',
        'active': 'Estado',
    }

    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


def formatar_data_saida(self, request, missao, *args):
    data_pt = datetime.strftime(missao.data_saida, "%d/%m/%y  %H:%M")
    return data_pt


def formatar_data_chegada(self, request, missao, *args):
    data_pt = datetime.strftime(missao.data_chegada, "%d/%m/%y  %H:%M")
    return data_pt


def formatar_viatura(self, request, missao, *args):
    straux = missao.viaturas.name + "-" + missao.viaturas.description
    return straux


def formatar_motorista(self, request, missao, *args):
    straux = missao.motoristas.name + "-" + missao.motoristas.om
    return straux

def formatar_motorista_final(self, request, missao, *args):
    print(missao.ultimo_motorista)
    nomes_motoristas = []
    for i in missao.missao_motorista():
        if i.id == missao.ultimo_motorista:
            nomes_motoristas.append(i.name)


    return nomes_motoristas


def viatura_all():


    return Viatura.query


class MissaoView(ModelView):

    column_searchable_list = ['siloms', 'ficha']
    can_view_details = True
    create_modal = True
    edit_modal = True
    form_choices = {'ultimo_motorista': [(str(row), str(row)) for row in range(10)]}
    form_edit_rules = rules.FieldSet =\
                {   'viaturas',
                    'data_chegada',
                    'km_viatura',
                    'km_chegada',
                    'ultimo_motorista',
                    'status_',
                    'observacao',

                }
    form_create_rules = rules.FieldSet =   {
                    'ficha',
                    'siloms',
                    'motoristas',
                    'viaturas',
                    #'km_viatura',
                    'data_saida',
                    'natureza_servico',
                    'observacao',
                    'status_',

                }

    #form_columns = ['ficha', 'siloms', 'motoristas', 'viaturas', 'km_saida', 'data_saida', 'natureza_servico','observacao', 'status']
    def on_form_prefill(self, form, id):

        self.teste =Form()
        self.teste = [(str(row.id), row.name) for row in Missao.missao_motorista(self)]
        #form.km_saida.data = 324
        form.status_.choices = [('1', 'jorge'), ('2', 'teste')]
        missao = Missao.get_missao_by_id(self,id)
        print(missao.__dict__, 'print missao')

        #print(self.teste)
        #print(form.viaturas.__dict__)
        form.ultimo_motorista.choices = self.teste
        return form

    def teste(self):
        print('chegou')


    column_display_pk = True
    can_view_details = True
    # form_args = dict(
    #
    #     viaturas=dict(
    #
    #         query_factory=viatura_all,
    #         validators=[DataRequired()]
    #     )
    # )

    # def create_model(self, form):
    #
    #     #
    #     Missao
    #     model = form.data
    #     print(model)
    #     #self._on_model_change(form, model, False)
    #     return form


    column_formatters = {
        'data_saida': formatar_data_saida,
        'data_chegada': formatar_data_chegada,
        'viaturas': formatar_viatura,
        'motoristas': formatar_motorista,
        'ultimo_motorista' : formatar_motorista_final,

                        }

    column_labels = {
        'siloms': 'Nº Siloms',
        'ficha': 'Nº Ficha',
        'viatura': 'RegFab e Viatura',
        'natureza_servico': 'Missão',
        'km_saida': 'Km de saída',
        'km_chegada': 'Km de Chegada',
        'motoristas': 'Motorista',
        'observacao': 'Observação'

    }

    form_widget_args = {
        'data_saida': {
            #'type': 'date',
            'style': 'color: black',
            'onchange': teste
        },
    }


    def on_model_change(self, form, model, is_created):
        print('teste change')
        if is_created:
            model.user_created = current_user.id

            id = form.viaturas.raw_data[0]
            print(Missao, 'Missao  onchange')
            viatura = Missao.get_viatura_by_id(self, id)
            print(viatura.km_viatura, 'viatura ...')
            # #print(missao.km_viatura, 'teset 3k2lj')
            model.km_viatura = viatura.km_viatura

            model.km_saida = viatura.km_viatura

    def is_accessible(self):


        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = False
        elif role == 3:
            self.can_create = True
            self.can_edit = True
            self.can_delete = False

        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:

            return redirect('/admin')
        else:
            return redirect('/login')

class StatusView(ModelView):
    can_view_details = True
    column_list = {'id', 'name', 'description'}
    column_labels = {
        'name': 'Status da missão',
        'description': 'Observação'
    }



    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class MissaoConcluidaView(ModelView):

    can_view_details = True
    create_modal = True
    edit_modal = True
    column_display_pk = True
    can_view_details = True

    @expose('/')
    def index(self):

        missao_concluida_controller = MissaoConcluidaController()
        missao_concluida_model = MissaoConcluida()

        missaoconcluida_controller = missao_concluida_controller.get_missao_concluida()
        missaoconcluida = missao_concluida_model.get_missao_concluida()

        return self.render('home_missaoconcluida.html', report={
            'missaoconcluida': missaoconcluida[0]

        }, missaoconcluida_controller=missaoconcluida_controller)

    def is_accessible(self):

        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = False
        elif role == 3:
            self.can_create = True
            self.can_edit = True
            self.can_delete = False

        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:

            return redirect('/admin')
        else:
            return redirect('/login')
