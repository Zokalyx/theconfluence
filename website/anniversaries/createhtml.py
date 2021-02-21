import csv
from pathlib import Path
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import ceil

w = open("../../data/week.txt", "r")
week = int(w.readline())
# = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

mega = []
upcoming = []
# Format: [Name, Date, Anniversary?]
pro = open("../../data/basic/probyuser.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        mega.append(row)
pro.close()

original = 1583722800000


def get_ms_from_week(wk):
    ans = original + (wk-1)*604800000
    if wk >= 36:
        ans += 172800000
    return ans


def get_date_from_ms(ms):
    return datetime.utcfromtimestamp(ms/1000)


def get_ms_from_sum(origin, months):
    ans = get_date_from_ms(origin) + relativedelta(months=months)
    return round(ans.timestamp()*1000)


def insert_into_correct_index(what, where):
    ind = 0
    last = True
    if len(where) == 0:
        where.append(what)
    else:
        for lol in where:
            if lol[3].timestamp() > what[3].timestamp():
                where.insert(ind, what)
                last = False
                break
            else:
                ind += 1
        if last:
            where.append(what)


time_now = get_ms_from_week(week)

for user in mega:
    if user[-1] != "0":
        origin_week = 0
        for i in range(len(user)):
            if i == 0:
                continue
            if user[i] != "0":
                origin_week = i
                break
        origin_ms = get_ms_from_week(origin_week)
        origin_date = get_date_from_ms(origin_ms)
        found_next_date = False
        index = 1
        ans_date = 0
        is_anni = False
        while not found_next_date:
            candidate = get_ms_from_sum(origin_ms, index*6)
            if candidate > time_now and not (index % 2 == 1 and index > 1):
                found_next_date = True
                if index % 2 == 0:
                    is_anni = True
                ans_date = get_date_from_ms(candidate)
            else:
                index += 1
        ans_list = [user[-1], user[0], origin_date, ans_date, is_anni, ceil(index/2)]
        insert_into_correct_index(ans_list, upcoming)


def get_string(user_anni, html):
    bold = "<b>" if html else ""
    bold_end = "</b>" if html else ""
    ending = "<br><br>" if html else ""
    aux_text = "Sem"
    if i[4]:
        aux_text = "#" + str(i[5]) + " Ann"
    ans = i[3].strftime("%b %d") + " - " + f"{bold}" + i[1] + f"{bold_end}" + "'s " + aux_text + "iversary (Joined: " + i[2].strftime("%d/%m/%Y") + ")" + f"{ending}" + "\n"
    return ans


before = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <base href="https://zokalyx.github.io/theconfluence/">

    <!-- tab -->
    <title>Anniversaries and Semiversaries</title>
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
        Anniversaries and Semiversaries
    </h1>
    <p class="important">
"""

after = """

    </p>
    <section class="content">
        <span> Notes </span>
        <p>
            Semiversaries commemorate 6 months since the user first joined the sub <br><br>
            Click <a href="website/anniversaries/results.txt"> here </a> for a full list of the upcoming anniversaries and semiversaries
        </p>
    </section>
    
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
lead.write(before)

for i in upcoming[:12]:
    lead.write(get_string(i, True))

lead.write(after)
lead.close()

with open("results.txt", "w") as results:
    for i in upcoming:
        results.write(get_string(i, False))


