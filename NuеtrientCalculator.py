#Создаю класс, так как удобнее будет работать
#Особенно если представить, что этот калькулятор будет частью модели (если попытаемся в MVC сделать)
class NutrientCalculator:
    #Хоть и есть 6 вариаций этого значений - предположим, что приложением пользуются только работники умственного и лёгкого физ. труда
    calories_coef = 1.5
    def calculate_nutrients(self, gender, mass, height, age, diet_type):
        #Решил выбрать формулу Харриса Бенедикта, так как там учитывается именно текущий вес, а не желаемый
        mev = 0
        if gender == 0: #Для женщин
            mev = 65 + 9.6*mass + 1.8*height - 4.7*age
        else: #Для мужчин
            mev = 66 + 3.7*mass + 6*height - 6.8*age
        #Константа в данном случае
        calories = mev*self.calories_coef
        return (calories, self.proteins_calculation(calories, diet_type), self.fats_calculation(calories, diet_type),
                self.pcarbohydrates_calculation(calories, diet_type))

    def __proteins_calculation(self, calories, type):
        if type==0:
            pass

    def __fats_calculation(self, calories, type):
        return 0

    def __carbohydrates_calculation(self, calories, type):
        return 0