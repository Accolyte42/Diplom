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
# 1 / N is a normalization factor
# Ampl = (1/N) * np.abs(Ampl_c)[:(N//2)] * 2     # Массив действительных амплитуд АЧХ
# Ampl_phs = (1/N) * np.angle(Ampl_c)[:(N//2)]   # Массив фаз для ФЧХ


# Чтение из файла Cur_FRF_wing.txt массив данных с датчиков
read_file = np.loadtxt("Cur_FRF_wing.txt")
# print(read_file.shape[0])  # 336
freq = read_file[:, 0]
Ampl_c_arr = arr_sensor(read_file)  # Массив перед ф-ций для всех точек
N = read_file.shape[0]  # количество точек
Ampl_arr = (1/N) * np.abs(Ampl_c_arr)    # Массив действительных амплитуд АЧХ
Ampl_phs_arr = (1/N) * np.angle(Ampl_c_arr)   # Массив фаз для ФЧХ
# print(Ampl_c_arr)
# np.savetxt('test1.txt', Ampl_c_arr)

# Рассматриваемый датчик
Src_snsr = Config.Src_snsr
Ampl = Ampl_arr[:, Src_snsr]
Ampl_phs = Ampl_phs_arr[:, Src_snsr]

# Построение графиков
# Построение графика АЧХ
fig = plt.figure()
ax = fig.add_subplot(311)
ax.plot(freq, Ampl, 'g', label='Действ')  # График АЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.grid()
ax.legend()

# Построение графика ФЧХ
ax = fig.add_subplot(312)
ax.plot(freq, Ampl_phs, 'g', label='Мним')  # График ФЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.grid()
ax.legend()

# Построение графика АЧХ для всех датчиков
ax = fig.add_subplot(313)
ax.plot(freq, Ampl_arr, 'g')  # График ФЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.grid()
# Отображение
plt.show()


# Выбранные интервалы для резонансной частоты
w_list = Config.w_list

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
Num_des_r = Config.Num_des_r  # номер искомого резонанса. Нумерация идет по тому, как в w_list диапазоны заданы
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

plt.show()
