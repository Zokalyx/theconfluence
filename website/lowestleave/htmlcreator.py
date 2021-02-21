import csv
from pathlib import Path

w = open("../../data/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

p = open("../../data/arrivals/" + str(week) + ".txt", "r") # Get population
for last_line in p:
    pass
p.close()
space = last_line.find(" ")
pop = int(last_line[0:space])

leaders = []

pro = open("../../data/basic/pro.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for i in range(pop):
        ppl = next(reader)
        leaders.append(ppl[len(ppl)-1])
pro.close()

lead = open("lead.html", "w")
lead.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='style.css'></head><body id=\"iframe\">")
for i in range(pop):
    lead.write(str(i+1) + ". " + leaders[i])
    if wk == week:
        if comment_array[i][1] == "True":
            lead.write(" <a href=https://www.{} target=\"_parent\"><b>&checkmark;</b></a>".format(comment_array[i][2]))
        else:
            lead.write(" <span style=\"color: #FF5901;\"><b>&cross;</b></span>")
    lead.write("<br>")
lead.write("</body></html>")
lead.close()

names = open("names.txt", "w")
for leader in leaders[:5]:
    names.write(leader+"\n")
names.close()