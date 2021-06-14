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

for i in range(len(percentage)):
    percentage[i] *= 100

#fix broken weeks
brokenWeeks = (4, 10, 34, 40, 53, 63)
for broken in brokenWeeks:
    if broken + 2 == week:
        percentage[broken] = percentage[broken-1]
    else:
        percentage[broken] = (percentage[broken-1]+percentage[broken+1])/2

minimumIndex = 0 #Stuff for min and max
minimum = 100
maximumIndex = 0
maximum = 0

for i in range(len(percentage)):
    if percentage[i] > maximum:
        maximum = percentage[i]
        maximumIndex = i
    elif percentage[i] < minimum:
        minimum = percentage[i]
        minimumIndex = i

average = sum(percentage)/len(percentage) #Write minimum and it's index value, average and maximum and it's index value
with open("average.txt", "w") as note:
    note.write(str(minimum)+"\n")
    note.write(str(minimumIndex + 1) + "\n")
    note.write(str(average)+"\n")
    note.write(str(maximum) + "\n")
    note.write(str(maximumIndex + 1) + "\n")

# USING MATPLOTLIB FOR NOW
percentage = np.array(percentage)

x = np.arange(1,week)
xnew = np.linspace(1,week-1,num=401,)
#print(xnew)
f = interp1d(x, percentage, kind = "cubic")
f2 = interp1d(x, percentage)

#plt.plot(xnew, f(xnew))
#plt.plot(xnew, f2(xnew))
#plt.show()

fig = plt.figure()
g = fig.add_subplot()
g.set_ylabel("Retention Percentage (%)")
g.set_xlabel("Week")
#g.plot(xnew, f(xnew))
plt.axvline(minimumIndex+2,0,minimum/100, color='black', linestyle='-.', linewidth=1)
plt.axvline(maximumIndex+2,0,maximum/100, color='black', linestyle='-.', linewidth=1)
#plt.axhline(minimum, 0, (minimumIndex+1)/week, color='black', linestyle='-.', linewidth=1)
#plt.axhline(maximum, 0, (maximumIndex+1)/week, color='black', linestyle='-.', linewidth=1)
plt.plot(x+1, percentage, linewidth=3)
plt.plot(x+1, percentage, "ro")
plt.grid(True)
g.set_ylim(ymin=0,ymax=1)
g.set_xlim(xmin=0,xmax=week+1)
plt.xticks(np.arange(0, week, 5))
plt.yticks(np.arange(0, 110, 10))

plt.figtext(0.16, 0.93, "Minimum = " + str(truncate(minimum,2)) +"%   Average = " + str(truncate(average,2)) + "%   Maximum = " + str(truncate(maximum,2)) + "%")
#plt.show()
plt.savefig("graph.png")

print(percentage)