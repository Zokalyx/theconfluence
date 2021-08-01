import csv
import matplotlib.pyplot as plt
import numpy as np

week = int(open("../../data/week.txt", "r").readline())


def main():
    # Read files and get matrices as objects
    deps = get_data_list("departures")
    arrs = get_data_list("arrivals")

    # Where data for the graph is stored
    graph_data_raw = []
    graph_data_percentage = []

    # Start loop over departures
    run = 1
    for week, dep in enumerate(deps):
        # If departures file was empty, ignore
        if not dep:
            continue
        run += 1

        # The arrival week corresponding to the people
        # departing is week - 1, but we have to account
        # for the fact that week is 0-indexing
        arr_week = week-1+1
        # Handle empty weeks
        while not arrs[arr_week]:
            arr_week -= 1

        # Index over list corresponding to departures
        # of the current week
        # Loop until a user who arrived last run is found
        # The number of people before that one ( = amount)
        # is the amount of people who joined previously
        for amount, departed in enumerate(dep):
            if departed in arrs[arr_week]:
                print(f"Run {run}: {amount}")
                graph_data_raw.append(amount)
                graph_data_percentage.append(100*amount/len(dep))
                break
        
    create_graph(graph_data_raw, "raw", " "*25 + "Unexpected departures per run")
    create_graph(graph_data_percentage, "percentage", " "*25 + "Same, but as a percentage of population")


def is_empty(l):
    for i in l:
        if i:
            return False
    return True


def is_whitepsace(l):
    for i in l:
        if i not in (" ", "\t", "\n"):
            return False
    return True


def get_data_list(type):

    data_list = []

    if type == "arrivals":
        with open("../../data/arrivals/1.txt") as f:
            data_list.append([ row.strip("\n") for row in f.readlines() if not is_empty(row) and not is_whitepsace(row) ])

    for i in range(1, week):
        with open(f"../../data/{type}/{i+1}.txt") as f:
            data_list.append([ row.split(" ")[1].strip("\n") for row in f.readlines() if not is_empty(row) and not is_whitepsace(row) ])

    return data_list


def create_graph(data, name, desc):
    fig = plt.figure()
    g = fig.add_subplot()
    g.set_xlabel("Run")
    plt.grid(True)
    g.set_ylim(ymin=0, ymax=1.1*max(data))

    plt.plot(range(2, len(data) + 2), data, linewidth=2)

    plt.figtext(0.16, 0.93,desc)
    plt.savefig(f"subretention{name}.png")


main()
