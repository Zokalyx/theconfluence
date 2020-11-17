import csv
from pathlib import Path

w = open(str(Path(__file__).parents[2]) + "/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

wek = open("wk.txt", "r")
wk = int(wek.read())
wek.close()

extra_text = ".<br>On Mondays and Tuesdays, a tick will appear indicating if the user has posted or commented in the week."
if wk == week:
    extra_text = ". The tick indicates whether the user commented or posted since the last run began.<br><span style=\"color: #F800FF;\">The ticks do not update automatically</span>; only when I run my script. I'll try to do it every Monday at <a href=\"https://www.google.com/search?q=15%3A00 GMT\" target=\"_parent\">15:00 GMT</a>.<br>You can click on the ticks to get sent to the user's latest comment or post."

comment_array = []
com = open("commented.csv", "r", newline="")
reader = csv.reader(com)
for row in reader:
    comment_array.append(row)

p = open(str(Path(__file__).parents[2]) + "/arrivals/" + str(week) + ".txt", "r") # Get population
for last_line in p:
    pass
p.close()
space = last_line.find(" ")
pop = int(last_line[0:space])
# pop = 162

leaders = []

pro = open(str(Path(__file__).parents[2]) + "/csv/pro.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for i in range(pop):
        ppl = next(reader)
        leaders.append(ppl[len(ppl)-1])
pro.close()

lead = open("lead.html", "w")
lead.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='style.css'></head><body id=\"iframe\">"
           "<h4>Tip: Use Ctrl+F to find a user" + extra_text + "</h4>")
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