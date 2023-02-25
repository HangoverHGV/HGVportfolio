import math

const1 = math.sqrt(3)
rez_al = 0.028
rez_cu = 0.0175
sectiuni = [1, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240]


pamant_electrica_al = [0, 0, 0, 36, 45, 60, 78, 99, 118, 142, 176, 221, 242, 270, 308, 363]
aer_electrica_al = [0, 0, 0, 27, 34, 47, 63, 83, 102, 124, 158, 190, 220, 252, 289, 339]

pamant_electrica_cu = [0, 26, 34, 44, 56, 75, 98, 128, 157, 185, 228, 275, 313, 353, 399, 464]
aer_electrica_cu = [0, 18.5, 25, 34, 43, 60, 80, 106, 131, 159, 202, 244, 282, 324, 371, 436]






def SectiuneAl(P, L, pozare, tip):

    red = True

    if tip == 'monofazic':
        U = 230
    if tip == 'trifazic':
        U = 400

    P = P * 1000
    I = P / 636.6



    res_al = [L * rez_al/i for i in sectiuni]
    DU_al = [const1 * I * i for i in res_al]
    DUp_al = [i / U * 100 for i in DU_al]
    DP_al = []
    n = len(sectiuni)
    chose = []
    chose.append(I)
    for i in range(0, n):
        val = (res_al[i] * sectiuni[i] ** 2) / (U ** 2) * 10 ** 3
        DP_al.append(val)
    for i in range(0, n):
        if pozare.lower() == 'aerian':
            if aer_electrica_al[i] > I and DUp_al[i] < 5:
                red = False
                chose.append(DUp_al[i])
                chose.append(DU_al[i])
                chose.append(DP_al[i])
                chose.append(sectiuni[i])
                chose.append(red)
                break
        if pozare.lower() == 'subteran':
            if pamant_electrica_al[i] > I and DUp_al[i] < 5:
                red = False
                chose.append(DUp_al[i])
                chose.append(DU_al[i])
                chose.append(DP_al[i])
                chose.append(sectiuni[i])
                chose.append(red)
                break

    if red:
        chose.append(DUp_al[-1])
        chose.append(DU_al[-1])
        chose.append(DP_al[-1])
        chose.append(sectiuni[-1])
        chose.append(red)

    return chose


def SectiuneCu(P, L, pozare, tip):

    red = True

    if tip == 'monofazic':
        U = 230
    if tip == 'trifazic':
        U = 400

    P = P * 1000
    I = P / 636.6


    res_cu = [L * rez_cu/i for i in sectiuni]
    DU_cu = [const1 * I * i for i in res_cu]
    DUp_cu = [i / U * 100 for i in DU_cu]
    DP_cu = []
    n = len(sectiuni)
    chose = []
    chose.append(I)
    for i in range(0, n):
        val = (res_cu[i] * sectiuni[i] ** 2) / (U ** 2) * 10 ** 3
        DP_cu.append(val)
    for i in range(0, n):
        if pozare.lower() == 'aerian':
            if aer_electrica_cu[i] > I and DUp_cu[i] < 5:
                red = False
                chose.append(DUp_cu[i])
                chose.append(DU_cu[i])
                chose.append(DP_cu[i])
                chose.append(sectiuni[i])
                chose.append(red)
                break
        if pozare.lower() == 'subteran':
            if pamant_electrica_cu[i] > I and DUp_cu[i] < 5:
                red = False
                chose.append(DUp_cu[i])
                chose.append(DU_cu[i])
                chose.append(DP_cu[i])
                chose.append(sectiuni[i])
                chose.append(red)
                break
    if red:
        chose.append(DUp_cu[-1])
        chose.append(DU_cu[-1])
        chose.append(DP_cu[-1])
        chose.append(sectiuni[-1])
        chose.append(red)

    return chose

