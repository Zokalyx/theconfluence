from pathlib import Path
import csv
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

w = open("../../data/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

people = []
limitvalue = []

pop = 0

raw = open("../../data/basic/raw.csv", "r", newline="")
with raw:
    reader = csv.reader(raw)

    for i in range(week):

        if i == 0:
            next(reader) #Skips first week departures (empty)
            next(reader)
            limitvalue.append(0)
        elif i == 5 or i == 11:
            next(reader) #Irrelevant info. Add the same as last week
            next(reader)
            people.append(people[len(people)-1])
            limitvalue.append(limitvalue[len(limitvalue) - 1])
        else:
            next(reader) #Skips names
            bye = len(next(reader))
            pop -= bye
            limitvalue.append(pop)

        if i == 5 or i == 11:
            next(reader) #Skip empty
            next(reader)
        else:
            next(reader)
            pop += len(next(reader))
            people.append(pop)
raw.close()

#fix broken weeks
brokenWeeks = (5, 11, 35, 41, 54, 64, 94)
for broken in brokenWeeks:
    if broken + 1 == week:
        limitvalue[broken] = limitvalue[broken-1]
    else:
        limitvalue[broken] = (limitvalue[broken-1]+limitvalue[broken+1])/2

average = sum(limitvalue)/len(limitvalue) # Write average
with open("average.txt", "w") as note:
    note.write(str(average))

# USING MATPLOTLIB FOR NOW
limitvalue = np.array(limitvalue)
people = np.array(people)

x = np.arange(1,week+1)
xnew = np.linspace(0,week-1,num=401,)
#print(xnew)
f = interp1d(x, limitvalue, kind = "cubic")
f2 = interp1d(x, limitvalue)

#plt.plot(xnew, f(xnew))
#plt.plot(xnew, f2(xnew))
#plt.show()

fig = plt.figure()
g = fig.add_subplot()
g.set_ylabel("People")
g.set_xlabel("Week")
#g.plot(xnew, f(xnew))
#plt.axhline(minimum, 0, (minimumIndex+1)/week, color='black', linestyle='-.', linewidth=1)
#plt.axhline(maximum, 0, (maximumIndex+1)/week, color='black', linestyle='-.', linewidth=1)
plt.plot(x, people/2, "-.")
plt.plot(x,limitvalue,linewidth=3, color="#0029FF")
plt.plot(x,limitvalue,"ro",markersize=3, color="#00880A")
plt.plot(x, people,linewidth=4, color="#D59700")
plt.plot(x, people,"ro",markersize=4 , color="#306C48")

plt.grid(True)
g.set_ylim(ymin=0,ymax=100)
g.set_xlim(xmin=0,xmax=week+1)
plt.xticks(np.arange(0, week, 5))
plt.yticks(np.arange(0, people[len(people)-1] + 15, 10))

plt.figtext(0.16, 0.93,"Gold = Population              People above blue = Newcomers")

#print(people)
#plt.show()
plt.savefig("graph.png")

