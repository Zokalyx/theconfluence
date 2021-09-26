import csv
import sys

week = int(sys.argv[1])

with open("../basic/pro.csv") as pro:
    reader = csv.reader(pro)
    for row in reader:
        print(f"{row[0]} {row[week]}")
