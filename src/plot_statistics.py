#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# Author : Xiang,Zuo
# E-Mail : xianglinks@gmail.com
# Date   : 2016-01-03 18:12:02
# About  : Plot statistical results of helper_test using matplotlib
# #############################################################################

import numpy as np
from matplotlib import pyplot as plt


def plotErrorBar(x, y, x_error, y_error):
    pass


def main():
    # init list for plot  ---------------------------------------------------------------
    total_no_helper_avg = []
    total_no_helper_hwci = []

    total_helper_avg = []
    total_helper_hwci = []
    recoder_avg = []
    recoder_hwci = []

    # read data from file ---------------------------------------------------------------
    data_file = open('./results.dat', 'r')
    data = data_file.read()
    data_file.close()

    # data processing -------------------------------------------------------------------
    data = data.split('\n')
    data.pop()

    for line in range(len(data)):
        # even line number: test without helper
        if line % 2 == 0:
            data_line = data[line]
            data_line = data_line.split(' ')
            data_line = data_line[0].split(',')
            total_no_helper_avg.append(data_line[0])
            total_no_helper_hwci.append(data_line[1])
        # odd line number: test with helper
        else:
            data_line = data[line]
            data_line = data_line.split(' ')
            total_line = data_line[0]
            recoder_line = data_line[1]

            total_line = total_line.split(',')
            total_helper_avg.append(total_line[0])
            total_helper_hwci.append(total_line[1])

            recoder_line = recoder_line.split(',')
            recoder_avg.append(recoder_line[0])
            recoder_hwci.append(recoder_line[1])

    # change data from string to float
    total_no_helper_avg = map(float, total_no_helper_avg)
    total_no_helper_hwci = map(float, total_no_helper_hwci)
    total_helper_avg = map(float, total_helper_avg)
    total_helper_hwci = map(float, total_helper_hwci)
    recoder_avg = map(float, recoder_avg)
    recoder_hwci = map(float, recoder_hwci)

    # calc the half width of confidence interval(using student-distribution)
    num_sim = 20
    t_factor = 2.845

    def calc_hwci(num):
        return (t_factor * float(num)) / np.sqrt(num_sim)

    total_no_helper_hwci = map(calc_hwci, total_no_helper_hwci)
    total_helper_hwci = map(calc_hwci, total_helper_hwci)
    recoder_hwci = map(calc_hwci, recoder_hwci)

    # plot the result  ------------------------------------------------------------------
    e_3 = np.arange(0, 100, 5)
    plt.errorbar(e_3, total_no_helper_avg, yerr=total_helper_hwci, color='red', label='without helper', lw=1.5, marker='.')
    plt.errorbar(e_3, total_helper_avg, yerr=total_helper_hwci, color='black', label='total packets sent with helper', lw=1.5, marker='.')
    plt.errorbar(e_3, recoder_avg, yerr=recoder_hwci, color='blue', label='packets sent from helper', lw=1.5, marker='.')

    # settings for the figure
    plt.title("Test for Helper Node")
    plt.xlabel("loss e_3 (%)")
    plt.ylabel("number of packets")
    plt.ylim(0, 1100)
    plt.xlim(0, 90)
    plt.legend(loc='upper left', prop={'size': 12})
    plt.grid()

    plt.savefig('e_2(0.4)_local2.png', dpi=1080)


if __name__ == "__main__":
    main()
