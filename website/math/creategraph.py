from pathlib import Path
import csv
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

import math
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


w = open("../../data/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

people = []
percentage = []

pop = 0 #Auxiliary variable

raw = open("../../data/basic/raw.csv", "r", newline="")
with raw:
    reader = csv.reader(raw)

    for i in range(week):

        if i == 0:
            next(reader) #Skips first week departures (empty)
            next(reader)
        elif i == 5 or i == 11:
            next(reader) #Irrelevant info. Add the same as last week
            next(reader)
            people.append(people[len(people)-1])
            percentage.append(percentage[len(percentage) - 1])
        else:
            next(reader) #Skips names
            bye = len(next(reader))
            pop -= bye
            people.append(pop)
            percentage.append(pop/(pop+bye))

        if i == 5 or i == 11:
            next(reader) #Skip empty
            next(reader)
        else:
            next(reader)
            pop += len(next(reader))
raw.close()

# for i in range(len(percentage)):
    # percentage[i] *= 100

#fix broken weeks

with open("../../data/broken.txt") as b:
    brokenWeeks = [int(wk) - 2 for wk in b.readlines()]

for broken in brokenWeeks:
    if broken + 2 == week:
        percentage[broken] = percentage[broken-1]
    else:
        percentage[broken] = (percentage[broken-1]+percentage[broken+1])/2

for broken in reversed(brokenWeeks):
    percentage.pop(broken)

diff = []
for i, p in enumerate(percentage):
    if i == 0:
        continue
    diff.append(percentage[i] - percentage[i-1])

percentage.pop()

def transpose(m):
    n = []
    a = len(m)
    b = len(m[0])
    for i in range(b):
        n.append([])
        for j in range(a):
            n[-1].append(m[j][i])
    return n


def submatrix(m, a, b):
    n = []
    for i, row in enumerate(m):
        if i == a:
            continue
        n.append([])
        for j, cell in enumerate(row):
            if j == b:
                continue
            n[-1].append(m[i][j])
    return n


def determinant(m):
    if len(m) == 1:
        return m[0][0]
    d = 0
    s = 1
    for i, row in enumerate(m):
        d += s * row[0] * determinant(submatrix(m, i, 0))
        s *= -1
    return d


def matrix_product(a, b):
    m = []
    for i in range(len(a)):
        m.append([])
        for j in range(len(b[0])):
            s = 0
            for k in range(len(b)):
                s += a[i][k] * b[k][j]
            m[-1].append(s)
    return m


def matrix_scale(m, s):
    n = []
    for row in m:
        n.append([])
        for cell in row:
            n[-1].append(s * cell)
    return n


def cofactor(m, a, b):
    return determinant(submatrix(m, a, b))


def cofactor_matrix(m):
    n = []
    s = 1
    for i, row in enumerate(m):
        n.append([])
        t = 1
        for j, cell in enumerate(row):
            n[-1].append(s * t * cofactor(m, i, j))
            t *= -1
        s *= -1
    return n


# https://en.wikipedia.org/wiki/Adjugate_matrix
def adjugate(m):
    return transpose(cofactor_matrix(m))


def inverse(m):
    return matrix_scale(adjugate(m), 1 / determinant(m))

# Creates row matrix
def create_matrix(*args):
    m = []
    for vector in args:
        m.append([])
        for element in vector:
            m[-1].append(element)
    return m

# https://stackoverflow.com/a/50257693/10236655
def pretty(m):
    print('\n'.join(['\t'.join([str(truncate(cell, 2)) for cell in row]) for row in m]))

one_matrix = [1 for _ in percentage]

a_transpose = create_matrix(one_matrix, percentage)

b = transpose(create_matrix(diff))

a_transpose_b = matrix_product(a_transpose, b)

a_transpose_a = matrix_product(a_transpose, transpose(a_transpose))

x = matrix_product(inverse(a_transpose_a), a_transpose_b)

k = x[0][0]
s = -(k + x[1][0])

print(percentage)

"""
with open("a.csv", "w", newline='') as f:
    writer = csv.writer(f)
    for p in percentage:
        writer.writerow([p])
"""
