from flask import Flask, jsonify
from flask import request
import sqlalchemy
from ServerErrorHandlers import InvalidUsage
from NutrientCalculator import NutrientCalculator
from NutrientDB import NutrientDB
from FoodDB import FoodDB
from CoefCalc import CoefCalc

"""
Male - 1; Female - 2
"""

app = Flask(__name__)

@app.errorhandler(InvalidUsage)
def handler_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/', methods = ['POST'])
def test_handler():
    if request.is_json:
        d = request.get_json()
        if "status" in d:
            if d["status"]=="ok" :

                nutrient_norms_connection = sqlalchemy.create_engine('mysql+pymysql://root@localhost/Nutrients')
                food_db_connection = sqlalchemy.create_engine('mysql+pymysql://root@localhost/nutrition_db')

                height = d["data"]["height"]
                gender=-1
                if d["data"]["gender"] == "Female":
                    gender=2
                else:
                    gender=1
                mass = d["data"]["mass"]
                age = d["data"]["age"]
                diet_type=-1
                if d["data"]["diet type"] == "LOSS":
                    diet_type=1
                elif d["data"]["diet type"] == "SAVE":
                    diet_type=2
                else:
                    diet_type=3
                food_list=d["data"]["food_list"]
                calc = CoefCalc()
                calculations_result = calc.get_cpfc_and_combinations(gender, mass, height, age, diet_type, nutrient_norms_connection, food_db_connection, food_list)
                #дневная норма бжу, калорий, воды(полученной из еды), золы
                cpfc = {"calories":calculations_result["cpfc"][0], "proteins":calculations_result["cpfc"][1], "fats":calculations_result["cpfc"][2],
                        "carbohydrates":calculations_result["cpfc"][3],"water":calculations_result["cpfc"][4], "ash": calculations_result["cpfc"][5]}

                js_res = {"status":"ok","data":{"cpfc":cpfc, "combinatons":calculations_result["combinations"]}}
                return jsonify(js_res)
            else:
                raise InvalidUsage('Invalid data format', status_code=400)
        else:
            raise InvalidUsage('invalid data format', status_code=400)
app.run()
