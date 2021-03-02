import csv
from pathlib import Path
from math import floor

w = open("../../data/week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

wek = open("wk.txt", "r")
wk = int(wek.read())
wek.close()

extra_text = "On Mondays and Tuesdays," \
             " a tick will appear indicating if the user has posted or commented during the week.<br><br>"
if wk == week:
    extra_text = "The tick indicates whether the user commented or posted since the last run began.<br>" \
                 "<span style=\"color: #F800FF;\">The ticks do not update automatically</span>;" \
                 " only when I run my script. I'll try to do it every Monday at" \
                 " <a href=\"https://www.google.com/search?q=15%3A00 GMT\" target=\"_parent\">15:00 GMT</a>.<br>" \
                 "You can click on the ticks to get sent to the user's latest comment or post.<br><br>"

comment_array = []
com = open("../../data/misc/commented.csv", "r", newline="")
reader = csv.reader(com)
for row in reader:
    comment_array.append(row)

p = open("../../data/arrivals/" + str(week) + ".txt", "r") # Get population
for last_line in p:
    pass
p.close()
space = last_line.find(" ")
pop = int(last_line[0:space])
# pop = 162

leaders = []

pro = open("../../data/basic/pro.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for i in range(pop):
        ppl = next(reader)
        leaders.append(ppl[len(ppl)-1])
pro.close()

before = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <base href="https://zokalyx.github.io/theconfluence/">

    <!-- tab -->
    <title>Leaderboard</title>
    <link rel="shortcut icon" type="image/ico" href="website/images/favicon.ico"/>

    <!-- external files -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="website/script.js"></script>
    <link rel="stylesheet" href="website/style.css">
</head>
<body onload="loaded()">
    <div id="wrapper">
    <!-- header -->
    <header>
        <a href="https://zokalyx.github.io/theconfluence">
            <img id="home" src="">
        </a>
        <a id="github" href="https://github.com/Zokalyx/theconfluence">
            <img class="external" src="website/images/github.png">
        </a>
        <a href="https://discord.gg/K2ykw9K">
            <img class="external" src="website/images/discord.png">
        </a>
        <a href="https://www.reddit.com/r/TheConfluence">
            <img class="external" src="website/images/reddit.png">
        </a>
        <span id="days">
        </span>
    </header>

    <!-- main -->
    <h1>
        Current standings
    </h1>
    <p class="important">
        Tip: Use Ctrl+F to find a user <br>
"""

after = """

    </p>

    </div>
    <!-- footer -->
    <footer>
        <div id="container">
            <img id="shh" src="website/images/shh.png">
            <p id="secret">
                This is a private community, so keep this a secret ;) <br>
                Website design and content by u/Zokalyx
            </p>
        </div>
    </footer>
</body>
</html>"""

lead = open("index.html", "w")
lead.write(before + extra_text)
for i in range(pop):
    lead.write(str(i+1) + ". " + leaders[i])
    if wk == week:
        if comment_array[i][1] == "True":
            lead.write(" <a href=https://www.{} title='{} day{} ago' target=\"_parent\"><b>&checkmark;</b></a>".format(comment_array[i][2], floor(float(comment_array[i][3])), "" if floor(float(comment_array[i][3])) == 1  else "s"))
        else:
            lead.write(" <span style=\"color: #FF5901;\"><b>&cross;</b></span>")
    lead.write("<br>\n")
lead.write(after)
lead.close()

names = open("names.txt", "w")
for leader in leaders[:5]:
    names.write(leader+"\n")
names.close()