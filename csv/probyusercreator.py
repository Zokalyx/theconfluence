# Writes a file that orders all history sorting by user (essentially just rearranges pro.csv)

import csv

w = open("../week.txt","r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

p = open("../arrivals/" + str(week) + ".txt", "r") # Get population
for last_line in p:
    pass
p.close()
space = last_line.find(" ")
pop = int(last_line[0:space])

bynum = [] # contains the info of pro.csv
pro = open("pro.csv","r",newline="")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        bynum.append(row)
pro.close()
# week = 3
# pop = 5
mega = [] # to be written onto the file
for i in range(week):
    for j in range(pop):

        name = bynum[j][i+1]
        if name == " ":
            break
        whereisname = -1
        for k in range(len(mega)):
            if name == mega[k][0]:
                whereisname = k
                break

        if whereisname == -1: # -1 means it is still not in the list, and a row will be created.
            mega.append([name])
            whereisname = len(mega)-1
            for k in range(week):
                mega[len(mega)-1].append(0)

        mega[whereisname][i+1] = j + 1 # write their flair value on that week

proby = open("probyuser.csv","w",newline="") # Write the data
with proby:
    writer = csv.writer(proby)
    for row in mega:
        writer.writerow(row)
proby.close()