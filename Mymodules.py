import matplotlib.pyplot as plt
import xlrd
# import os
import math
import numpy as np


# import sympy
# from numpy import array, arange, abs as np_abs
# from numpy.fft import fft, fftfreq
# from numpy.random import uniform


def create_worksheet(table, sheet):
    # возвращает рабочий лист из Excel файла с именем Table
    # и страницы sheet
    workbook = xlrd.open_workbook(table)
    worksheet = workbook.sheet_by_name(sheet)
    return worksheet


def table_data(worksheet, axx):
    # Функция, возвращающая значения для новых осей
    x = []
    y = []
    for i in range(0, worksheet.nrows):
        x.append(worksheet.cell(i, 0).value)
        y.append(abs(worksheet.cell(i, 1).value))  # здесь берем модуль
    if axx == 1:
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
    for i in range(1, len(y) - 1):
        if (y[i] > y[i + 1]) & (y[i] > y[i - 1]):
            indexes.append(i)
            y_out.append(y[i])
    return [y_out, indexes]


def reduce_array(indexes, arr):
    # возвращает массив, элементов с индексами indexes из массива arr
    # мне нужен для получения массива, состоящего только из локальных максимумов
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


def peak_picking_an(index_max, x, y):
    # Реализация метода половинной мощности
    # Делается так: от пика спускаемся в каждую сторону до тех пор,
    # пока у[i] не будет меньше заданного значения, а потом линейной
    # интерполяцией находится значение частоты для левой частоты
    i = index_max
    # print('y/sqrt(2)',y[index_max]/(2**(1/2)))
    while y[i] >= y[index_max] / (2 ** (1 / 2)):
        i -= 1
    temp = line_2_dots(x[i], y[i], x[i + 1], y[i + 1])
    x_left = (y[index_max] / (2 ** (1 / 2)) - temp[1]) / temp[0]
    # print('x_left', x_left)

    # то же самое, но для правой точки
    i = index_max
    while y[i] >= y[index_max] / (2 ** (1 / 2)):
        i += 1
    temp = line_2_dots(x[i], y[i], x[i - 1], y[i - 1])
    x_right = (y[index_max] / (2 ** (1 / 2)) - temp[1]) / temp[0]
    # print('x_rigth', x_right)

    delta_w = x_right - x_left
    # print(delta_w)
    # print(delta_w)
    print(x[index_max])
    return delta_w / (2 * x[index_max])


def peak_picking(w_arr, a_arr, w_list):
    # Входные параметры: АЧХ  и частота, которую прикидываем резонансной
    # Реализация метода половинной мощности
    # Делается так: от пика спускаемся в каждую сторону до тех пор,
    # пока у[i] не будет меньше заданного значения, а потом линейной
    # интерполяцией находится значение частоты для левой частоты

    step = w_arr[1] - w_arr[0]  # шаг по частотам

    index_max = [0]*len(w_list)
    dempf_arr = [0]*len(w_list)
    w_rez = [0]*len(w_list)

    for i in range(len(w_list)):
        index_l = int((w_list[i][0]) // step)  # индекс левой точки от заданной
        index_r = int((w_list[i][1]) // step)  # индекс правой точки от заданной

        # Получение индекса точки с максимальной амплитудой на участке
        index_max[i] = int(index_l)
        for j in range(index_l, index_r):
            if a_arr[j] > a_arr[index_max[i]]:
                index_max[i] = j

        # создание вектора демпфирований
        dempf_arr[i] = peak_picking_an(index_max[i], w_arr, a_arr)
        w_rez[i] = w_arr[index_max[i]]

    return [w_rez, dempf_arr]


def function_disp(list_a, list_lambda, list_w, t):
    # Функция, аналитически задающая перемещение на определенных частотах
    # list_A - это список амплитуд. list_lambda - это список коэффициентов затухания
    # list_w - список частот возбуждения. list_trans_max - список времен, на которых происходит возбуждение
    # t - аргумент
    y = 0
    for i in range(len(list_a)):
        y += list_a[i] * math.exp(-list_lambda[i] * abs(t)) * math.sin(list_w[i]*2*math.pi * t)
    return y


def analitic_disp_array(list_a, list_lambda, list_w, diapason):
    # daipason -> [max_x, length_step] подразумевается, что они делятся без остатка, хотя могут и не делиться
    # функция, возвращающая список точек по х и по y при применении аналитической функции к аргументу х
    list_x = []
    list_y = []
    for i in range(round(diapason[0] / diapason[1])):
        list_x.append(i * diapason[1])
        list_y.append(function_disp(list_a, list_lambda, list_w, list_x[i]))
    return [list_x, list_y]


def nextpow2(p):
    n = 2
    while p < n:
        n *= 2
    return n



def absol(lst):
    # функция возвращает абсолютные значения списка
    for i in range(len(lst)):
        lst[i] = abs(lst[i])
    return lst


def summa(lst):
    # Возвращает сумму элементов списка
    temp = 0
    for i in range(len(lst)):
        temp += lst[i]
    return temp
