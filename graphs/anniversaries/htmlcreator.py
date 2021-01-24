import csv
from pathlib import Path
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import ceil

w = open(str(Path(__file__).parents[2]) + "/week.txt", "r")
week = int(w.readline())
# = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

mega = []
upcoming = []
# Format: [Name, Date, Anniversary?]
pro = open(str(Path(__file__).parents[2]) + "/csv/probyuser.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        mega.append(row)
pro.close()

original = 1583712000000


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

lead = open("anniversaries.html", "w")
lead.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='style.css'></head><body id=\"iframe\">")
for i in upcoming[:12]:
    aux_text = "Sem"
    if i[4]:
        aux_text = "#" + str(i[5]) + " Ann"
    lead.write(i[3].strftime("%b %d") + " - " + "<b>" + i[1] + "</b>" + "'s " + aux_text + "iversary (Joined: " + i[2].strftime("%d/%m/%Y") + ")")
    lead.write("<br><br>")
lead.write("</body></html>")
lead.close()
