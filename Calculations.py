import csv
import numpy as np
import math
from collections import defaultdict

import requests

OUR_USER = 13
WORKING_DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri')

def getTopFive(sim:list):
    top5 = []  # Индексы похожих юзеров
    simGrades = list(sim)
    simGrades.sort(reverse=True)
    taken = 0
    for a in simGrades:
        whichUser = sim.index(a)
        while whichUser in top5:
            whichUser = sim.index(a, whichUser + 1)
        top5.append(whichUser)
        taken += 1
        if taken == 5: break
    return top5

with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    raw_data = [raw_data[1:] for raw_data in reader][1:]
    data = np.asarray(raw_data, float) #Прочли в матрицу
    '''
    for a in data:
        print(','.join(a))
    '''
with open('context.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    raw_data = [raw_data[1:] for raw_data in reader][1:]
    cont = np.asarray(raw_data) #Прочли в матрицу
    #print(cont[OUR_USER])

sim = [0]*40
average = [0] * 40
#Рассматриваем нашего пользователя (14)
u = 0
for user in data:
    count = 0
    for myVal in user:
        if int(myVal) != -1:
            count+=1
            average[u]+=int(myVal)
    average[u]/=count
    if u == OUR_USER:
        u+=1
        continue #Скипнули расчет схожести для нашего пользователя
    A = 0
    B, C = 0,0
    film = 0
    for myVal in data[OUR_USER]:
        if int(myVal) != -1 and int(user[film]) != -1:  # Нашли оцененный обоими пользователями фильм
            A+=int(myVal)*int(user[film])
            B+=int(myVal)**2
            C+= int(user[film]) ** 2
        film += 1
    sim[u]=(A/math.sqrt(B))/math.sqrt(C)

    u += 1


sim = [round(a,4) for a in sim]
average = [round(a, 4) for a in average]

# Берем топ5
top5 = getTopFive(sim)

# top5 = [32,14,37,33,36]
#print("influenced by " + str([a + 1 for a in top5]))
#print([sim[a] for a in top5])

film = 0
firstTask = {}
films = [] # Один из этих фильмов мы порекомендуем
maxGrade = 0
maxGradeI=0
for val in data[OUR_USER]:
    if int(val) == -1: #Нашли в строке неоцененный фильм
        data[OUR_USER][film] = 0 #Не забыли сбросить перед дальнейшими вычислениями
        simBoth = 0
        for simUser in top5:
            if int(data[simUser][film]) != -1:
                simBoth += abs(sim[simUser])
                data[OUR_USER][film]+= sim[simUser] * (data[simUser][film] - average[simUser])
        data[OUR_USER][film] /= simBoth
        data[OUR_USER][film] += average[OUR_USER]

        films.append(film) #для рекомендации
        if data[OUR_USER][film] > maxGrade:
            maxGrade = data[OUR_USER][film]
            maxGradeI = film

        firstTask["movie " + str(film+1)] = round(data[OUR_USER][film],2)
        print('"movie ' + str(film+1)+'": ' +str(round(data[OUR_USER][film],2)))
    film+=1
#print(data[OUR_USER])
print(firstTask)

MathW = {} # в рабочие дни
MathH = {} # в выходные дни
reliable={} #во сколько раз фильм интереснее в будние, чем в выходные
nonReliable={} #во сколько раз фильм интереснее в будние, чем в выходные
for f in films:
    MathW["M"] = 0 #Мат.ожидание
    MathW["M2"] = 0  # Мат.ожидание квадрата
    MathW["C"] = 0  # колво просмотров
    MathH["M"] = 0 #Мат.ожидание
    MathH["M2"] = 0  # Мат.ожидание квадрата
    MathH["C"] = 0  # колво просмотров
    u=0
    for user in data:
        if u == OUR_USER:
            u+=1
            continue
        if user[f] > 0:
            if cont[u][f] in WORKING_DAYS:
                MathW["C"]+=1
                MathW["M"]+=user[f]
                MathW["M2"]+= user[f] ** 2
            else:
                MathH["C"] += 1
                MathH["M"] += user[f]
                MathH["M2"] += user[f] ** 2
        u+=1
    MathW["M"] = round(MathW["M"]/MathW["C"],2)
    MathH["M"] = round(MathH["M"]/MathH["C"],2)
    MathW["M2"] = round(MathW["M2"] / MathW["C"], 2)
    MathH["M2"] = round(MathH["M2"] / MathH["C"], 2)

    MathW["Q"] = round(math.sqrt(MathW["M2"]-MathW["M"]**2),2) #Среднекв отклонение в будние дни
    MathH["Q"] = round(math.sqrt(MathH["M2"] - MathH["M"] ** 2),2) #Среднекв отклонение в целом

    #Оценка достоверности случайной величины
    rel=abs(MathW["M"]-MathH["M"])/math.sqrt((MathW["Q"]/math.sqrt(MathW["C"]-1))**2+(MathH["Q"]/math.sqrt(MathH["C"]-1))**2)
    if rel >= 2: #Величина достоверна
        reliable[f]=MathW["M"]/MathH["M"]
        reliable[f] *= reliable[f] #Насколько фильм интереснее для просмотра в будние
    else:
        nonReliable[f]=MathW["M"]/MathH["M"]
        nonReliable[f] *= nonReliable[f]
'''
    print(str(MathW["M"]) + " " + str(MathH["M"]), end = ' | ')
    print(str(MathW["Q"]) + " " + str(MathH["Q"]), end=' | ')
    print(MathW["C"]/MathH["C"]/5*2)
    print(MathW["C"], end=' ')
    print(rel)
'''

def bestMovie(film_list):
    mx = 0
    mxi = 0
    for ind, item in film_list.items():
        if item>mx:
            mx = item
            mxi = ind
    if mx >= 3:
        return mxi
    else:
        return -1
def goodMovie(film_list):
    best = bestMovie(nonReliable)
    if best == -1:
        best = maxGradeI  # мы сдались
    return best


best = -1
if len(reliable) > 0:
    best = bestMovie(reliable)
    if best == -1:

        best = goodMovie(nonReliable)
else:
    best = goodMovie(nonReliable)

print(best+1)


reg_a = 'https://cit-home1.herokuapp.com/api/rs_homework_1'
jsargs = {
    "user":14,
    "1": firstTask,
    "2": {"movie " + str(best+1) : firstTask["movie "+str(best+1)]}
}
head = {'content-type': 'application/json'}
print()

r = requests.post(reg_a, json=jsargs,headers=head)
print(r.json())
