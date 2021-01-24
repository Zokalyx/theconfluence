from pathlib import Path

w = open("../week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

with open("script.js","r") as jsfile:
    data = jsfile.readlines()

data[0] = "var week = " + str(week) + ";\n"

with open("script.js","w") as jsfile:
    jsfile.writelines(data)

with open("searchbyuser.js","r") as jsfile:
    data = jsfile.readlines()

data[0] = "var week = " + str(week) + ";\n"

with open("searchbyuser.js","w") as jsfile:
    jsfile.writelines(data)

with open("converter.js","r") as jsfile:
    data = jsfile.readlines()

data[0] = "var week = " + str(week) + ";\n"

with open("converter.js","w") as jsfile:
    jsfile.writelines(data)