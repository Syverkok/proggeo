import math as mt
# Script for calculating the geodial height N from a Global Gravity Model.

# Constants needed in the formula for calculation of N
a = 6378137.0000
b = 6356752.3141
f = 298.257222101
e2 = 0.006694380023
R = 6371000.7900
GM = 3986005 * 10 ** 8
Y = 9.81
j2 = 0.108263 * (10 ** -2)

# Dictionary for storing values in the recursion when calculating the Normalized Legendre’s polynomials
p_dict = {}


# Sub function used for calculating N
def get_j_bar(n):
    if (n % 2) != 0:
        return 0
    return (-1)**(n/2) * ((3*mt.sqrt(e2)**n)*(1-(n/2)+((5/2)*(j2/e2)*n))) / ((n+1)*(n+3)*(2*n + 1)**0.5)


# Sub function used for calculating N
def get_r_bar(n, m, dic):
    if m == 0:
        return dic.get((n, m))[0] - get_j_bar(n)
    return dic.get((n, m))[0]


# Initial values needed for calculation of the Normalized Legendre’s polynomials. This is a "sub sub" function
def init_values(n, m, fi):
    ret = 0
    t = mt.sin(fi)
    if n == 0 and m == 0:
        ret = 1
    if n == 1 and m == 0:
        ret = t * mt.sqrt(3)
    if n == 1 and m == 1:
        ret = mt.sqrt(3) * mt.sqrt(1 - t ** 2)
    if n == 2 and m == 0:
        ret = mt.sqrt(5) * ((3 * t ** 2 / 2) - 1 / 2)
    if n == 2 and m == 1:
        ret = t * mt.sqrt(15) * mt.sqrt(1 - t ** 2)
    return ret


# Sub function used for calculating N. The sub function is calculating of the Normalized Legendre’s polynomials
def get_p_bar(n, m, fi, t):
    if (n, m,fi, t) in p_dict:
        return p_dict.get((n, m, fi, t))
    if n <= 2 and m <= 1:
        ret = init_values(n, m, fi)
    if n >= 2 and m == 0:
        ret = -mt.sqrt(2 * n + 1) / n * (n - 1) / mt.sqrt(2 * n - 3) * get_p_bar(n - 2, m, fi, t) + t * mt.sqrt(
                2 * n + 1) / n * mt.sqrt(2 * n - 1) * get_p_bar(n - 1, m, fi, t)
    if n >= 3 and 1 <= m <= n - 2:
        ret = -mt.sqrt(
            ((2 * n + 1) * (n + m - 1) * (n - m - 1)) / ((2 * n - 3) * (n + m) * (n - m))) * \
            get_p_bar(n - 2, m, fi, t) + t * mt.sqrt(
            ((2 * n + 1) * (2 * n - 1)) / ((n + m) * (n - m))) * get_p_bar(n - 1, m, fi, t)
    if n >= 1 and m == n - 1:
        ret = t * mt.sqrt(2 * n + 1) * get_p_bar(n - 1, n - 1, fi, t)
    if n == m >= 2:
        ret = mt.sqrt((2 * n + 1) / (2 * n)) * mt.sqrt(1 - t ** 2) * get_p_bar(n - 1, n - 1, fi, t)
    p_dict[(n, m, fi, t)] = ret
    return ret


# The main function for calculation of the geoidal Height N used when having many similar phi's
def get_n(lam, dic, n_max, pdict):
    sum_sub = 0
    sum_tot = 0
    for n in range(2, n_max+1):
        for m in range(0, n + 1):
            sum_sub += (get_r_bar(n, m, dic) * mt.cos(m * lam) + dic.get((n, m))[1] *
                        mt.sin(m * lam)) * pdict[n,m]
        sum_tot += sum_sub * (a / R) ** n
        sum_sub = 0
    return sum_tot * GM / (R * Y)

# The main function for calculation of the geoidal Height N
def get_n2(phi, lam, dic, n_max):
    sum_sub = 0
    sum_tot = 0
    for n in range(2, n_max+1):
        for m in range(0, n + 1):
            sum_sub += (get_r_bar(n, m, dic) * mt.cos(m * lam) + dic.get((n, m))[1] *
                        mt.sin(m * lam)) * get_p_bar(n, m, phi, mt.sin(phi))
        sum_tot += sum_sub * (a / R) ** n
        sum_sub = 0
    return sum_tot * GM / (R * Y)

