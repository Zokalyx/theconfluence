import csv

w = open("../week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

p = open("../arrivals/" + str(week) + ".txt", "r") # Get population
for last_line in p:
    pass
p.close()
space = last_line.find(" ")
pop = int(last_line[0:space])
# pop = 162

leaders = []

pro = open("../basic/pro.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for i in range(pop):
        ppl = next(reader)
        leaders.append(ppl[len(ppl)-1])
pro.close()

names = open("marblesonstream.csv", "w", newline="")
for leader in leaders[:64]:
    names.write(leader + "\n")
names.close()
