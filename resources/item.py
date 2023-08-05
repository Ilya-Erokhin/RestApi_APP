from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

# parser = reqparse.RequestParser():
# Здесь создается объект RequestParser из библиотеки Flask-RESTful.
# Это инструмент, который позволяет нам определить, какие аргументы ожидать в запросах (например, в теле POST-запроса) и как их обрабатывать.
    parser = reqparse.RequestParser()

# parser.add_argument(...):
# В этой части кода мы определяем ожидаемые аргументы для запросов.
# В данном случае, для POST и PUT запросов ожидаются два аргумента: price (цена товара) и store_id (идентификатор магазина).
# Оба аргумента должны иметь определенные типы данных (цена - float, идентификатор магазина - int), а также быть обязательными (required=True),
    # что означает, что они должны быть присутствовать в запросе. Если аргументы отсутствуют, будет возвращено сообщение об ошибке.
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

# @jwt_required():
# Это декоратор из библиотеки Flask-JWT-Extended, который указывает, что для доступа к методам класса Item требуется аутентификация через JSON Web Token.
# Таким образом, только авторизованные пользователи с правильным токеном смогут использовать методы get, post, put и delete.

# def get(self, name):
# Это метод для обработки HTTP-запросов типа GET, которые приходят на URL, содержащий имя элемента товара (/item/<name>).
# В данном случае, мы ожидаем, что вместе с запросом будет передано имя элемента (name).
# Метод вызывает статический метод класса ItemModel.find_by_name(name), чтобы найти элемент товара по его имени в базе данных.
# Если элемент найден, возвращается его представление в формате JSON, иначе возвращается сообщение об ошибке.
# Если сохранение прошло успешно, функция вернет JSON-представление созданного предмета со статусом 201 (это означает "создано").
    # Также она возвращает сообщение об успехе и данные о предмете.
# Если произошла ошибка при сохранении (например, что-то пошло не так с базой данных), функция вернет сообщение об ошибке с кодом статуса 500 (это означает "внутренняя ошибка сервера").
    # Это сообщает клиенту, что что-то пошло не так на стороне сервера, и предмет не был сохранен.
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

# def post(self, name):
# Это метод для обработки HTTP-запросов типа POST.
# Он принимает имя элемента товара (name) из URL и ожидает, что в теле запроса будут переданы аргументы price и store_id.
# Сначала метод проверяет, существует ли уже элемент товара с таким именем, и если да, возвращается сообщение об ошибке.
# Затем данные запроса передаются в parser.parse_args(), чтобы получить аргументы price и store_id.
# Создается объект класса ItemModel с переданными аргументами, и попытка сохранить его в базу данных с помощью метода save_to_db().
# Если сохранение прошло успешно, функция вернет JSON-представление созданного предмета с кодом статуса 201, что означает "создано".
    # JSON-представление предмета получается путем вызова метода json() у объекта item.
# Если произошла ошибка при сохранении предмета в базу данных (например, что-то пошло не так с базой данных),
    # функция вернет JSON-ответ с сообщением об ошибке: "An error occurred inserting the item." и установит статус ответа в 500, что означает "внутренняя ошибка сервера".
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

# def delete(self, name):
# Это метод для обработки HTTP-запросов типа DELETE.
# Аналогично предыдущим методам, он принимает имя элемента (name) из URL.
# Затем он пытается найти элемент с указанным именем в базе данных с помощью ItemModel.find_by_name(name).
# Если элемент найден, он удаляется из базы данных с помощью метода delete_from_db(), и возвращается сообщение об успешном удалении.
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

# def put(self, name):
# Это метод для обработки HTTP-запросов типа PUT.
# Он работает похожим образом на метод POST, но вместо создания нового элемента товара с указанным именем,
    # он обновляет цену (price) существующего элемента, если такой элемент уже существует.
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


# Класс ItemList:
# Этот класс представляет ресурс для работы со списком всех элементов товаров в нашем API.
class ItemList(Resource):

# def get(self):
# Это метод для обработки HTTP-запросов типа GET на URL /items.
# Он возвращает список всех элементов товаров в формате JSON.
# Для этого метод использует метод json() каждого элемента из списка, полученного с помощью ItemModel.query.all().
# Этот метод возвращает все записи из таблицы элементов товаров (в базе данных), которые затем преобразуются в список JSON-представлений элементов.
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}