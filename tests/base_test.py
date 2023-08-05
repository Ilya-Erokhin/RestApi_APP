"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
# Убедимся, что база данных существует
# app - экземпляр класса Flask
# "SQLALCHEMY_DATABASE_URI" - переменная конфигурации, которая указывает, какое хранилище базы данных будет использоваться вашим веб-приложением.
# В данном случае "SQLALCHEMY_DATABASE_URI" определяет строку подключения к базе данных (URI).
# "sqlite:////" - означает, что используется база данных SQLite.
# По сути, этот код устанавливает параметр конфигурации "SQLALCHEMY_DATABASE_URI" для вашего приложения Flask, чтобы использовать базу данных SQLite.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'

# Это гарантирует, что следующие операции выполняются в контексте приложения Flask,
# Что позволяет получить доступ к конфигурации и расширениям приложения.
        with app.app_context():

# db - объект базы данных (из db.py), который использует библиотеку SQLAlchemy.
# Метод init_app() используется для привязки этого объекта базы данных к вашему экземпляру "app" Flask.
# !!! Это указывает SQLAlchemy, какое приложение использовать для своих операций с базой данных !!! (в app.py - app = Flask(__na
            db.init_app(app)

    #@classmethod
    def setUp(self):
        with app.app_context():
            db.create_all()

# Получаем тестового клиента
# test_client() создает виртуального клиента для вашего приложения Flask.
# Этот клиент позволяет отправлять HTTP-запросы к вашим маршрутам Flask, как если бы ваше приложение работало на реальном сервере.
        self.app = app.test_client

# Сохраняем контекст вашего приложения Flask в переменной self.app_context.
# Это может быть полезно, если вам нужно выполнить код, который требует контекста вашего приложения, позже в коде класса тестов.
# Сохранение контекста позволяет использовать его в других методах класса тестов.
        self.app_context = app.app_context

    #@classmethod
    def tearDown(cls):
        # База данных очищается
        with app.app_context():
    # db.session.remove(): Эта строка закрывает текущую сессию базы данных.
    # При работе с базой данных обычно открывается сессия для выполнения операций, таких как чтение или запись данных.
    # После завершения операций сессию следует закрыть, чтобы избежать утечки ресурсов.
            db.session.remove()
    # db.drop_all():
    # Эта строка удаляет все таблицы из базы данных.
    # Это полезно, когда вам нужно очистить базу данных после выполнения тестов, чтобы следующие тесты начинались с чистого состояния базы данных.
            db.drop_all()
