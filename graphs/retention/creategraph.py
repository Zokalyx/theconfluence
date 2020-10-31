from pathlib import Path
import csv
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np


w = open(str(Path(__file__).parents[2]) + "/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

people = []
percentage = []

pop = 0 #Auxiliary variable

raw = open(str(Path(__file__).parents[2]) + "/csv/raw.csv", "r", newline="")
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

average = sum(percentage)/len(percentage) #Write overal averagee
with open("average.txt", "w") as note:
    note.write(str(average))

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
plt.plot(x,percentage)
plt.plot(x,percentage,"ro")
plt.grid(True)
g.set_ylim(ymin=0,ymax=1)
g.set_xlim(xmin=0,xmax=week)
plt.xticks(np.arange(0, week, 5))
plt.yticks(np.arange(0, 110, 10))
#plt.show()
plt.savefig("graph.png")