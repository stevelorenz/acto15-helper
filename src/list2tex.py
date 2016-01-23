#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# Author : Xiang,Zuo
# E-Mail : xianglinks@gmail.com
# Date   : 2016-01-03 18:12:02
# About  : Convert values in list to a tex format table
# #############################################################################

import numpy as np


def main():
    # init list for plot
    total_no_helper_avg = []
    total_no_helper_std = []

    total_helper_avg = []
    total_helper_std = []
    recoder_avg = []
    recoder_std = []

    # read data from file
    data_file = open('./results_30.dat', 'r')
    data = data_file.read()
    data_file.close()

    # data processing
    data = data.split('\n')
    data.pop()

    for line in range(len(data)):
        # even line number: test without helper
        if line % 2 == 0:
            data_line = data[line]
            data_line = data_line.split(' ')
            data_line = data_line[0].split(',')
            total_no_helper_avg.append(data_line[0])
            total_no_helper_std.append(data_line[1])
        # odd line number: test with helper
        else:
            data_line = data[line]
            data_line = data_line.split(' ')
            total_line = data_line[0]
            recoder_line = data_line[1]

            total_line = total_line.split(',')
            total_helper_avg.append(total_line[0])
            total_helper_std.append(total_line[1])

            recoder_line = recoder_line.split(',')
            recoder_avg.append(recoder_line[0])
            recoder_std.append(recoder_line[1])

    # change data to float
    total_no_helper_avg = map(float, total_no_helper_avg)
    total_no_helper_std = map(float, total_no_helper_std)
    total_helper_avg = map(float, total_helper_avg)
    total_helper_std = map(float, total_helper_std)
    recoder_avg = map(float, recoder_avg)
    recoder_std = map(float, recoder_std)

    # calculate the gain with helper node
    gain = []
    for i in range(len(total_helper_avg)):
        gain.append(total_no_helper_avg[i] / total_helper_avg[i])
        gain[i] = gain[i] - 1
        gain[i] = gain[i] * 100

    # limit to 2 decimals
    def use2decimal(num):
        return '%.2f'% float(num)

    total_no_helper_avg = map(use2decimal, total_no_helper_avg)
    total_no_helper_std = map(use2decimal, total_no_helper_std)
    total_helper_avg = map(use2decimal, total_helper_avg)
    total_helper_std = map(use2decimal, total_helper_std)
    recoder_avg = map(use2decimal, recoder_avg)
    recoder_std = map(use2decimal, recoder_std)
    gain = map(use2decimal, gain)

    # change data format to string
    total_no_helper_avg = map(str, total_no_helper_avg)
    total_no_helper_std = map(str, total_no_helper_std)
    total_helper_avg = map(str, total_helper_avg)
    total_helper_std = map(str, total_helper_std)
    recoder_avg = map(str, recoder_avg)
    recoder_std = map(str, recoder_std)
    gain = map(str, gain)

    # save results in file
    loss = np.arange(0, 100, 5)

    abs_tex_file = open('./abs.tex', 'w+')
    for i in range(len(loss)):
        line = str(loss[i]) + ' & ' + total_no_helper_avg[i] + ' & ' + total_helper_avg[i] + ' & ' + recoder_avg[i] +' & '
        line = line + total_no_helper_std[i] + ' & ' + total_helper_std[i] + ' & ' + recoder_std[i] + ' \\\\ \hline' + '\n'
        abs_tex_file.write(line)

    gain_tex_file = open('./gain.tex', 'w+')

    line1 = 'e_3(%)'
    line2 = 'Gewinn(%)'

    for i in range(len(gain)):
        line1 = line1 + ' & ' + str(loss[i])
    line1 += ' \\\\ \hline' + '\n'

    for i in range(len(gain)):
        line2 = line2 + ' & ' + gain[i]
    line2 += ' \\\\ \hline' + '\n'

    gain_tex_file.write(line1)
    gain_tex_file.write(line2)

    abs_tex_file.close()
    gain_tex_file.close()


if __name__ == "__main__":
    main()
