from NutrientCalculator import NutrientCalculator
from NutrientDB import NutrientDB
from FoodDB import FoodDB
import itertools

class CoefCalc:
    food_coef = {}

    def preparing_data(self, gender, mass, height, age, diet_type, norms_db, food_db, food_list):
        nc = NutrientCalculator()
        CPFC_list=nc.calculate_nutrients(gender, mass, height, age, diet_type)

        nutrient_norms_db = NutrientDB(norms_db)
        nutrient_norms_list, ash = nutrient_norms_db.get_all_nutrient_values_for_gender(gender)
        nutrient_norms_list = dict(nutrient_norms_list.fetchall())
        CPFC_list.insert(5,ash)

    def calculate(self, food_db, food_list, CPFC_list, nutrient_norms_list):
        #Вытаскиваем данные выбранной еды
        food_values_db=FoodDB(food_db)
        food_values_dict = {}
        for id in food_list:
            food_values_dict[id]={"cpfc":food_values_db.get_food_CPFC_by_id(id),"vitamins":food_values_db.get_food_vitamins_by_id(id),
                                  "minerals":food_values_db.get_food_minerals_by_id(id)}

        #Составляем всевозможные уникальные комбинации продуктов
        food_combinations=[]
        for i in range(1, len(food_list)+1):
            els = [list(x) for x in itertools.combinations(food_list, i)]
            food_combinations.extend(els)

        food_combinations_with_coefs=[]
        for combination in food_combinations:
            pass

    def get_food_coef(self):
        return self.food_coef