import sqlalchemy

class NutrientDB:
    nutrient_norms = []
    def __init__(self, database):
        self.database = database
    #Male - 1; Female - 2
    #Возвращает все нутриенты и их значения из базы, в зависимости от пола
    #Также возвращает значение необходимой золы
    def get_all_nutrient_values_for_gender(self, gender):
        self.nutrient_norms = self.database.execute(sqlalchemy.text("select Nutrient_idNutrient, value from Nutrient_has_Gender where Nutrient_has_Gender.Gender_idGender=:idGender"), {'idGender': gender})
        mineral_sum=0
        for nutrient in self.nutrient_norms:
            #константы - айдишники минералов в базе
            if nutrient[0] in [14,15,16,17,20,21,23,24,25,28]:
                mineral_sum+=nutrient[1]
        return self.nutrient_norms, mineral_sum
