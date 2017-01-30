# -*- coding:utf-8 -*-
import time
from plotter import turtle_plot
from scanner import scanner
from parser2 import parser

#
src1 = 'origin is (2, 3);' + 'for T from 0 to 30 step 1 draw (t, 0);' + 'for T from 0 to 20 step 1 draw (0, t);' + 'for T from 0 to 20 step 1 draw (t, t);'
#
src2 = 'origin is (60, 3);' + 'scale is (100, 100);' +'for t from 0 to 3.1415926*2 step 0.0314 * 3 draw(10 * cos(t), 10 * sin(t));'

#
src3 = 'origin is (2, -40);' + 'scale is (100, 200);' + 'rot is 3.1415926/2;' + 'for t from 0 to 6.28 step 0.0314 * 3 draw(10 * cos(t), 10 * sin(t));'

src4 = ''

src = src1 + src2 +src3
token1 = scanner(src1)
print(token1)

token2 = scanner(src2)
print(token2)

token3 = scanner(src3)
print(token3)

print(parser(token1))
#print(parser(token2))
#print(parser(token3))
turtle_plot(parser(token1))
turtle_plot(parser(token2))
turtle_plot(parser(token3))