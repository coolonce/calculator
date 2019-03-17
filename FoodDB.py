import sqlalchemy

class FoodDB:
    def __init__(self, database):
        self.database = database
        #TODO get this mapping from json-file
        self.mapping = {
    "0": 10,
    "1": 11,
    "2": 12,
    "3": 16,
    "4": 13,
    "5": 18,
    "6": 17,
    "7": 15,
    "9": 2,
    "10": 3,
    "11": 8,
    "12": 5,
    "13": 9,
    "14": 52,
    "15": 55,
    "16": 54,
    "17": 56,
    "19": 53,
    "20": 58,
    "22": 59,
    "24": 60,
    "25": 61,
    "28": 62,
    "29": 14
  }
    #получаем на вход список продуктов, возвращаем словарь, где ключ - id витамина по мапе, значение - значение витамина
    def get_food_vitamins_by_id(self, food_id):
        food_vitamin = {}
        temp=self.database.execute(sqlalchemy.text("select * from vitamins where vitamins.food_id=:id"),
                                    {"id":food_id}).fetchall()
        for i in range(2,len(temp[0])):
            if i in self.mapping.values():
                food_vitamin[i]=temp[0][i]

        return food_vitamin

    # получаем на вход список продуктов, возвращаем словарь, где ключ - id минерала по мапе, значение - значение минералов
    def get_food_minerals_by_id(self, food_id):
        food_mineral = {}
        temp = self.database.execute(sqlalchemy.text("select * from vitamins where vitamins.food_id=:id"),
                                    {"id": food_id}).fetchall()
        for i in range(2, len(temp[0])):
            if i + 50 in self.mapping.values():
                food_mineral[i + 50] = temp[0][i]

        return food_mineral

    # получаем на вход список продуктов, возвращаем словарь, где ключ - id продукта,
    # значение - содержание БЖУ и сопутствующих им нутриентов
    def get_food_CPFC_by_id(self, food_id):

        temp=self.database.execute(sqlalchemy.text("select * from food where food.id=:id"), {"id":food_id}).fetchall()
        return dict(temp[0][3:])



