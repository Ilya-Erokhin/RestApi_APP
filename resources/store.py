from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

# def get(self, name):
# В данном случае, мы ожидаем, что вместе с запросом будет передано имя магазина (name).
# Метод вызывает статический метод класса StoreModel.find_by_name(name) для поиска магазина по его имени в базе данных.
# Если магазин найден, возвращается его представление в формате JSON, иначе возвращается сообщение об ошибке.
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404


# def post(self, name):
# Это метод для обработки HTTP-запросов типа POST.
# Он принимает имя магазина (name) из URL и проверяет, существует ли уже магазин с таким именем.
# Если магазин с таким именем уже существует, возвращается сообщение об ошибке.
# Затем создается объект класса StoreModel с переданным именем, и попытка сохранить его в базу данных с помощью метода save_to_db().
# Если сохранение прошло успешно, возвращается представление созданного магазина в формате JSON.
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

# def delete(self, name):
# Это метод для обработки HTTP-запросов типа DELETE.
# Аналогично предыдущим методам, он принимает имя магазина (name) из URL.
# Затем он пытается найти магазин с указанным именем в базе данных с помощью StoreModel.find_by_name(name).
# Если магазин найден, он удаляется из базы данных с помощью метода delete_from_db(), и возвращается сообщение об успешном удалении.
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
# def get(self):
# Это метод для обработки HTTP-запросов типа GET на URL /stores.
# Он возвращает список всех магазинов в формате JSON.
# Метод использует генератор списка, чтобы пройти по всем объектам StoreModel в базе данных (полученным с помощью StoreModel.query.all()),
# и преобразовать каждый объект магазина в его JSON-представление с помощью метода json().
# Затем список JSON-представлений всех магазинов возвращается как ответ на запрос.
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
