# Получение координаты по х и по у аналитически через коэффициенты
list_A_1 = [1, 5, 6]
list_lambda_1 = [0.1, 0.2, 1]
list_w_1 = [10, 50, 70]
diapason_1 = [70, 0.001]
displ_arr1 = an_displ(list_A_1, list_lambda_1, list_w_1, diapason_1)

list_A_2 = [2, 4, 7]
list_lambda_2 = [0.05, 0.15, 1.2]
list_w_2 = [10, 50, 70]
diapason_2 = [70, 0.001]
displ_arr_2 = an_displ(list_A_2, list_lambda_2, list_w_2, diapason_2)

list_A_3 = [7, 3, 8]
list_lambda_3 = [0.3, 0.10, 1.1]
list_w_3 = [10, 50, 70]
diapason_3 = [70, 0.001]
displ_arr_3 = an_displ(list_A_3, list_lambda_3, list_w_3, diapason_3)

list_A_4 = [4, 5, 6]
list_lambda_4 = [0.35, 0.20, 1.5]
list_w_4 = [10, 50, 70]
diapason_4 = [70, 0.001]
displ_arr_4 = an_displ(list_A_4, list_lambda_4, list_w_4, diapason_4)

displ_arr = displ_arr1 + displ_arr_2 + displ_arr_3 + displ_arr_4

















fig = plt.figure()
counter = 1
for i in range(len(Y)):
    for j in range(len(Y)):
        print(i, j)
        f, Gyy[i][j] = csd(Y[i], Y[j], fs, nperseg=dscrt)
        if i == j:
            Test[i] = Gyy[i][j]
        ax = fig.add_subplot(len(Y), len(Y), counter)
        ax.plot(f, Gyy[0][0], 'g', label=str([i,j]))  # График CSD
        ax.set_xlabel('FREQ')
        ax.set_ylabel('CSD431214321')
        ax.legend()
        ax.grid()
        counter = counter + 1



counter = 1
flag = 1
for i in range(len(Y)):
    for j in range(len(Y),0,-1):
        print(i, j)
        if i == 1 and flag:
            ax = fig.add_subplot(len(Y), len(Y), counter)
            ax.plot(f, Gyy[0][0], 'g', label=str([i, j]))  # График CSD
            ax.set_xlabel('FREQ')
            ax.set_ylabel('До')
            ax.legend()
            ax.grid()
            counter = counter + 1
            flag = 0
        f, Gyy[i][j] = csd(Y[i], Y[j], fs, nperseg=dscrt)
        if i == j:
            Test[i] = Gyy[i][j]
        ax = fig.add_subplot(len(Y), len(Y), counter)
        ax.plot(f, Gyy[0][0], 'g', label=str([i,j]))  # График CSD
        ax.set_xlabel('FREQ')
        ax.set_ylabel('CSD431214321')
        ax.legend()
        ax.grid()
        if counter == 9:
            break
        counter = counter + 1




fig = plt.figure()
ax = fig.add_subplot(311)
ax.plot(f, Test[0], 'g', label='0 0')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(312)
ax.plot(f, Test[1], 'g', label='1 1')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(313)
ax.plot(f, Test[2], 'g', label='2 2')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

fig = plt.figure()
ax = fig.add_subplot(331)
ax.plot(f, Gyy[0][0], 'g', label='0 0')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(332)
ax.plot(f, Gyy[0][1], 'g', label='0 1')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(333)
ax.plot(f, Gyy[0][2], 'g', label='0 2')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(334)
ax.plot(f, Gyy[1][0], 'g', label='1 0')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(335)
ax.plot(f, Gyy[1][1], 'g', label='1 1')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(336)
ax.plot(f, Gyy[1][2], 'g', label='1 2')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(337)
ax.plot(f, Gyy[2][0], 'g', label='2 0')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(338)
ax.plot(f, Gyy[2][1], 'g', label='2 1')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()

ax = fig.add_subplot(339)
ax.plot(f, Gyy[2][2], 'g', label='2 2')  # График CSD
ax.set_xlabel('FREQ')
ax.set_ylabel('CSD')
ax.legend()
ax.grid()