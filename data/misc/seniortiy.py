import csv

leaders = []

num = 1

with open("../basic/probyuser.csv") as f:
    reader = csv.reader(f)
    for user in reader:
        if user[-1] != '0':
            leaders.append(f"{num} {user[0]}")
            num += 1