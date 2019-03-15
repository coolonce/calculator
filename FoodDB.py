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
    #получаем на вход список продуктов, возвращаем словарь, где ключ - id продукта, значение - содержание витаминов
    def get_all_food_vitamins(self, food_id_list):
        food_vitamin_dict = {}
        for id in food_id_list:
            current_food_vitamin = {}
            temp=self.database.execute(sqlalchemy.text("select * from vitamins where vitamins.food_id=:id"),
                                       {"id":id}).fetchall()
            for i in range(2,len(temp[0])):
                if i in self.mapping.values():
                    current_food_vitamin[i]=temp[0][i]
            food_vitamin_dict[id]=current_food_vitamin
        return food_vitamin_dict

    # получаем на вход список продуктов, возвращаем словарь, где ключ - id продукта, значение - содержание минералов
    def get_all_food_minerals(self, food_id_list):
        food_mineral_dict = {}
        for id in food_id_list:
            current_food_minerals = {}
            temp = self.database.execute(sqlalchemy.text("select * from vitamins where vitamins.food_id=:id"),
                                         {"id": id}).fetchall()
            for i in range(2, len(temp[0])):
                if i + 50 in self.mapping.values():
                    current_food_minerals[i + 50] = temp[0][i]
            food_mineral_dict[id] = current_food_minerals
        return food_mineral_dict

    # получаем на вход список продуктов, возвращаем словарь, где ключ - id продукта,
    # значение - содержание БЖУ и сопутствующих им нутриентов
    def get_all_food_CPFC(self, food_id_list):
        food_CPFC_dict={}
        for id in food_id_list:
            temp=self.database.execute(sqlalchemy.text("select * from food where food.id=:id"), {"id":id}).fetchall()
            food_CPFC_dict[id] = list(temp[0][3:])
        return food_CPFC_dict


