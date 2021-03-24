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
    return parser.parse_args()