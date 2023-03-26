#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Serial Resistor TCR Calculator
# 孟奇 Meng Qi

from decimal import Decimal
import iec60063 as iec
import re

class Resistor(object):

    @property
    def resistance(self):
        return self.__resistance
    @resistance.setter
    def resistance(self, value):
        self.__resistance = value

    @property
    def tolerance(self):
        return self.__tolerance
    @tolerance.setter
    def tolerance(self, value):
        self.__tolerance = value

    @property
    def tcr(self):
        return self.__tcr
    @tcr.setter
    def tcr(self, value):
        self.__tcr = value

    @property
    def series(self):
        return self.__series
    @series.setter
    def series(self, value):
        self.__series = value

    def find_nearest(self):
        unit_number = 0
        tenhunderd = 0
        num3 = self.__resistance
        while num3 > 999:
            num3 /= 1000
            unit_number += 1
        num1 = num3
        while num1 > 9:
            num1 /= 10
            tenhunderd += 1
        
        nearest_res = min(iec.get_series(self.__series), key=lambda x:abs(x - Decimal(num1).quantize(Decimal('0.01'))))
        unit = iec.res_ostrs[unit_number + 1]
        res_value = nearest_res * (10 ** tenhunderd)
        real_value = float(res_value * (1000 ** unit_number))
        return {'decimal':res_value, 'unit':unit, 'real_value':real_value, 'series':self.__series}

# TCRserial = TCR1 x (R1/(R1+R2)) + TCR2 x (R2/(R1+R2))
class SerialTCR(object):
    def __init__(self, r1 = None, tcr1 = 3900, r2 = None, tcr2 = 0):
        self.__r1 = r1
        self.__tcr1 = tcr1
        self.__r2 = r2
        self.__tcr2 = tcr2

    @property
    def r1(self):
        return self.__r1
    @r1.setter
    def r1(self, value):
        self.__r1 = value

    @property
    def tcr1(self):
        return self.__tcr1
    @tcr1.setter
    def tcr1(self, value):
        self.__tcr1 = value

    @property
    def r2(self):
        return self.__r2
    @r2.setter
    def r2(self, value):
        self.__r2 = value

    @property
    def tcr2(self):
        return self.__tcr2
    @tcr2.setter
    def tcr2(self, value):
        self.__tcr2 = value

    @property
    def target_tcr(self):
        return self.__target_tcr
    @target_tcr.setter
    def target_tcr(self, value):
        self.__target_tcr = value
        
    def serial_tcr(self):
        r1 = self.__r1
        tcr1 = self.__tcr1
        r2 = self.__r2
        tcr2 = self.__tcr2
        tcr = tcr1 * (r1 / (r1 + r2)) + tcr2 * (r2 / (r1 + r2))
        return tcr

    def r2_calc(self):
        r1 = self.__r1
        tcr1 = self.__tcr1
        target_tcr = self.__target_tcr 
        r2 = (tcr1 * r1) / target_tcr - r1
        return r2
        

# 初始化：
r1 = Resistor()
r2 = Resistor()
tcr = SerialTCR()

if __name__ == '__main__':
    print(r"""

串联电阻温度系数计算器 - 输入热敏电阻的阻值、温度系数，以及所需的温度系数，程序给出特定 E 系列下的最优解
Serial TCR Calculator - Find the optimized real resistor for a target TCR.

--[PTC   ]--[NORMAL]--

孟奇 Meng Qi

Website : mengqimusic.com
Instagram : @mengqimusic

    """)
    
    series = input('E Series (E24 / E48 / E96 / E192) : ')
    while not series in ['E24', 'E48', 'E96', 'E192']:
        print('(wrong input)')
        series = input('E Series (E24 / E48 / E96 / E192) : ')
    r1.series = series
    r2.series = series

    keyboard_input = input('TCR Resistance Value (integer) = ')
    while not re.match(r'^[0-9]+$', keyboard_input):
        print('(wrong input)')
        keyboard_input = input('TCR Resistance Value (integer) = ')
    r1.resistance = int(keyboard_input)
    tcr.r1 = r1.resistance


    keyboard_input = input('TCR Temperature Coeffectiet (integer) = ')
    while not re.match(r'^[0-9]+$', keyboard_input):
        print('(wrong input, integer plz. 请输入整数)')
        keyboard_input = input('TCR Temperature Coeffectiet (integer) = ')
    r1.tcr = int(keyboard_input)
    tcr.tcr1 = r1.tcr

    keyboard_input = input('Targe TCR (integer) = ')
    while not re.match(r'^[0-9]+$', keyboard_input):
        print('(wrong input)')
        keyboard_input = input('Targe TCR (integer) = ')
    target_tcr = int(keyboard_input)
    tcr.target_tcr = target_tcr

    r2.resistance = tcr.r2_calc()
    res = r2.find_nearest()
    tcr.r2 = res['real_value']
    tcr_result = tcr.serial_tcr()
    print()
    print()
    print('Nearest Resistor = ', str(res['decimal']) + res['unit'])
    print('Serial Resistor TCR = ', tcr_result)
    print('Serial Resistor Resitance = ', r1.resistance + tcr.r2)
    print()