# -*- coding:utf-8 -*-
'''
词法分析器的四个任务：
1.识别记号，并供语法分析器使用
2.处理与平台相关的输入
3.滤掉源程序中的无用成分
4.识别非法输入，并报告错误

记号的组成：
记号的类别和属性
'''

COMMENTS = {'//', '--'}
WHITE_SPACE = {'\t', '\n', '\r'}
OPERATORS = {'+', '-', '*', '/', '**', ';', '(', ')', ',', '.'}
'''
SEMICO = {';'}
L_BRACKET = {'('}
R_BRACKET = {')'}
COMMA = {','}
CONST_ID = {'.'}
'''


def scanner(str):
    '''
    共分为三大块，分别是标识符，数字，符号
    :return:
    '''
    str = str.lower() #语言对大小写
    token = []
    i = 0
    count = 0

    while i < len(str):
        # 跳过空格,换行符
        if str[i] in {' ', '\n'}:
            i=i+1
            continue
        # 识别数字
        if (str[i]>='0' and str[i]<='9'):
            j = i
            i += 1
            if (i < len(str) and str[i]=='.'):
                i += 1
            while(i < len(str) and str[i]>='0' and str[i]<='9'):
                i += 1
                if (i < len(str) and str[i] == '.'):
                    i += 1
            token.append(str[j:i])
            continue
        # 识别运算符
        if str[i:i+2] in OPERATORS:   # **
            token.append(str[i:i+2])
            i += 2
            continue
        elif str[i] in OPERATORS:    # 其他
            token.append(str[i:i+1])
            i += 1
            continue
        # 识别标识符
        if str[i].isalpha():  # .isalpha()识别是否全部为字母
            j = i
            while ( str[i].isalpha() and i < len(str) ):
                i += 1
            token.append(str[j:i])
            continue

    return token




if __name__ == '__main__':
    str1 = 'origin is (80.2, 40);'
    str2 = 'scale is (100, 200);'
    str3 = 'for t from 0 to 6.28 step 0.0314 * 3 draw(10 * cos(t), 10 * sin(t));'
    print(scanner(str1))
    print(scanner(str2))
    print(scanner(str3))











