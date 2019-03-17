from enum import IntEnum
class DietType(IntEnum):
    WEIGHT_LOSS = 1
    WEIGHT_SAVE = 2
    WEIGHT_GAIN = 3

#Создаю класс, так как удобнее будет работать
#Особенно если представить, что этот калькулятор будет частью модели (если попытаемся в MVC сделать)
class NutrientCalculator:
    #Здесь рассчитываем норму калорийности+количество белков,жирова, углеводов

    def calculate_nutrients(self, gender, mass, height, age, diet_type, calories_coef=1.4):
        #алгоритм Харриса-Бенедикта используется при похудении
        #в остальных же случаях используется алгоритм Миффлина-Сан Жеора
        main_energy_exchange = 0
        if gender == 2: #Для женщин
            if diet_type == DietType.WEIGHT_LOSS:
                main_energy_exchange = 65 + 9.6*mass + 1.8*height - 4.7*age
            else:
                main_energy_exchange = 10*mass + 6.25*height - 5*age -161
        else: #Для мужчин
            if diet_type == DietType.WEIGHT_LOSS:
                main_energy_exchange = 66 + 3.7*mass + 6*height - 6.8*age
            else:
                main_energy_exchange = 10 * mass + 6.25 * height - 5*age + 5
        energy_loss = main_energy_exchange*calories_coef

        calories = self.__calories_interval_calculation(energy_loss, diet_type)
        proteins = self.__proteins_calculation(energy_loss, calories, diet_type)
        fats = self.__fats_calculation(energy_loss, calories, diet_type)
        carbohydrates = self.__carbohydrates_calculation(energy_loss, calories, proteins, fats, diet_type)
        water = mass*31/2 if gender==0 else mass*35/2
        sugar= carbohydrates/10
        fiber=20
        cholesterol=300
        #просто предпологаю, что крахмальных углеводов должно быть 90% всех углеводов -- кол-во пищевых волокон
        starch=carbohydrates-sugar-fiber
        #с википедии
        trans_fats=calories/100
        #Золу надо добавлять уже позже, после получения нормы минералов
        return [calories, proteins, fats, carbohydrates, water, sugar, fiber, starch, cholesterol, trans_fats]

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

