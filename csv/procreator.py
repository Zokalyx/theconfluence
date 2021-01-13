# Writes a file that orders all history sorting by flair number

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
# pop = 180

mega = [] # array containing the arranged information of all the raw file (to be saved in pro.csv)
for i in range(pop):
    mega.append([i+1])
    for j in range(week):
        mega[i].append(" ")

raw = open("raw.csv","r",newline="")
with raw:
    reader = csv.reader(raw)

    people = 0 # Debugging
    for i in range(week):

        # Departures logic, does not apply for first run
        namerow = next(reader)
        numrow = next(reader)
        people -= len(numrow)

        if i != 0:
            # first get the previous week members as they are and make it a list
            current = []
            for j in range(pop):
                current.append(mega[j][i])
            # delete the members who leave
            numrow.reverse()
            namerow.reverse()
            for j in range(len(numrow)):
                if current[int(numrow[j])-1] != namerow[j]:
                    print("error in departure " + str(i+1) + " entry " + numrow[j] + " " + namerow[j] + " (vs " + current[int(numrow[j])-1] + " in arrival)")
                current.pop(int(numrow[j])-1)

            # now make the rest of the weeks like that
            for j in range(len(current)):
                for k in range(i,week):
                    mega[j][k+1] = current[j]

        # Arrival logic
        namerow = next(reader)
        numrow = next(reader)
        people += len(numrow)
        if numrow:
            apparentpeople = numrow[len(numrow)-1]

        # write the arrivals in their corresponding place from that week onwards (someone else will have to take their place)
        for j in range(len(numrow)):
            for k in range(i,week):
                mega[int(numrow[j])-1][k+1] = namerow[j]

        if int(apparentpeople) != people: # Debugging
            print("week " + str(i+1) + ": expected " + str(people) + " people instead of " + apparentpeople)
raw.close()

#save the processed csv file with mega
pro = open("pro.csv","w",newline="")
with pro:
    writer = csv.writer(pro)
    for row in mega:
        writer.writerow(row)
pro.close()

raw.close()
