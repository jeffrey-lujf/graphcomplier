# -*- coding:utf-8 -*-
from scanner import scanner
from parser2 import parser
srcs = [
      # ERROR_WRONG_TOKEN
    #'rot is ((1+ 2 + 3);',  # ERROR_UNMATCHED_BRACKETS
    #'rot is 1 ++ 2;',  # ERROR_WRONG_EXPRESSION
    #'for t is;',  # ERROR_WRONG_SYNTAX
    'scale is );'
]

for s in srcs:
    src = scanner(s)
    print(src)
    print(parser(src))