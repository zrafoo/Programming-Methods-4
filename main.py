import time
from collections import defaultdict
import math
from random import randint


class XORShift1:

    def __init__(self, seed=int(time.time() // 11 * 1000)):
        self.state = seed * int(time.time() * 1000) & 0xFFFFFFFF

    def __call__(self):
        self.state ^= (self.state << 13) & 0xFFFFFFFF
        self.state ^= (self.state >>17) & 0xFFFFFFFF
        self.state ^= (self.state << randint(3, 6)) & 0xFFFFFFFF
        return self.state % 10000

class XORShift2:

    def __init__(self, seed=int(time.time() // randint(10, 12) * 1000)):
        self.state = seed * int(time.time() * 1000) & 0xFFFFFFFF

    def __call__(self):
        self.state ^= (self.state << randint(14, 18)) & 0xFFFFFFFF
        self.state ^= (self.state >>randint(14, 18)) & 0xFFFFFFFF
        self.state ^= (self.state << randint(3, 6)) & 0xFFFFFFFF
        return self.state % 10000


def xi2_checker(posled, max_value):
    n = round(1 + 3.322 * math.log(len(posled)))
    xp = [-2.33, -1.64, -0.674, 0, 0.674, 1.64, 2.33]
    xi_prob = [1, 5, 25, 50, 75, 95, 99]
    xi_standart = [(n - 1 + math.sqrt(2 * (n - 1)) * xp[i] + 2 / 3 * pow(xp[i], 2) - 2 / 3, xi_prob[i]) for i in range(len(xp))]
    count_intervals = defaultdict(lambda: 0)
    for i in posled:
        for j in range(n):
            if j * max_value / n <= i <= (j + 1) * max_value / n:
                count_intervals[j] += 1
                break
    xi = sum([pow((i - len(posled) / n), 2) for k, i in count_intervals.items()]) / (len(posled) / n)
    for count, xi_i in enumerate(xi_standart):
        if xi < xi_i[0]:
            return xi_standart[count][1], xi_standart[min(count + 1, len(xi_standart) -
                                                      1)][1]
    else:
        return 0, 1

countOfSamples = 10
countOfRandoms = 50

generator = XORShift1()
samples = defaultdict()
means = defaultdict()
variances = defaultdict()
deviation=defaultdict()
varCoefficient = defaultdict()
xiValuables = defaultdict()



for i in range(countOfSamples):
    samples[i] = [generator() for _ in range(countOfRandoms)]
    # генерируем выборку
    means[i] = sum(samples[i]) / countOfRandoms
    # Вычисляем мат ожидание
    variances[i] = sum([pow((el - means[i]), 2) for el in samples[i]]) / countOfRandoms  # вычисляем дисперсию
    deviation[i]=math.sqrt(variances[i])
    varCoefficient[i] = math.sqrt(variances[i]) / means[i] * 100
    # вычисляем коэффициент вариации
    xiValuables[i] = xi2_checker(samples[i], 10000)



print("Результат:", '\n')
for i in range(countOfSamples):
    print("Выборка - ",i+1, ", Среднее - ",str(round(means[i])), ", Отклонение - ",str(round(deviation[i])), ", Коэффициент вариации, % - ",str(round(varCoefficient[i])),
          "Однородность - ", str(varCoefficient[i] < 33),"Вероятность равномерности, % - ",str(str(round(xiValuables[i][0])) + '-' +
              str(round(xiValuables[i][1]))))