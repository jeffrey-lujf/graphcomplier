# -*- coding:utf-8 -*-
from math import sin, cos, pi, exp, log
from parser import final_calculate
from scanner import scanner
import copy


def origin(points, x, y, start=0):    # 设置原点的偏移量
    #print(points)
    #print(x,y)
    #print('start')
    #print(start)
    for p in points[start:]:
        p[0] += x
        p[1] += y
    #print(points)
    return points

def scale(points, x, y, start=0):     # 设置横坐标,纵坐标的比例
    for p in points[start:]:
        p[0] *= float(x) / 100
        p[1] *= float(y) / 100
    return points


def rot(points, rad, start=0):       # 设置旋转角度（0不旋转）
    for p in points[start:]:
        x = p[0]
        y = p[1]
        p[0] = x * cos(rad) + y * sin(rad)
        p[1] = y * cos(rad) - x * sin(rad)
    return points

'''
def test_transfer():
    points = [
        [0, 0],
        [1, 1]
    ]
    print(scale(points, 200, 100))
    print(origin(points, 2, 2))
    print(rot(points, pi))
'''

# 设置原点偏移量，比例，旋转角度的初始值
TRANS = {
    'origin': [0, 0],
    'scale': [100, 100],
    'rot': 0,
}

# 按横纵坐标比例，原点偏移量，旋转角度转换
def trans(points, start):
    points = scale(points, TRANS['scale'][0], TRANS['scale'][1], start=start)
    points = rot(points, TRANS['rot'], start=start)
    points = origin(points, TRANS['origin'][0], TRANS['origin'][1], start=start)
    return points

def do_for_draw(token, points):
    # for VAR from START to STOP step STEP draw(x, y)
    # ex:for t from 0 to 20 step 1 draw (t, t)
    #print('do_for_draw')
    former_len = len(points)
    var = token[1]
    i = 2
    tags = []
    while i < len(token): #检查语句是否完整
        if token[i] in {'from', 'to', 'step', 'draw'}:
            tags.append(i)
        i += 1
    if len(tags) != 4:
        raise RuntimeError('FOR_DRAW语句不完整')
    beg = tags[0] + 1 # tags[0] = 2
    end = tags[1]
    start = final_calculate(token[beg:end])  # start 起始点的计算
    beg = tags[1] + 1
    end = tags[2]
    stop = final_calculate(token[beg:end])   # end 终止点的计算
    beg = tags[2] + 1
    end = tags[3]
    step = final_calculate(token[beg:end])   # step 每个点增量的计算
    i = tags[3]
    while i < len(token): #计算draw()括号中的两个值x, y
        if token[i] == ',':
            e_x = token[tags[3]+2:i]
            e_y = token[i+1:-1]
            break
        i += 1
    i = start     #i = 起始点
    while i < stop:
        x = subs(e_x, var, i)
        y = subs(e_y, var, i)
        points.append([x, y])
        i += step
    points = trans(points, former_len)   # 转换求出的点，坐标偏移，比例，旋转角度
    return points

# 把t转换为实际坐标，用于do_draw_for函数
def subs(expr_argu, token, val):
    expr = copy.deepcopy(expr_argu) # 深度拷贝，拷贝对象及其子对象
    i = 0
    while i < len(expr_argu):
        if expr[i] == token:
            expr[i] = str(val)
        i += 1
    #print(expr)
    return final_calculate(expr)

def do_origin(token, points):
    # origin is (x, y)
    #print('do_origin')
    strat = -1
    i = 0
    while i < len(token):
        if token[i] == 'is':
            start = i + 2
            i += 1
        if token[i] == ',':
            x = final_calculate(token[start:i])
            y = final_calculate(token[i+1:-1])
            #print(x,y)
            TRANS['origin'] = [x, y]    # 坐标偏移量
            return points
        i += 1
    raise RuntimeError('ERROR_origin_SYNTAX')


def do_scale(token, points):
    # scale is (x, y)
    start = -1
    i = 0
    while i < len(token):
        if token[i] == 'is':
            start = i + 2
            i += 1 #跳过'('
        if token[i] == ',':
            x = final_calculate(token[start:i])
            y = final_calculate(token[i+1:-1])
            TRANS['scale'] = [x, y]   # 坐标比例
            return points
        i += 1
    raise RuntimeError('ERROR_scale_SYNTAX')


def do_rot(token, points):
    # rot is x
    i = 0
    while i < len(token):
        if token[i] == 'is':
            a = final_calculate(token[i+1:])
            TRANS['rot'] = a   # 旋转角度
            return points
        i += 1
    raise RuntimeError('ERROR_rot_SYNTAX')

# 把函数存入字典
COMMANDS = {
    'for': do_for_draw,
    'scale': do_scale,
    'origin': do_origin,
    'rot': do_rot
}

def parser(token):   # 语法分析器函数
    points = []
    i = 0
    start = -1
    while i < len(token):
        if token[i] in COMMANDS.keys():
            cmd = token[i]
            start = i
        elif token[i] == ';':  # 判断是否为一个完整的函数绘图语句，是则执行
            method = COMMANDS[cmd]
            points = method(token[start:i], points)
        i += 1
    return points



if __name__ == '__main__':
    src1 = 'origin is (80, 40);'
    src2 = 'scale is (100, 200);'
    src3 = 'rot is 3.14159;'
    src4 = 'for t from 0 to 6.28 step 0.0314 * 3 draw(t, t);'
    src = src1 + src2 +src4
    result = scanner(src)
    points = []
    print(result)
    aa = parser(result)
    #print (do_origin(result,points))
    print (aa)

