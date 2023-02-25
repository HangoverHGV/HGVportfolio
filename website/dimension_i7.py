import math

const1 = math.sqrt(3)

rez_al = 0.028
rez_cu = 0.0175
sectiuni = [1, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240]


pamant_tub_i7_al = [0, 0, 0, 17.5, 23, 31, 41, 53, 65, 78, 98, 118, 135, 155, 176, 207]
aer_tub_i7_al = [0, 0, 0, 21, 27, 36, 48, 62, 77, 92, 116, 139, 160, 176, 199, 232]
aer_no_tub_i7_al = [0, 0, 0, 25, 32, 44, 59, 73, 90, 110, 140, 170, 197, 227, 259, 305]

pamant_tub_i7_cu = [0, 13, 17.5, 23, 29, 39, 52, 68, 83, 99, 125, 150, 172, 196, 223, 261]
aer_tub_i7_cu = [0, 15, 20, 27, 34, 46, 62, 80, 99, 118, 149, 179, 206, 225, 255, 297]
aer_no_tub_i7_cu = [0, 17.5, 24, 32, 41, 57, 76, 96, 119, 144, 184, 223, 259, 299, 341, 403]

pamant_tub_i7_al_mono = [0, 0, 0, 19.5, 25, 33, 44, 58, 71, 86, 108, 130, 150, 172, 195, 229]
aer_tub_i7_al_mono = [0, 0, 0, 21, 30, 41, 54, 71, 86, 104,131,157,181, 201, 230, 269]
aer_no_tub_i7_al_mono = [0, 0, 0, 28, 36, 49, 66, 83, 103, 125, 160, 160, 195, 226, 261, 298, 352]

pamant_tub_i7_cu_mono = [0, 14, 18.5, 25, 32, 43, 57, 75, 95, 110, 139, 167, 192, 219, 248, 291]
aer_tub_i7_cu_mono = [0, 16.5, 23, 30, 38, 52, 69, 90, 111, 133, 168, 201, 232, 258, 294, 344]
aer_no_tub_i7_cu_mono = [0, 19.5, 27, 36, 46, 63, 85, 112, 138, 168, 213, 258, 299,344, 392, 461]



def SectiuneAl(P, L, pozare, tip):

    red = True

    P = P * 1000

    if tip == 'monofazic':
        U = 230
        I = P / 230
    elif tip == 'trifazic':
        U = 400
        I = P / 636.6

    chose = []
    chose.append(I)

    res_al = [L * rez_al/i for i in sectiuni]
    if tip == 'trifazic':
        DU_al = [const1 * I * i for i in res_al]
    elif tip == 'monofazic':
        DU_al = [I * i for i in res_al]
    DUp_al = [i / U * 100 for i in DU_al]
    DP_al = []

    n = len(sectiuni)

    for i in range(0, n):
        val = (res_al[i] * sectiuni[i] ** 2) / (U ** 2) * 10 ** 3
        DP_al.append(val)
    for i in range(0, n):
        if pozare.lower() == 'aerian_tub':
            if tip == 'trifazic':
                if aer_tub_i7_al[i] > I and DUp_al[i] < 5:
                    red = False
                    chose.append(DUp_al[i])
                    chose.append(DU_al[i])
                    chose.append(DP_al[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
            elif tip == 'monofazic':
                if aer_tub_i7_al_mono[i] > I and DUp_al[i] < 5:
                    red = False
                    chose.append(DUp_al[i])
                    chose.append(DU_al[i])
                    chose.append(DP_al[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
        if pozare.lower() == 'subteran_tub':
            if tip == 'trifazic':
                if pamant_tub_i7_al[i] > I and DUp_al[i] < 5:
                    red = False
                    chose.append(DUp_al[i])
                    chose.append(DP_al[i])
                    chose.append(DU_al[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
            elif tip == 'monofazic':
                if pamant_tub_i7_al_mono[i] > I and DUp_al[i] < 5:
                    red = False
                    chose.append(DUp_al[i])
                    chose.append(DU_al[i])
                    chose.append(DP_al[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
        if pozare.lower() == 'aerian_notub':
            if tip == 'trifazic':
                if aer_no_tub_i7_al[i] > I and DUp_al[i] < 5:
                    red = False
                    chose.append(DUp_al[i])
                    chose.append(DU_al[i])
                    chose.append(DP_al[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
            elif tip == 'monofazic':
                if aer_no_tub_i7_al_mono[i] > I and DUp_al[i] < 5:
                    red = False
                    chose.append(DUp_al[i])
                    chose.append(DU_al[i])
                    chose.append(DP_al[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break

    if red:
        chose.append(DUp_al[-1])
        chose.append(DP_al[-1])
        chose.append(sectiuni[-1])
        chose.append(red)

    return chose


def SectiuneCu(P, L, pozare, tip):

    red = True

    P = P * 1000

    if tip == 'monofazic':
        U = 230
        I = P / U
    elif tip == 'trifazic':
        U = 400
        I = P / 636.6




    chose = []
    chose.append(I)

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
        if pozare.lower() == 'aerian_tub':
            if tip == 'trifazic':
                if aer_tub_i7_cu[i] > I and DUp_cu[i] < 5:
                    red = False
                    chose.append(DUp_cu[i])
                    chose.append(DU_cu[i])
                    chose.append(DP_cu[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
            elif tip == 'monofazic':
                if aer_tub_i7_cu_mono[i] > I and DUp_cu[i] < 5:
                    red = False
                    chose.append(DUp_cu[i])
                    chose.append(DU_cu[i])
                    chose.append(DP_cu[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
        if pozare.lower() == 'subteran_tub':
            if tip == 'trifazic':
                if pamant_tub_i7_cu[i] > I and DUp_cu[i] < 5:
                    red = False
                    chose.append(DUp_cu[i])
                    chose.append(DU_cu[i])
                    chose.append(DP_cu[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
            elif tip == 'monofazic':
                if pamant_tub_i7_cu_mono[i] > I and DUp_cu[i] < 5:
                    red = False
                    chose.append(DUp_cu[i])
                    chose.append(DU_cu[i])
                    chose.append(DP_cu[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
        if pozare.lower() == 'aerian_notub':
            if tip == 'trifazic':
                if aer_no_tub_i7_cu[i] > I and DUp_cu[i] < 5:
                    red = False
                    chose.append(DUp_cu[i])
                    chose.append(DU_cu[i])
                    chose.append(DP_cu[i])
                    chose.append(sectiuni[i])
                    chose.append(red)
                    break
            elif tip == 'monofazic':
                if aer_no_tub_i7_cu_mono[i] > I and DUp_cu[i] < 5:
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
