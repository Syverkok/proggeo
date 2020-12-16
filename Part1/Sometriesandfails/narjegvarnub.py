import math as mt
import numpy

def get_p_naive_try(n, m, t):
    if n <= 2 and m <= 1:
        return init_values(n, m, t)

    if n >= 2 and m == 0:
        return_value = -mt.sqrt(2 * n + 1) / n * (n - 1) / mt.sqrt(2 * n - 3) * get_p_naive_try(n - 2, m,
                                                                                                t) + t * mt.sqrt(
            2 * n + 1) / n * mt.sqrt(2 * n - 1) * get_p_naive_try(n - 1, m, t)
        return return_value

    if n >= 3 and 1 <= m <= n - 2:
        return_value = -mt.sqrt(
            ((2 * n + 1) * (n + m - 1) * (n - m - 1)) / ((2 * n - 3) * (n + m) * (n - m))) * get_p_naive_try(n - 2, m,
                                                                                                             t) + t * mt.sqrt(
            ((2 * n + 1) * (2 * n - 1)) / ((n + m) * (n - m))) * get_p_naive_try(n - 1, m, t)
        return return_value

    if n >= 1 and m == n - 1:
        return_value = t * mt.sqrt(2 * n + 1) * get_p_naive_try(n - 1, n - 1, t)
        return return_value

    if n == m >= 2:
        return_value = mt.sqrt((2 * n + 1) / (2 * n)) * mt.sqrt(1 - t ** 2) * get_p_naive_try(n - 1, n - 1, t)
        return return_value


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


# The following two functions are another approach to calculate The Normalized Legendre’s polynomials
# The approach was attempted to improve the runtime, but didnt outperform the original method
def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return memoized_func


@memoize
def get_p_bar_memo(n, m, fi, t):
    if n <= 2 and m <= 1:
        return init_values(n, m, fi)
    if n >= 2 and m == 0:
        ret = -mt.sqrt(2 * n + 1) / n * (n - 1) / mt.sqrt(2 * n - 3) * get_p_bar_memo(n - 2, m, fi, t) + t * mt.sqrt(
                2 * n + 1) / n * mt.sqrt(2 * n - 1) * get_p_bar_memo(n - 1, m, fi, t)
        return ret
    if n >= 3 and 1 <= m <= n - 2:
        ret = -mt.sqrt(
            ((2 * n + 1) * (n + m - 1) * (n - m - 1)) / ((2 * n - 3) * (n + m) * (n - m))) * \
            get_p_bar(n - 2, m, fi, t) + t * mt.sqrt(
            ((2 * n + 1) * (2 * n - 1)) / ((n + m) * (n - m))) * get_p_bar_memo(n - 1, m, fi, t)
        return ret
    if n >= 1 and m == n - 1:
        ret = t * mt.sqrt(2 * n + 1) * get_p_bar_memo(n - 1, n - 1, fi, t)
        return ret
    if n == m >= 2:
        ret = mt.sqrt((2 * n + 1) / (2 * n)) * mt.sqrt(1 - t ** 2) * get_p_bar_memo(n - 1, n - 1, fi, t)
        return ret

# Calculation of N with the second approach
#@numpy.vectorize
def get_n_memo(fi, lam, dic, n_max):
    sum_sub = 0
    sum_tot = 0
    for n in range(2, n_max+1):
        for m in range(0, n + 1):
            sum_sub += (get_r_bar(n, m, dic) * mt.cos(m * lam) + dic.get((n, m))[1] *
                        mt.sin(m * lam)) * get_p_bar_memo(n, m, fi, mt.sin(fi))
        sum_tot += sum_sub * (a / R) ** n
        sum_sub = 0
    return sum_tot * GM / (R * Y)
