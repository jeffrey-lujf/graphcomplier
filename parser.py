# -*- coding:utf-8 -*-
'''
1.设计函数绘图语言的文法，使其适合递归下降分析
2.使用语法树的结点，用于存放表达式的语法树
3.设计递归下降子程序，分析句子并构造表达式的语法树
4.测试
'''

from scanner import scanner
from math import sin, cos, pi


def is_num(src, signed=False):  #识别是否为数值
    dot = False
    i = 0
    while i < len(src):
        char = src[i]
        # filter illegal char
        if not signed:
            if not (char.isdigit() or char in {'.'}):
                return False
        else:
            if not (char.isdigit() or char in {'.', '-'}):
                return False
            if char == '-' and i != 0:
                return False
            if char == '-' and len(src) == 1:
                return False
        # handle '.'
        if char == '.':
            if dot:
                return False
            else:
                dot = True
        i += 1
    return True
# 优先级

# 操作符
OPERATIONS = {
    '**': lambda x, y: x**y,
    '*': lambda x, y: x*y,
    '/': lambda x, y: x/y,
    '+': lambda x, y: x+y,
    '-': lambda x, y: x-y,
}

# 函数
FUNCTIONS = {
    'sin': sin,
    'cos': cos,
}



def digital_calculate(token):#获得操作符，操作数，普通数值计算
    operators = []
    operands = []
    # 负号的判断
    i = 1
    while i < len(token):
        if (token[i]>='0' and token[i-1]=='-'):
            if token[i-2] in OPERATIONS or i == 1:
                token[i] = '-' + token[i]
                token.pop(i-1)
                i -= 1
        i += 1

    # 获得操作符和操作数，并检验输入的语句是否合法
    rr = 0  #在操作符后面必须跟一个操作数，rr作为判断条件
    i = 0
    while i <len(token):
        if (is_num(token[i],signed=True)):  #大于9的数怎么办，要解决
            if rr != 0:
                raise RuntimeError('WRONG_EXPR1')
            operands.append(float(token[i]))
            rr = 1
        elif token[i] in OPERATIONS:
            if rr != 1:
                raise RuntimeError('WRONG_EXPR2')
            operators.append(token[i])
            rr = 0
        i += 1
    #print((operands))
    #print((operators))
    if len(operands) != len(operators) + 1:
        raise RuntimeError('WRONG_EXPR3')
    i = len(operators) - 1
    #计算（处理操作符，操作数）
    # **
    while i >= 0:
        if operators[i] in {'**'}:
            operator = operators.pop(i)
            operand1 = operands.pop(i)
            operand2 = operands.pop(i)
            result = OPERATIONS[operator](operand1, operand2)
            operands.insert(i, result)
            i += 1
        i -= 1
    # * and /
    i = 0
    while i < len(operators):
        if operators[i] in {'*', '/'}:
            operator = operators.pop(i)
            operand1 = operands.pop(i)
            operand2 = operands.pop(i)
            result = OPERATIONS[operator](operand1, operand2)
            operands.insert(i, result)
            i -= 1
        i += 1
    # + and -
    i = 0
    while i < len(operators):
        if operators[i] in {'+', '-'}:
            operator = operators.pop(i)
            operand1 = operands.pop(i)
            operand2 = operands.pop(i)
            result = OPERATIONS[operator](operand1, operand2)
            operands.insert(i, result)
            i -= 1
        i += 1
    return operands[0]


# 带sin, cos等函数的计算
def func_calculate(token):
    # exp:sin(x, y)
    func = FUNCTIONS[token[0]]
    #args = []
    start = 2 # 'sin', '(' 从2开始
    result = digital_calculate(token[start:-1])
    return func(result)




# 处理带有括号的运算字符串，并的出最终计算结果
def final_calculate(token):
    i = 0
    func = False
    l_bracket = []
    while i < len(token):
        if token[i] in FUNCTIONS.keys():
            func = True
        if token[i] in {'('}:
            l_bracket.append(i)
        elif token[i] in {')'}:
            if not func:
                result = str(digital_calculate(token[l_bracket[-1] + 1: i]))
                token.insert(i+1, result)
                del token[l_bracket[-1]:i+1]
                i = l_bracket.pop()
            elif func:
                result = str(func_calculate(token[l_bracket[-1] - 1: i + 1]))
                token.insert(i + 1, result)
                del token[l_bracket[-1] - 1: i + 1]
                i = l_bracket.pop() - 1
                func = False
            else:
                raise RuntimeError('错误：括号不匹配')
        i += 1
    if len(l_bracket) != 0:
        raise RuntimeError('错误：括号不匹配')
    return digital_calculate(token)



if __name__ == '__main__':
    src = 'sin(50+30/3+40*1)'
    token = scanner(src)
    result = final_calculate(token)
    print(result)







