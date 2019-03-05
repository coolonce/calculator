from enum import IntEnum
class DietType(IntEnum):
    WEIGHT_LOSS = 1
    WEIGHT_SAVE = 2
    WEIGHT_GAIN = 3

#Создаю класс, так как удобнее будет работать
#Особенно если представить, что этот калькулятор будет частью модели (если попытаемся в MVC сделать)
class NutrientCalculator:
    #Здесь рассчитываем норму калорийности+количество белков,жирова, углеводов

    def calculate_nutrients(self, gender, mass, height, age, diet_type, calories_coef=1.5):
        #Решил выбрать формулу Харриса Бенедикта, так как там учитывается именно текущий вес, а не желаемый
        main_energy_exchange = 0
        if gender == 0: #Для женщин
            main_energy_exchange = 65 + 9.6*mass + 1.8*height - 4.7*age
        else: #Для мужчин
            main_energy_exchange = 66 + 3.7*mass + 6*height - 6.8*age

        energy_loss = main_energy_exchange*calories_coef
        consumption_rate_norm = main_energy_exchange+energy_loss

        calories = self.__calories_interval_calculation(consumption_rate_norm, diet_type)
        proteins = self.__proteins_calculation(consumption_rate_norm, calories, diet_type)
        fats = self.__fats_calculation(consumption_rate_norm, calories, diet_type)
        carbohydrates = self.__carbohydrates_calculation(consumption_rate_norm, calories, proteins, fats, diet_type)

        return (calories, proteins, fats, carbohydrates)

    def __calories_interval_calculation(self, consumption_rate_norm, type):
        if type == DietType.WEIGHT_LOSS:
            return consumption_rate_norm - consumption_rate_norm*0.22
        elif type == DietType.WEIGHT_SAVE:
            return consumption_rate_norm
        else:
            return consumption_rate_norm + consumption_rate_norm*0.25

    def __proteins_calculation(self, consumption_rate_norm,calories, type):
        if type == DietType.WEIGHT_LOSS:
            return consumption_rate_norm*0.18/4
        elif type == DietType.WEIGHT_SAVE:
            return calories*0.18/4
        else:
            return calories*0.2/4

    def __fats_calculation(self, consumption_rate_norm,calories, type):
        if type == DietType.WEIGHT_LOSS:
            return consumption_rate_norm*0.32/9
        elif type == DietType.WEIGHT_SAVE:
            return calories*0.32/9
        else:
            return calories*0.3/9

    def __carbohydrates_calculation(self, consumption_rate_norm, calories, proteins, fats, type):
        if type == DietType.WEIGHT_LOSS:
            return (calories - (proteins*4+fats*9))/4
        elif type == DietType.WEIGHT_SAVE:
            return calories*0.5/4
        else:
            return calories*0.5/4