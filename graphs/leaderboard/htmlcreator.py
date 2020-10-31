import csv
from pathlib import Path

w = open(str(Path(__file__).parents[2]) + "/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

leaders = []
displayOnly = 10

pro = open(str(Path(__file__).parents[2]) + "/csv/pro.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)

    for i in range(displayOnly):
        ppl = next(reader)
        leaders.append(ppl[len(ppl)-1])
pro.close()

lead = open("lead.html","w")
lead.write("<!DOCTYPE html><html><body>")
for i in range(displayOnly):
    lead.write(str(i+1) + ". " + leaders[i] + "<br>")
lead.write("</body></html>")
lead.close()