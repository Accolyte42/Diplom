import matplotlib.pyplot as plt
import xlrd
import os
import math
import sympy
from numpy import array, arange, abs as np_abs
from numpy.fft import fft, fftfreq
from numpy.random import uniform


def create_worksheet(table, sheet):
    # возвращает рабочий лист из Excel файла с именем Table
    # и страницы sheet
    workbook = xlrd.open_workbook(table)
    worksheet = workbook.sheet_by_name(sheet)
    return worksheet


def table_data(worksheet, Axx):
    # Функция, возвращающая значения для новых осей
    x = []
    y = []
    for i in range(0,worksheet.nrows):
        x.append(worksheet.cell(i,0).value)
        y.append(abs(worksheet.cell(i,1).value)) # здесь берем модуль
    if Axx == 1:
        return x
    else:
        return y


def graphic_my(x, y):
    # функция построения графика по массиву x-ов и y-ов
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='Time', ylabel='Amplitude')
    plt.show()


def maxes_of_list_y(y):
    # функция получения массива индексов локальных максимумов
    indexes = []
    y_out = []
    for i in range(1,len(y)-1):
        if (y[i] > y[i+1]) & (y[i] > y[i-1]):
            indexes.append(i)
            y_out.append(y[i])
    return [y_out, indexes]


def reduce_array(indexes, arr):
    # возвращает массив, элементов с индексами indexes из массива arr
    # по сути нужен для получения массива, состоящего только из локальных максимумов
    final_arr = []
    for i in indexes:
        final_arr.append(arr[i])
    return final_arr


def reduce_loop(amount, x, y):
    # функция, убирающая amount раз элементы около локальных максимумов
    # возвращает матрицу, один столбец - х, а другой - у
    for i in range(amount):
        temp = maxes_of_list_y(y)
        ind = temp[1]
        x = reduce_array(ind, x)
        y = reduce_array(ind, y)
        # print(len(y))
    return [x, y]


def some_rezonanses(amount, y, x):
    # функция возвращает матрицу с amount максимумами: координаты y,x и индексами
    temp = maxes_of_list_y(y)
    maximums = sorted(temp[0], reverse=True)
    # print(maximums)
    maxes = []
    indexes = []
    xes = []
    for i in range(amount):
        maxes.append(maximums[i])
        # print(maxes)
        indexes.append(y.index(maximums[i]))
        # print(indexes)
        xes.append(x[indexes[i]])
    return [maxes, xes, indexes]


def line_2_dots(x1, y1, x2, y2):
    # коэффициенты прямой по двум точкам
    k = (y1 - y2) / (x1 - x2)
    b = y2 - k * x2
    return [k, b]


def peak_picking_method(index_max, y, x):
    # Реализация метода половинной мощности
    # Делается так: от пика спускаемся в каждую сторону до тех пор,
    # пока у[i] не будет меньше заданного значения, а потом линейной
    # интерполяцией находится значение частоты для левой частоты
    i = index_max
    # print(y[index_max]/(2**(1/2)))
    while y[i] > y[index_max]/(2**(1/2)):
        i -= 1
    temp = line_2_dots(x[i],y[i],x[i+1],y[i+1])
    x_left = ( y[index_max]/(2**(1/2)) - temp[1] ) / temp[0]
    # print(x_left)

    # то же самое, но для правой точки
    i = index_max
    while y[i] > y[index_max] / (2 ** (1 / 2)):
        i += 1
    temp = line_2_dots(x[i], y[i], x[i - 1], y[i - 1])
    x_right = ( y[index_max]/(2**(1/2)) - temp[1] ) / temp[0]
    # print(x_right)

    delta_w = x_right - x_left
    # print(delta_w)
    return delta_w/(2*x[index_max])


def Function_ACHX (list_A, list_lambda, list_w, list_trans_max, t):
    # Функция, аналитически задающая возбуждение на определенных частотах
    # list_A - это список амплитуд. list_lambda - это список коэффициентов затухания
    # list_w - список частот возбуждения. list_trans_max - список частот, на которых происходит возбуждение
    # t - аргумент
    y = 0
    for i in range(len(list_A)):
        y += list_A[i]*math.exp( -list_lambda[i] * abs(t - list_trans_max[i]) )*math.sin(list_w[i]*(t - list_trans_max[i]))
    return y


def Analitic_ACHX_array (list_A, list_lambda, list_w, list_trans_max, diapason):
    # daipason -> [max_x, length_step] подразумевается, что они делятся без остатка, хотя могут и не делиться
    # функция, возвращающая список точек по х и по y при применении аналитической функции к аргументу х
    list_x = []
    list_y = []
    for i in range( round(diapason[0]/diapason[1]) ):
        list_x.append(i*diapason[1])
        list_y.append( Function_ACHX(list_A, list_lambda, list_w, list_trans_max, list_x[i]) )
    return [list_x, list_y]


def absol (list):
    # функция возвращает абсолютные значения списка
    for i in range(len(list)):
        list[i] = abs(list[i])
    return list


def summa (list):
    # Возвращает сумму элементов списка
    temp = 0
    for i in range(len(list)):
        temp += list[i]
    return temp


# print(os.listdir()) # нужно, чтобы правильно ввести название excel-файла

# получение листа из таблицы
# worksheet = create_worksheet('Signal_Table.xls', 'Sheet_1')

# Задание функции АЧХ аналитически для проверки
# Получение координаты по х и по у аналитически через коэффициенты
list_A = [10, 20]
list_lambda = [0.1, 5]
list_w = [10, 50]
list_trans_w = [2, 10]
diapason = [10, 0.01]
temp_f = Analitic_ACHX_array(list_A, list_lambda, list_w, list_trans_w, diapason)
x = temp_f[0]
y = temp_f[1]
# y = absol(temp_f[1])


# Вытаскиваниие из лист координат х и у точек
# x = table_data(worksheet, 1)
# y = table_data(worksheet, 2)

# убирание точек вокруг локальных максимумов
# в принципе, здесь надо делать сглаживание/аппроксимацию/интерполяцию
# для входных данных, т.к. пик может получиться слишком тонким
# a = (reduce_loop(1, x, y))
# x = a[0]
# y = a[1]

# Дискретное преобразование Фурье над двумерным массивом
spectrum = fft(y, n=None, axis=-1)
spectrum = spectrum[:len(spectrum)//2]
print(spectrum)
Disc_freq = 2*math.pi/diapason[0]

# Получение матрицы с 5 локальными экстремумами, отсортированными по убыванию
# Extremums = some_rezonanses(2, y, x)
# print(Extremums[0], "\n", Extremums[1], "\n", Extremums[2] )

# print(sympy.nsolve([summa( math.log(A) + y[Extremums[2][0]] - lmb*(x[Extremums[2][0]] - 10) ),summa(( math.log(A) + y[Extremums[2][0]] - lmb*(x[Extremums[2][0]] - 10) )*(x[Extremums[2][0]] - 10)]   ) )


# Применение метода половинной мощности
# for i in range(2):
#     print("Демфирование для ", i+1, " резонанса ", peak_picking_method(Extremums[2][i], y, x))

# Построение графика
# plt.plot(temp_f[0],temp_f[1])
plt.plot(fftfreq(len(spectrum), Disc_freq), absol(spectrum)/len(spectrum) )
plt.show()
# добавил преобразоване Фурье
# Добавил ещё что-то
