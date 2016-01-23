#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# Author : Xiang,Zuo
# E-Mail : xianglinks@gmail.com
# Date   : 2016-01-03 18:12:02
# About  : Plot the gain of using the helper node
# #############################################################################

import numpy as np
from matplotlib import pyplot as plt


def main():
    # init list for plot  ---------------------------------------------------------------
    total_no_helper_avg = []
    total_no_helper_hwci = []

    total_helper_avg = []
    total_helper_hwci = []
    recoder_avg = []
    recoder_hwci = []

    # read data from file ---------------------------------------------------------------
    data_file = open('./results_30.dat', 'r')
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
    num_sim = 50
    t_factor = 2.678  # 99% for two sided

    def calc_hwci(num):
        return (t_factor * float(num)) / np.sqrt(num_sim)

    total_no_helper_hwci = map(calc_hwci, total_no_helper_hwci)
    total_helper_hwci = map(calc_hwci, total_helper_hwci)
    recoder_hwci = map(calc_hwci, recoder_hwci)

    # calculate the gain with helper node
    gain = []
    for i in range(len(total_helper_avg)):
        gain.append(total_no_helper_avg[i] / total_helper_avg[i])
        gain[i] = gain[i] - 1
        gain[i] = gain[i] * 100

    # plot the result  ------------------------------------------------------------------
    e_3 = np.arange(0, 100, 5)

    plt.plot(e_3, gain, color='black', lw=1, ls='-', label='Gewinn durch Helfer', marker='o', markerfacecolor='None', markeredgewidth=1, markeredgecolor='black')

    # settings for the figure
    #  plt.title("")
    plt.xlabel("Paketverlustrate e_3 (%)")
    plt.ylabel("Gewinn (%)")
    # set extrem value on x and y axis
    plt.ylim(-100, 700)
    #  plt.xlim(30, 70)
    plt.legend(loc='upper left', prop={'size': 12})
    plt.grid()

    plt.savefig('./fig2(30)_gain.png', dpi=500)


if __name__ == "__main__":
    main()
