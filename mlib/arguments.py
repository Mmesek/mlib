'''
ArgParse wrapper
---
arguments.add("cmd")

arg = arguments.parse()

arg.cmd

'''
import argparse

parser = argparse.ArgumentParser()

def add(*args, **kwargs):
    return parser.add_argument(*args, **kwargs)

def parse():
    args, unknown = parser.parse_known_args()
    return args

def parse_all():
    return parser.parse_args()