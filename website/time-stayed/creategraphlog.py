from pathlib import Path
import csv
import matplotlib.pyplot as plt
import math


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


w = open("../../data/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

dataToGraph = [0 for i in range(week)]

pop = 0

proby = open("../../data/basic/probyuser.csv", "r", newline="")
with proby:
    reader = csv.reader(proby)
    for row in reader:
        if row == "":
            break
        personStayed = 0
        for i in range(week):
            if int(row[i+1]) > 0:
                personStayed += 1
        dataToGraph[personStayed-1] += 1

proby.close()

average = 0
n = 0
for i in range(len(dataToGraph)):
    n += dataToGraph[i]
    average += (i + 1)*dataToGraph[i]
average /= n

print(dataToGraph)
print(average)
print(n)

fig = plt.figure()
g = fig.add_subplot()
g.set_ylabel("People")
g.set_xlabel("Weeks stayed")
plt.bar([i + 1 for i in range(week)], dataToGraph)
plt.figtext(0.16, 0.93,"              Timed stayed in the sub - Average: " + str(truncate(average,3)) + " weeks")
plt.axvline(average,0,average, color='black', linestyle='-.', linewidth=1)
g.set_yscale("log")
plt.savefig("graphWith1.png")


