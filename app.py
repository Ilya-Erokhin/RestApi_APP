import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, JWTError

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

from flask import jsonify


# Создание нового экземпляра класса Flask и присваивание его переменной "app"
# Параметр __name__ используется для указания Flask корневого пути приложения.
# Передавая __name__ в качестве аргумента, Flask знает, где искать шаблоны, статические файлы и другие ресурсы относительно текущего модуля.
app = Flask(__name__)

# Установка DEBUG в значение TRUE. Это включает режим отладки Flask.
app.config['DEBUG'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db'):
# Эта строка устанавливает переменную SQLALCHEMY_DATABASE_URI в конфигурации вашего Flask-приложения.
# Эта переменная определяет URI для подключения к базе данных.
# В этой строке используется функция os.environ.get(), чтобы получить значение из переменной окружения DATABASE_URL.
# Если переменная окружения не определена (или не существует), то будет использовано значение 'sqlite:///data.db'.
    # 'sqlite:///data.db': Это URI для SQLite базы данных.
# В данном случае, если не задано значение DATABASE_URL в переменной окружения,
    # Flask будет использовать SQLite базу данных с именем data.db в текущей директории приложения.
# Значение DATABASE_URL может быть использовано для указания URI другой базы данных, такой как PostgreSQL,
    # MySQL или других баз данных, поддерживаемых SQLAlchemy.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False:
# Эта строка устанавливает переменную SQLALCHEMY_TRACK_MODIFICATIONS в конфигурации приложения в значение False.
# Это параметр SQLAlchemy, который определяет, будет ли приложение отслеживать изменения объектов и отправлять сигналы сессии
    # о необходимости сохранения этих изменений в базе данных.
# Установка значения в False отключает автоматическое отслеживание изменений.
# Это рекомендуется для улучшения производительности приложения, если вы не планируете использовать механизм отслеживания изменений SQLAlchemy.
# Если этот параметр установлен в True, он может вызвать неэффективное использование ресу
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'jose123'

# Создание API
# Api(app) создает экземпляр класса Api и связывает его с нашим приложением "app".
# Теперь мы можем использовать объект "api" для определения маршрутов нашего API и указания, какие функции должны обрабатывать запросы.
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

# Этот код добавляет ресурс "Store", "Item", "ItemList", "StoreList" в API, который будет доступен по маршруту URL '/item/<string:name>'....
# '/item/<string:name>'.... - Это маршрут URL, к которому будет привязан ресурсы Store, Item, ItemList, StoreList.
# В этом маршруте есть переменная <string:name>, которая указывает, что после '/item/' ожидается параметр с именем в виде строки.
# Например, если вы отправите GET-запрос на '/item/apple', Flask-RESTful поймет, что apple - это значение параметра "name".
# '/item/<string:name>' - Какая структура конечных точек, позволяющая обращаться к определенному элементу в API
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

# @app.errorhandler(JWTError): Это декоратор Flask, который связывает функцию auth_error_handler с обработкой ошибок типа JWTError.
# JWTError - это тип ошибки, который сгенерируется, если возникнут проблемы с аутентификацией на основе JWT.
@app.errorhandler(JWTError)

# jsonify() - это функция Flask, которая преобразует словарь или объект в JSON-ответ.
# {'message': "Could not..."} - это словарь, содержащий единственный ключ "message" с соответствующим сообщением об ошибке.
# 401 - это код состояния HTTP, который указывает, что доступ к запрашиваемому ресурсу требует аутентификации,
    # но она не была предоставлена или оказалась недействительной.
def auth_error_handler(err):
    return jsonify({'message': "Could not authorize. Did you include a valid Authorization header?"}), 401

# Когда мы выполняем ЭТОТ файл, мы импортируем объект базы данных (DataBase Connector)
# Это проверяет, равен ли встроенный атрибут __name__ строке '__main__'.
# Когда Python запускает программу напрямую (то есть не как модуль, импортированный в другой файл), он устанавливает атрибут __name__ в '__main__'.
# Таким образом, код, находящийся внутри этой проверки, будет выполняться только при запуске файла напрямую.
if __name__ == '__main__':
# Здесь мы импортируем объект db из модуля db. Это объект базы данных, определенный в другом файле db.py.
    from db import db

# Инициализация базы данных с нашим приложением Flask
    db.init_app(app)

# Если мы в режиме отладки, мы создадим все таблицы, НО ТОЛЬКО ПЕРЕД ПЕРВЫМ ЗАПРОСОМ К ПРИЛОЖЕНИЮ
# Создание ВСЕХ таблиц и, наконец, запуск приложения на определенном порту
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
