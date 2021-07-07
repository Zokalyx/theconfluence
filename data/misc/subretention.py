import csv
week = 70


def main():
    deps = get_data_list("departures")
    arrs = get_data_list("arrivals")

    run = 1
    for week, dep in enumerate(deps):
        if not dep:
            continue
        run += 1

        arr_week = week-1+1
        while not arrs[arr_week]:
            arr_week -= 1

        for amount, departed in enumerate(dep):
            if departed in arrs[arr_week]:
                print(f"Run {run}: {amount}")
                break


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
        with open("../arrivals/1.txt") as f:
            data_list.append([ row.strip("\n") for row in f.readlines() if not is_empty(row) and not is_whitepsace(row) ])

    for i in range(1, week):
        with open(f"../{type}/{i+1}.txt") as f:
            data_list.append([ row.split(" ")[1].strip("\n") for row in f.readlines() if not is_empty(row) and not is_whitepsace(row) ])

    return data_list

main()
