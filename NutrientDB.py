import sqlalchemy

class NutrientDB:
    def __init__(self, database):
        self.database = database
    #Male - 1; Female - 2
    #Возвращает все нутриенты и их значения из базы, в зависимости от пола
    def get_all_nutrient_values_for_gender(self, gender):
        return self.database.execute(sqlalchemy.text("select Nutrient.name as Nutrient_name, Nutrient_has_Gender.value from Nutrient, Gender, Nutrient_has_Gender where Nutrient.idNutrient="
        "Nutrient_has_Gender.Nutrient_idNutrient and Nutrient_has_Gender.Gender_idGender=:idGender"), {'idGender': gender})


