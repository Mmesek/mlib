from typing import List


def read_file(filename: str, filter_func: callable=lambda i: i) -> list:
    with open(filename,'r',newline='',encoding='utf-8') as file:
        lines = file.readlines()
    array = []
    for line in lines:
        array.append(filter_func(line.strip()))
    return array

def write_file(filename: str, lines: list) -> None:
    with open(filename,'w',encoding='utf-8') as file:
        file.writelines(lines)

def load_csv(filename) -> List:
    import csv
    rows = []
    with open(filename,'r',newline='',encoding='utf-8') as file:
        for row in csv.reader(file):
            rows.append(row)
            #yield row
    return rows