# import os
import math
import matplotlib.pyplot as plt
import numpy as np
from Mymodules import analitic_displ_array as an_displ
from Mymodules import peak_picking, one_degree_coef, h_per, arr_sensor
import Config

# print(os.listdir()) # нужно, чтобы правильно ввести название excel-файла

# получение листа из таблицы
# worksheet = create_worksheet('Signal_Table.xls', 'Sheet_1')

# Задание функции АЧХ аналитически для проверки
# Получение координаты по х и по у аналитически через коэффициенты
list_A = [1, 5]
list_lambda = [0.1, 0.2]
list_w = [8, 14]
diapason = [70, 0.01]
displ_arr = an_displ(list_A, list_lambda, list_w, diapason)

# fig = plt.figure()
# plt.plot(displ_arr[0], displ_arr[1], 'g')
# plt.xlim([0, 5])
# plt.show()

## Дискретное преобразование Фурье над двумерным массивом
# Ampl_c = np.fft.fft(displ_arr[1])  # Массив комплексных амплитуд в АЧХ
# N = len(displ_arr[1])  # количество точек
# freq = np.linspace(0, 1/(displ_arr[0][1] - displ_arr[0][0]), N)[:(N//2)]
# Ampl = (1/N) * np.abs(Ampl_c)[:(N//2)] * 2     # Массив действительных амплитуд АЧХ
# Ampl_phs = (1/N) * np.angle(Ampl_c)[:(N//2)]   # Массив фаз для ФЧХ


# Чтение из файла Cur_FRF_wing.txt массив данных с датчиков
read_file = np.loadtxt("Cur_FRF_wing.txt")
# print(read_file.shape[0])  # 336
freq = read_file[:, 0]
Ampl_c = arr_sensor(read_file)
N = read_file.shape[0]  # количество точек
Ampl = (1/N) * np.abs(Ampl_c)[:(N)] * 2     # Массив действительных амплитуд АЧХ
Ampl_phs = (1/N) * np.angle(Ampl_c)[:(N)]   # Массив фаз для ФЧХ
# print(Ampl_c)
# np.savetxt('test1.txt', Ampl_c)

# Построение графиков
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(freq, Ampl, 'g', label='Эксперимент')  # График АЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.legend()

plt.show()



# Выбранные интервалы для резонансной частоты
w_list = [[6,   9],
          [12, 16]]

# Получение по МПМ демпфирования для заданной частоты
dempf = peak_picking(freq, Ampl, w_list)  # демпфирование по МПМ
print('Найденный резонансные частоты', dempf[0], '\nНайденные демпфирования', dempf[1])
print('Лог декр зат ', dempf[0][0]*2*math.pi*dempf[1][0], ',', dempf[0][1]*2*math.pi*dempf[1][1])
print('Резонансные амплитуды ', dempf[2][0], ' ,', dempf[2][1])

# Погрешности логарифм декремента
inaccur_deckr = [0]*len(list_lambda)
inaccur_chastot = [0]*len(list_lambda)
for i in range(len(list_lambda)):
    inaccur_deckr[i] = abs( (dempf[0][i]*2*math.pi*dempf[1][i] - list_lambda[i])/list_lambda[i] )
    inaccur_chastot[i] = abs( (list_w[i]-dempf[0][i])/list_w[i] )
print('Погрешность логарифм декремент', inaccur_deckr)
print('Погрешность резонансных частот', inaccur_chastot)

# нахождение массы, демпф и жесткости для одностеп системы
Num_des_r = 0  # номер искомого резонанса
[m, c, k] = one_degree_coef(dempf[0][Num_des_r], dempf[1][Num_des_r], dempf[2][Num_des_r])

# массив точек АЧХ для одностеп системы
arr_1_deg = [0]*len(freq)
for i in range(len(freq)):
    arr_1_deg[i] = h_per(freq[i], m, c, k)

# Построение графиков
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(freq, Ampl, 'g', label='Эксперимент')  # График АЧХ экспериментальный
ax.plot(freq, arr_1_deg, 'b', label='Аналитика для одностепенной')  # График АЧХ для одностеп системы
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.legend()

# plt.show()


# fig, ax = plt.subplots()
# ax.plot(freq, X_phs, 'g')
# plt.show()
