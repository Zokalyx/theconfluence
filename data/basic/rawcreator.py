# Writes the contents of all arrivals and departures into a single file

import csv

w = open("../week.txt","r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

# Special iteration for first run (formatted differently)
arrfile = open("../arrivals/1.txt","r")
arr = arrfile.readlines()
arrfile.close()
arrfix = [i for i in arr if i != "\n"]
for i in range(len(arrfix)):
    arrfix[i] = arrfix[i].replace("\n", "")

# Csv file writing
raw = open("raw.csv","w",newline="")
with raw:
    writer = csv.writer(raw)

    # Special iteration for writing arrivals 1 and departures 1 (empty)
    writer.writerow([])
    writer.writerow([])
    writer.writerow(arrfix)
    writer.writerow(i + 1 for i in range(len(arrfix)))

    # Iteration for rest of runs
    for j in range(week - 1):

        # First row is departures
        depfile = open("../departures/" + str(j + 2) + ".txt", "r")
        dep = depfile.readlines()
        depfile.close()
        depfix = [i for i in dep if i != "\n"]
        for i in range(len(depfix)):
            depfix[i] = depfix[i].replace("\n", "")
        depnum = []
        for i in range(len(depfix)):
            if "." in depfix[i]:
                dot = depfix[i].find(".")
                depnum.append(depfix[i][0:dot])
                depfix[i] = depfix[i][dot + 2:len(depfix[i])]
            else:
                space = depfix[i].find(" ")
                depnum.append(depfix[i][0:space])
                depfix[i] = depfix[i][space + 1:len(depfix[i])]
        writer.writerow(depfix)
        writer.writerow(depnum)
        # Second row number corresponding to the members in departures

        # Similar to departures (arrivals)
        arrfile = open("../arrivals/" + str(j+2) + ".txt","r")
        arr = arrfile.readlines()
        arrfile.close()
        arrfix = [i for i in arr if i != "\n"]
        for i in range(len(arrfix)):
            arrfix[i] = arrfix[i].replace("\n", "")
        arrnum = []
        for i in range(len(arrfix)):
            if "." in arrfix[i]:
                dot = arrfix[i].find(".")
                arrnum.append(arrfix[i][0:dot])
                arrfix[i] = arrfix[i][dot+2:len(arrfix[i])]
            else:
                space = arrfix[i].find(" ")
                arrnum.append(arrfix[i][0:space])
                arrfix[i] = arrfix[i][space + 1:len(arrfix[i])]
        writer.writerow(arrfix)
        writer.writerow(arrnum)

raw.close()