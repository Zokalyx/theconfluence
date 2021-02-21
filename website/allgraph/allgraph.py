from pathlib import Path
import csv
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import colorsys


w = open("../../data/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

raw = open("../../data/basic/probyuser.csv", "r", newline="")
mega = []
with raw:
    for row in csv.reader(raw):
        mega.append(row)
raw.close()


def separate(array):
    ans = []
    starting = []
    start_new = True
    last = 0
    for i in range(len(array)):
        a = int(array[i])
        if a != 0:
            if a > last:
                start_new = True

            if start_new:
                ans.append([a])
                starting.append([i])
                start_new = False
            else:
                ans[-1].append(a)
                starting[-1].append(i)
            last = a
        else:
            start_new = True
    return [ans, starting]


def plot_user(index, ax):
    d = 75
    color = colorsys.hsv_to_rgb((index % d)/d, 0.70, 0.70)
    data = separate(mega[index][1:])
    for i in range(len(data[0])):
        ax.plot(data[1][i], data[0][i], "o", ms=0.5, c=color)
        ax.plot(data[1][i], data[0][i], solid_capstyle = "round", c=color, lw=0.95)



plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlabel("Week")
ax.set_ylabel("Flair number")
for i in range(len(mega)):
    plot_user(i, ax)
for user in mega:
    if int(user[-1]) != 0:
        ax.text(week-1 + 0.075, int(user[-1]) - 0.2, user[-1] + " " + user[0], fontsize = 1.5)
plt.savefig("highres.png", dpi = 500, bbox_inches='tight')
plt.savefig("lowres.png", dpi = 150, bbox_inches="tight")