import numpy as np
import cmath
import matplotlib.pyplot as plt


def polygon_paths(n=3,s=1,h=5):
    omeg = cmath.exp((2 * cmath.pi * 1j) / n)
    sum1 = 0
    for j in range(0,n):
        sum1+=omeg**(-j*(h+s))*(1+omeg**(2*j))**h
    return int(sum1.real/n)


def tst():
    paths5 = [polygon_paths(n=5,h=h,s=2) for h in range(1,8)]
    paths6 = [polygon_paths(n=6,h=h,s=2) for h in range(1,8)]
    paths7 = [polygon_paths(n=7,h=h,s=2) for h in range(1,8)]
    paths8 = [polygon_paths(n=8,h=h,s=2) for h in range(1,8)]

    plt.plot(np.arange(1,8),paths5,label="5")
    plt.plot(np.arange(1,8),paths6,label="6")
    plt.plot(np.arange(1,8),paths7,label="7")
    plt.plot(np.arange(1,8),paths8,label="8")

    plt.legend()
    plt.show()


