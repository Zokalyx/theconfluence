import matplotlib.pyplot as plt
import numpy as np

with open("../../data/basic/raw.csv", "r") as raw:
    array = raw.readlines()

array = [i[0:-1] for i in array]
arr = []
for i in array:
    new = i.split(",")
    if len(new) > 0:
        try:
            arr.append([int(j) for j in new])
        except:
            pass
        finally:
            pass

actual_array = []
populations = []
lowests = []
mod_lowests = []
for i, el in enumerate(arr):
    if i % 2 == 0:
        populations.append(el[-1])
    else:
        actual_array.append(el)
        lowests.append(el[0])
        mod_lowests.append(el[0]/populations[-1])

mod_actual_array = [[actual_array[i][j]/populations[i] for j in range(len(actual_array[i]))] for i in range(len(actual_array))]

mod_averages = [sum(i)/len(i) for i in actual_array]
mod_averages = [mod_averages[i]/populations[i]*100 for i in range(len(mod_averages))]
mod_lowests = [lowests[i]/populations[i]*100 for i in range(len(lowests))]

mod_standards = [np.std(i)/4 for i in mod_actual_array]

averages = [sum(i)/len(i) for i in actual_array]
standards = [np.std(i)/4 for i in actual_array]

mod_actual_array = []
for i, el in enumerate(actual_array):
    mod_actual_array.append([])
    for j in el:
        mod_actual_array[i].append(j/populations[i]*100)
mod_averages = [sum(i)/len(i) for i in mod_actual_array]
mod_standards = [np.std(i)/4 for i in mod_actual_array]

print(mod_actual_array)

fig = plt.figure()
g = fig.add_subplot()
g.set_ylabel("Average and lowest flair of departures")
g.set_xlabel("Run")
plt.grid(True)

plt.plot(range(2, len(actual_array) + 2), averages, linewidth=2)
plt.plot(range(2, len(actual_array) + 2), lowests, linewidth=2)

plt.savefig("graph1.png")



fig = plt.figure()
g = fig.add_subplot()
g.set_ylabel("Average and lowest as % of total")
g.set_xlabel("Run")
plt.grid(True)
g.set_ylim(ymin=0, ymax=100)

plt.plot(range(2, len(actual_array) + 2), mod_averages, linewidth=2)
plt.plot(range(2, len(actual_array) + 2), mod_lowests, linewidth=2)

plt.savefig("graph2.png")
