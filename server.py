from flask import Flask, jsonify
from flask import request
import sqlalchemy
from ServerErrorHandlers import InvalidUsage
from NutrientCalculator import NutrientCalculator
from NutrientDB import NutrientDB
from FoodDB import FoodDB

nutrient_norms_connection=sqlalchemy.create_engine('mysql+pymysql://root@localhost/Nutrients')
nutrient_norms = NutrientDB(nutrient_norms_connection)
#Формируем списки норм для мужчин и женщин в формате {"Male":{нормы для мужчин},"Female":{нормы для женщин}
nutrient_norms = {"Male": dict(nutrient_norms.get_all_nutrient_values_for_gender(1).fetchall()),"Female": dict(nutrient_norms.get_all_nutrient_values_for_gender(2).fetchall())}
print(nutrient_norms)

food_db_connection=sqlalchemy.create_engine('mysql+pymysql://root@localhost/nutrition_db')
food_db=FoodDB(food_db_connection)
food_db.get_all_food_vitamins([1, 2])

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
                height = d["data"]["height"]
                gender=-1
                if d["data"]["gender"] == "Female":
                    gender=0
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
                calc = NutrientCalculator()
                result = calc.calculate_nutrients(gender, mass, height, age, diet_type)
                
                #js_res = {"status":"ok","data":result}
                #return jsonify(js_res)
            else:
                raise InvalidUsage('Invalid data format', status_code=400)
        else:
            raise InvalidUsage('invalid data format', status_code=400)
app.run()
"""