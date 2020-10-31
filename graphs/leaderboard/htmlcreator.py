import csv
from pathlib import Path

w = open(str(Path(__file__).parents[2]) + "/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

p = open(str(Path(__file__).parents[2]) + "/arrivals/" + str(week) + ".txt", "r") # Get population
for last_line in p:
    pass
p.close()
space = last_line.find(" ")
pop = int(last_line[0:space])

leaders = []

pro = open(str(Path(__file__).parents[2]) + "/csv/pro.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)

    for i in range(pop):
        ppl = next(reader)
        leaders.append(ppl[len(ppl)-1])
pro.close()

lead = open("lead.html","w")
lead.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='style.css'></head><body>")
for i in range(pop):
    lead.write(str(i+1) + ". " + leaders[i] + "<br>")
lead.write("</body></html>")
lead.close()