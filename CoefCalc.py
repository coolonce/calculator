from NutrientCalculator import NutrientCalculator
from NutrientDB import NutrientDB
from FoodDB import FoodDB
import itertools

class CoefCalc:
    food_coef = {}
    nutr_to_food_map = {
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
    def get_cpfc_and_combinations(self, gender, mass, height, age, diet_type, norms_db, food_db, food_list):
        nc = NutrientCalculator()
        CPFC_list=nc.calculate_nutrients(gender, mass, height, age, diet_type)

        nutrient_norms_db = NutrientDB(norms_db)
        nutrient_norms_list, ash = nutrient_norms_db.get_all_nutrient_values_for_gender(gender)
        nutrient_norms_list = dict(nutrient_norms_list)
        CPFC_list.insert(5,ash)
        result = self.__calculate(food_db, food_list, CPFC_list, nutrient_norms_list)
        return {"cpfc":CPFC_list[:6], "combinations":result}

    def __calculate(self, food_db, food_list, CPFC_list, nutrient_norms_list):
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
            combination_value={"combibation":combination, "overall_coefficient":0.00,
             "overall_cpfc":{"calories":{"value":0.00,"coefficient":0.00},
                             "proteins":{"value":0.00,"coefficient":0.00},
                             "fats":{"value":0.00,"coefficient":0.00},
                             "carbohydrates":{"value":0.00,"coefficient":0.00},
                             "water":{"value":0.00,"coefficient":0.00},
                             "ash":{"value":0.00,"coefficient":0.00}
                             },
             "overall_nutrients":{}
             }
            for id in combination:
                #высчитваем нутриенты
                combination_value["overall_cpfc"]["calories"]["value"]+=food_values_dict[id]["cpfc"]["energy"]
                combination_value["overall_cpfc"]["proteins"]["value"] += food_values_dict[id]["cpfc"]["protein"]
                combination_value["overall_cpfc"]["fats"]["value"] += food_values_dict[id]["cpfc"]["fat"]
                combination_value["overall_cpfc"]["carbohydrates"]["value"] += food_values_dict[id]["cpfc"]["carbohydrate"]
                combination_value["overall_cpfc"]["water"]["value"] += food_values_dict[id]["cpfc"]["water"]
                combination_value["overall_cpfc"]["ash"]["value"] += food_values_dict[id]["cpfc"]["ash"]
                for vitamin in food_values_dict[id]["vitamins"]:
                    temp = {"value":food_values_dict[id]["vitamins"][vitamin], "coefficient":0.00}
                    if( str(vitamin) in combination_value["overall_nutrients"]) == False:
                        combination_value["overall_nutrients"][str(vitamin)]=temp
                    else:
                        combination_value["overall_nutrients"][str(vitamin)]["value"]+=temp["value"]
                for mineral in food_values_dict[id]["minerals"]:
                    temp = {"value":food_values_dict[id]["minerals"][mineral], "coef":0.00}
                    if (str(mineral) in combination_value["overall_nutrients"]) == False:
                        combination_value["overall_nutrients"][str(mineral)]=temp
                    else:
                        combination_value["overall_nutrients"][str(mineral)]["value"] += temp["value"]
            #высчитываем коэффиценты комбинации
            nutrients_coefficients_list = []
            combination_value["overall_cpfc"]["calories"]["coefficient"]=combination_value["overall_cpfc"]["calories"]["value"]/CPFC_list[0]
            nutrients_coefficients_list.append(combination_value["overall_cpfc"]["calories"]["coefficient"])

            combination_value["overall_cpfc"]["proteins"]["coefficient"]=combination_value["overall_cpfc"]["proteins"]["value"] / CPFC_list[1]
            nutrients_coefficients_list.append(combination_value["overall_cpfc"]["proteins"]["coefficient"])

            combination_value["overall_cpfc"]["fats"]["coefficient"]=combination_value["overall_cpfc"]["fats"]["value"] / CPFC_list[2]
            nutrients_coefficients_list.append(combination_value["overall_cpfc"]["fats"]["coefficient"])

            combination_value["overall_cpfc"]["carbohydrates"]["coefficient"]=combination_value["overall_cpfc"]["carbohydrates"]["value"] / CPFC_list[3]
            nutrients_coefficients_list.append(combination_value["overall_cpfc"]["carbohydrates"]["coefficient"])

            combination_value["overall_cpfc"]["water"]["coefficient"]=combination_value["overall_cpfc"]["water"]["value"] / CPFC_list[4]
            nutrients_coefficients_list.append(combination_value["overall_cpfc"]["water"]["coefficient"])

            combination_value["overall_cpfc"]["ash"]["coefficient"]=combination_value["overall_cpfc"]["ash"]["value"] / CPFC_list[5]
            nutrients_coefficients_list.append(combination_value["overall_cpfc"]["ash"]["coefficient"])

            for key, value in self.nutr_to_food_map.items():
                tmp = combination_value["overall_nutrients"][str(value)]["value"] / nutrient_norms_list[int(key)]
                tmp = tmp if tmp < 3 else tmp / 1000
                combination_value["overall_nutrients"][str(value)]["coefficient"] = tmp
                nutrients_coefficients_list.append(combination_value["overall_nutrients"][str(value)]["coefficient"])
            #Высчитываем общий коэффицент комбинации
            combination_value["overall_coefficient"]=sum(nutrients_coefficients_list)/len(nutrients_coefficients_list)
            food_combinations_with_coefs.append(combination_value)
        return food_combinations_with_coefs


    def get_food_coef(self):
        return self.food_coef